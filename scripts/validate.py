#!/usr/bin/env python3
"""اعتبارسنجی spec در برابر جدول کدها.

هدف این نیست که spec «معتبر OpenAPI» باشد، آن کار redocly است. هدف این است
که چیزهایی که همیشه بی‌صدا از هم واگرا می‌شوند، بلند شکست بخورند:

  ۱. enum هر کد در spec، در برابر جدول متناظرش در codes/
  ۲. هر مسیری که operationId، summary، description یا tag ندارد
  ۳. هر ارجاع شکسته یا مدل بی‌استفاده

enum در spec شامل کدهایی است که `in_api` یا `confirmed` باشند: یا سرویس
اعلامشان می‌کند، یا ما مستقلاً وجودشان را تأیید کرده‌ایم.

کدی که `confirmed` نیست یک شکاف در خود سرویس است، نه در این مخزن. شکاف
خطا نیست، هشدار است، و با `--gaps` فهرست کاملش را می‌گیرید.

    python3 scripts/validate.py            بررسی و گزارش
    python3 scripts/validate.py --gaps     فقط فهرست شکاف‌ها، برای پیگیری
    python3 scripts/validate.py --strict   هشدار هم شکست حساب می‌شود
"""

import sys
import pathlib

try:
    import yaml
except ImportError:
    sys.exit("PyYAML لازم است:  pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent

# جدول کدها، و جایی در اسکیما که enum متناظرش می‌نشیند.
TABLES = [
    ("error-codes.yaml", ["ErrorCode", "enum"], "کد خطا"),
    ("status-codes.yaml", ["StatusItem", "properties", "StatusCode", "enum"], "کد وضعیت"),
    ("template-status.yaml", ["TokenListDetail", "properties", "Status", "enum"], "وضعیت قالب"),
]

errors = []
warnings = []
gaps = []


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dig(node, keys):
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def check_codes(label, version_dir, schemas):
    for filename, keys, what in TABLES:
        table_path = version_dir / "codes" / filename
        if not table_path.exists():
            errors.append(f"{label}: {filename} نیست")
            continue

        enum = dig(schemas, keys)
        if enum is None:
            errors.append(f"{label}: مسیر {'.'.join(keys)} در spec پیدا نشد")
            continue

        table = load(table_path)
        rows = table.get("codes") or []
        in_spec = set(enum)
        # هر کدی که سرویس اعلام می‌کند یا ما تأییدش کرده‌ایم، باید در enum باشد
        expected = {r["code"] for r in rows if r.get("in_api") or r.get("confirmed")}

        for code in sorted(in_spec - expected):
            errors.append(f"{label}: {what} {code} در enum spec هست ولی در {filename} پشتوانه‌ای ندارد")
        for code in sorted(expected - in_spec):
            errors.append(f"{label}: {what} {code} در {filename} هست ولی در enum spec نیست")

        seen = set()
        for row in rows:
            code = row["code"]
            if code in seen:
                errors.append(f"{label}: {what} {code} در {filename} تکراری است")
            seen.add(code)

            if row.get("in_docs") and not row.get("fa"):
                errors.append(f"{label}: {what} {code} علامت in_docs دارد ولی متن fa ندارد")

            if not row.get("confirmed"):
                if not row.get("in_docs"):
                    reason = "سرویس اعلامش می‌کند ولی شرح رسمی ندارد"
                elif not row.get("in_api"):
                    reason = "مستند شده ولی سرویس اعلامش نمی‌کند"
                else:
                    reason = "تأیید نشده"
                gaps.append((label, what, code, reason))
                warnings.append(f"{label}: {what} {code} تأیید نشده، {reason}")


def check_operations(label, spec):
    seen_ids = {}
    for path, item in (spec.get("paths") or {}).items():
        for method, op in item.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            where = f"{label}: {method.upper()} {path}"
            for field in ("operationId", "summary", "description"):
                if not op.get(field):
                    errors.append(f"{where} فیلد {field} ندارد")
            if not op.get("tags"):
                errors.append(f"{where} tag ندارد")
            op_id = op.get("operationId")
            if op_id:
                if op_id in seen_ids:
                    errors.append(f"{where} operationId تکراری با {seen_ids[op_id]}")
                seen_ids[op_id] = where
    return seen_ids


def check_refs(label, spec, schemas):
    def walk(node, trail):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str):
                prefix = "#/components/schemas/"
                if not ref.startswith(prefix):
                    errors.append(f"{label}: ارجاع ناشناخته {ref} در {trail}")
                elif ref[len(prefix):] not in schemas:
                    errors.append(f"{label}: ارجاع شکسته {ref} در {trail}")
            for key, value in node.items():
                walk(value, f"{trail}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{trail}[{index}]")

    walk(spec.get("paths"), "paths")
    walk(schemas, "components/schemas")

    used = set()

    def collect(node):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
                used.add(ref.rsplit("/", 1)[-1])
            for value in node.values():
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    collect(spec.get("paths"))
    collect(schemas)
    for name in sorted(set(schemas) - used):
        warnings.append(f"{label}: مدل {name} به آن ارجاعی نیست")


def check_version(version_dir, quiet):
    label = version_dir.name
    spec_path = version_dir / "openapi.yaml"
    if not spec_path.exists():
        errors.append(f"{label}: openapi.yaml نیست")
        return

    spec = load(spec_path)
    schemas = spec.get("components", {}).get("schemas", {})

    check_codes(label, version_dir, schemas)
    op_ids = check_operations(label, spec)
    check_refs(label, spec, schemas)

    for table_path in sorted((version_dir / "codes").glob("*.yaml")):
        table = load(table_path)
        if table.get("resolved") is False:
            question = table.get("conflict", {}).get("question", "")
            warnings.append(f"{label}: {table_path.name} حل‌نشده است. {question}")

    if not quiet:
        print(f"{label}: {len(spec.get('paths') or {})} مسیر، {len(op_ids)} عملیات، {len(schemas)} مدل")


def main():
    only_gaps = "--gaps" in sys.argv
    strict = "--strict" in sys.argv

    specs = ROOT / "specs"
    versions = sorted(p for p in specs.iterdir() if p.is_dir()) if specs.exists() else []
    if not versions:
        sys.exit("هیچ نسخه‌ای در specs/ نیست")

    for version_dir in versions:
        check_version(version_dir, quiet=only_gaps)

    if only_gaps:
        if not gaps:
            print("هیچ شکاف تأییدنشده‌ای نمانده است.")
            return
        print("شکاف‌های تأییدنشده، برای پیگیری از سمت پنل:")
        print()
        width = max(len(g[1]) for g in gaps)
        for label, what, code, reason in gaps:
            print(f"  {label}  {what.ljust(width)}  {str(code).rjust(3)}   {reason}")
        print()
        print(f"{len(gaps)} مورد")
        return

    for line in warnings:
        print(f"  هشدار  {line}")
    for line in errors:
        print(f"  خطا    {line}")

    print()
    print(f"{len(errors)} خطا، {len(warnings)} هشدار")
    if errors or (strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
