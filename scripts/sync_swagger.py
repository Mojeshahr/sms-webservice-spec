#!/usr/bin/env python3
"""Reconcile captured official Swagger into the versioned OpenAPI descriptions.

Offline by design: source URLs, dates and hashes live beside each snapshot.
Existing V3 operation IDs, schema aliases and navigation groups remain stable.
"""

import argparse
import copy
import hashlib
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REF = "#/components/schemas/"
V3_ALIASES = {
    "LegacyApiErrorType": "ErrorCode",
    "LegacySendResponseRecipient": "SentMessage",
    "LegacyApiResponseOfIEnumerableOfLegacySendResponseRecipient": "SendResponse",
    "LegacySendBulkRequest": "SendBulkRequest",
    "LegacySendBulkRecipient": "SendBulkRecipient",
    "LegacySendMultipleRequest": "SendMultipleRequest",
    "LegacySendMultipleRecipient": "SendMultipleRecipient",
    "LegacyApiResponseOfIEnumerableOfLegacyOtpResponseRecipient": "TokenResponse",
    "LegacyOtpResponseRecipient": "TokenSentMessage",
    "LegacyOtpSingleRequest": "SendTokenSingleRequest",
    "LegacyOtpSingleConcatRequest": "SendTokenSingleConcatParamRequest",
    "LegacyOtpRequest": "SendTokenMultiRequest",
    "LegacyOtpRequestItem": "TokenRecipient",
    "LegacyApiResponseOfIEnumerableOfLegacyTokenListDetail": "TokenListResponse",
    "LegacyTokenListDetail": "TokenListDetail",
    "LegacyTokenListRequest": "ApiKeyOnlyRequest",
    "LegacyAccountInfoRequest": "ApiKeyOnlyRequest",
    "LegacyGetInboxRequest": "ApiKeyOnlyRequest",
    "LegacyApiResponseOfIEnumerableOfLegacyStatusResponseItem": "StatusResponse",
    "LegacyStatusResponseItem": "StatusItem",
    "LegacyStatusByIdRequest": "StatusByIdRequest",
    "LegacyStatusByUserTraceIdRequest": "StatusByUserTraceIdRequest",
    "LegacyApiResponseOfLegacyAccountDetail": "AccountInfoResponse",
    "LegacyAccountDetail": "AccountDetail",
    "LegacyApiResponseOfIEnumerableOfLegacyInboxResponseItem": "InboxResponse",
    "LegacyInboxResponseItem": "InboxItem",
}
V3_GROUPS = {
    "ارسال پیامک": "ارسال",
    "کد تأیید و الگوها": "قالب",
    "گزارش تحویل": "گزارش",
    "اطلاعات حساب": "حساب",
    "صندوق دریافت": "دریافت",
}


class Dumper(yaml.SafeDumper):
    pass


def represent_string(dumper, value):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", value, style="|" if "\n" in value else None
    )


Dumper.add_representer(str, represent_string)


def convert_nullable(value):
    """Translate OAS 3.0 nullable schemas to OAS 3.1 without dropping constraints."""
    if isinstance(value, list):
        return [convert_nullable(v) for v in value]
    if not isinstance(value, dict):
        return value
    node = {k: convert_nullable(v) for k, v in value.items() if k != "nullable"}
    # NSwag emits oneOf with a single reference. It is equivalent to that
    # reference (with OAS 3.1 siblings), and otherwise triggers a lint warning.
    if len(node.get("oneOf", [])) == 1:
        only = node.pop("oneOf")[0]
        node = {**only, **node}
    if value.get("nullable"):
        if isinstance(node.get("type"), str):
            node["type"] = [node["type"], "null"]
        else:
            annotations = {k: node.pop(k) for k in ("description", "example") if k in node}
            node = {**annotations, "anyOf": [node, {"type": "null"}]}
    return node


def read_source(version):
    directory = ROOT / "sources" / version
    raw = (directory / "swagger.json").read_bytes()
    provenance = json.loads((directory / "provenance.json").read_text())
    if hashlib.sha256(raw).hexdigest() != provenance["sha256"]:
        raise ValueError(f"{version}: source snapshot hash mismatch")
    return json.loads(raw), provenance


def sandbox_servers():
    return json.loads((ROOT / "sources" / "sandbox-servers.json").read_text())


def v3_document(source, provenance):
    source = convert_nullable(source)
    original_schemas = source["components"]["schemas"]
    inline = {"LegacyApiMessageStatus", "LegacyTokenListDetailStatus"}

    def remap(value):
        if isinstance(value, list):
            return [remap(v) for v in value]
        if not isinstance(value, dict):
            return value
        node = {k: remap(v) for k, v in value.items() if k != "$ref"}
        if "$ref" in value:
            name = value["$ref"].removeprefix(REF)
            if name in inline:
                return {**remap(original_schemas[name]), **node}
            node["$ref"] = REF + V3_ALIASES[name]
        return node

    schemas = {}
    for original, value in original_schemas.items():
        if original in inline:
            continue
        alias = V3_ALIASES[original]
        converted = remap(value)
        if alias in schemas and schemas[alias] != converted:
            raise ValueError(f"Cannot combine unequal source schemas into {alias}")
        schemas[alias] = converted

    # Keep the existing shared key and response-envelope components.
    key_schema = copy.deepcopy(schemas["SendBulkRequest"]["properties"]["ApiKey"])
    for schema in schemas.values():
        if "ApiKey" in schema.get("properties", {}):
            if schema["properties"]["ApiKey"] != key_schema:
                raise ValueError("Source ApiKey declarations differ")
            schema["properties"]["ApiKey"] = {"$ref": REF + "ApiKey"}
    schemas["ApiKey"] = key_schema
    envelope_properties = {
        k: copy.deepcopy(schemas["SendResponse"]["properties"][k])
        for k in ("Success", "ErrorCode", "Error")
    }
    schemas["ResponseEnvelope"] = {"type": "object", "properties": envelope_properties}
    for name in ("SendResponse", "TokenResponse", "TokenListResponse", "StatusResponse", "AccountInfoResponse", "InboxResponse"):
        schema = schemas[name]
        if schema.pop("additionalProperties") is not False:
            raise ValueError("Unexpected response openness")
        for field, value in envelope_properties.items():
            if schema["properties"].pop(field) != value:
                raise ValueError("Source response envelopes differ")
        schemas[name] = {
            "description": schema["description"],
            "allOf": [{"$ref": REF + "ResponseEnvelope"}, {"type": "object", "properties": schema["properties"]}],
            "unevaluatedProperties": False,
        }

    paths = {}
    for source_path, item in source["paths"].items():
        path = source_path.removeprefix("/api/V3")
        paths[path] = {}
        for method, operation in item.items():
            op = remap(operation)
            name = path.lstrip("/")
            op["x-source-operation-id"] = op["operationId"]
            op["operationId"] = name + ("ByQuery" if method == "get" and name != "Send" else "")
            op["x-source-tags"] = op["tags"]
            op["tags"] = [V3_GROUPS[t] for t in op["tags"]]
            if not op.get("description"):
                op["description"] = op["summary"]
                op["x-description-source"] = "summary; published description is empty"
            paths[path][method] = op

    info = copy.deepcopy(source["info"])
    info["contact"] = {"name": "پشتیبانی پنل پیامکی پیام رسان", "url": "https://payam-resan.com"}
    info["license"] = {"name": "MIT", "identifier": "MIT"}
    info["description"] += (
        "\n\nاین فایل با Swagger رسمی تطبیق داده شده است؛ درخواست‌ها و پاسخ‌های نمونه "
        "از همان سند آمده‌اند و در این مرحله با سرویس زنده آزموده نشده‌اند. "
        "اعلان‌های required و nullable عین قرارداد منتشرشده حفظ شده‌اند؛ "
        "تعارض متن با اسکیما و نام نامشخص GetToken در گزارش تطبیق ثبت شده است."
    )
    return {
        "openapi": "3.1.0",
        "x-generator": source.get("x-generator"),
        "info": info,
        "externalDocs": {"url": "https://www.payam-resan.com/api/V3/", "description": "راهنمای Swagger رسمی نسخه ۳"},
        "x-source": {**provenance, "snapshot": "../../sources/v3/swagger.json", "verification": "published-swagger-only"},
        "x-sandbox-source": {"path": "../../sources/sandbox-servers.json", "verification": sandbox_servers()["verification"]},
        "servers": [
            {"url": "https://www.payam-resan.com/api/V3", "description": "سرور عملیاتی طبق مسیرهای Swagger"},
            {"url": sandbox_servers()["v3"], "description": "پایه آزمایشی با تأیید نگهدارنده؛ عملیات آن در این مرحله آزموده نشده‌اند"},
        ],
        "tags": [{"name": v, "description": k} for k, v in V3_GROUPS.items()],
        "paths": paths,
        "components": {"schemas": schemas},
    }


def v4_document(source, provenance):
    document = convert_nullable(source)
    # The maintainer corrected the published sandbox base. Preserve the raw
    # Swagger capture, but do not repeat its obsolete URL as current guidance.
    document["info"]["description"] = document["info"]["description"].replace(
        "`/uapi/v4/sandbox`", "`/uapi/v4SandBox`"
    )
    document["openapi"] = "3.1.0"
    document["info"]["contact"] = {"name": "پشتیبانی پنل پیامکی پیام رسان", "url": "https://payam-resan.com"}
    document["info"]["license"] = {"name": "MIT", "identifier": "MIT"}
    document["info"]["description"] += (
        "\n\nاین توصیف فقط عملیات منتشرشده در Swagger رسمی را پوشش می‌دهد. "
        "درخواست‌ها و پاسخ‌های نمونه از همان سند هستند و با سرویس زنده آزموده نشده‌اند. "
        "نام فیلدها و حروف بزرگ و کوچک آن‌ها مطابق اسکیما و پارامترهای منتشرشده است. "
        "تعریف‌های پیشین sandbox که در Swagger عمومی نیستند، به‌عنوان شاهد تاریخی "
        "در sources/v4/previous-sandbox.json نگه داشته شده‌اند؛ وضعیت فعلی آن‌ها تأیید نشده است."
    )
    document["externalDocs"] = {"url": provenance["ui_url"], "description": "راهنمای Swagger رسمی نسخه ۴"}
    document["x-source"] = {**provenance, "snapshot": "../../sources/v4/swagger.json", "verification": "published-swagger-only"}
    document["x-sandbox-source"] = {"path": "../../sources/sandbox-servers.json", "verification": sandbox_servers()["verification"]}
    archive = ROOT / "sources" / "v4" / "previous-sandbox.json"
    archived = json.loads(archive.read_text())
    document["x-unpublished-sandbox"] = {
        "snapshot": "../../sources/v4/previous-sandbox.json",
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "origin": archived["x-origin"],
        "verification": "historical definitions only; absent from current public Swagger; not retested",
        "operations": [
            {"path": p, "method": m, "operationId": o["operationId"]}
            for p, item in archived["paths"].items() for m, o in item.items()
        ],
    }
    production = {"url": "https://www.payam-resan.com/uapi/v4", "description": "سرور عملیاتی نسخه ۴؛ مسیرها نسبت به این پایه هستند"}
    document["servers"] = [
        production,
        {"url": sandbox_servers()["v4"], "description": "پایه آزمایشی با تأیید نگهدارنده؛ عملیات آن در این مرحله آزموده نشده‌اند"},
    ]
    document["paths"] = {p.removeprefix("/uapi/v4"): item for p, item in document["paths"].items()}
    # Swagger explicitly excludes SendMultiple from sandbox. A server override
    # prevents generators from offering that operation on the sandbox base.
    document["paths"]["/SendMultiple"]["post"]["servers"] = [copy.deepcopy(production)]
    groups = {}
    for item in document["paths"].values():
        for operation in item.values():
            for tag in operation["tags"]:
                groups[tag] = {"name": tag, "description": tag}
            if not operation.get("description"):
                operation["description"] = operation["summary"]
                operation["x-description-source"] = "summary; published description is empty"
    document["tags"] = list(groups.values())
    issues_path = ROOT / "sources" / "v4" / "issues.json"
    issues = json.loads(issues_path.read_text())
    for issue in issues["invalid_examples"]:
        path = issue["path"].removeprefix("/uapi/v4")
        response = document["paths"][path][issue["method"]]["responses"][issue["status"]]
        media = response["content"][issue["media_type"]]
        example = media["examples"].pop(issue["example"])
        digest = hashlib.sha256(json.dumps(example["value"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if digest != issue["example_sha256"]:
            raise ValueError("Upstream invalid example changed; review the issue before regenerating")
        media.setdefault("x-invalid-source-examples", {})[issue["example"]] = {
            "original": example,
            "reason": issue["reason"],
            "field": issue["field"],
        }
        response["description"] += (
            " نمونه موفق منتشرشده زمان بدون منطقه زمانی دارد و با قالب date-time سازگار نیست؛ "
            "اصل آن در x-invalid-source-examples نگه داشته شده است. "
            "تا روشن شدن قالب زمان، از آن به‌عنوان نمونه معتبر استفاده نکنید."
        )
    document["x-source"]["issues"] = "../../sources/v4/issues.json"
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=["v3", "v4"])
    parser.add_argument("--check", action="store_true", help="fail on drift without writing")
    args = parser.parse_args()
    source, provenance = read_source(args.version)
    document = (v3_document if args.version == "v3" else v4_document)(source, provenance)
    destination = ROOT / "specs" / args.version / "openapi.yaml"
    if args.check:
        if yaml.safe_load(destination.read_text()) != document:
            sys.exit(f"{args.version}: specification differs from the captured Swagger reconciliation")
        print(f"{args.version}: captured Swagger and specification agree")
    else:
        destination.write_text(yaml.dump(document, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")


if __name__ == "__main__":
    main()
