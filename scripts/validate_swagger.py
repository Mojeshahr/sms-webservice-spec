#!/usr/bin/env python3
"""Check snapshot coverage, source hashes, references, and every explicit example.

Requires PyYAML and jsonschema. Does not call an API or infer live behavior.
"""

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

import jsonschema
import yaml

from sync_swagger import ROOT, convert_nullable, read_source

METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
FORMATS = jsonschema.FormatChecker()


@FORMATS.checks("date-time", raises=(ValueError, TypeError))
def rfc3339_datetime(value):
    """Require timezone even when jsonschema's optional format extras are absent."""
    if not isinstance(value, str):
        return True
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})", value):
        return False
    # RFC 3339 permits a leap second. Validate the calendar using second 59.
    calendar_value = re.sub(r"([Tt]\d{2}:\d{2}):60", r"\1:59", value)
    parsed = datetime.datetime.fromisoformat(calendar_value.upper().replace("Z", "+00:00"))
    return parsed.utcoffset() is not None


def operations(document):
    return {
        (path, method): op
        for path, item in document["paths"].items()
        for method, op in item.items()
        if method in METHODS
    }


ANNOTATIONS = {"description", "title", "example", "examples", "default", "deprecated"}


def contract(schema, document):
    """Expand aliases and compare actual schema constraints, not component names."""
    if isinstance(schema, list):
        return [contract(v, document) for v in schema]
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        target = document
        for key in schema["$ref"][2:].split("/"):
            target = target[key.replace("~1", "/").replace("~0", "~")]
        base = contract(target, document)
        return {**base, **contract({k: v for k, v in schema.items() if k != "$ref"}, document)}
    node = {
        k: ({name: contract(value, document) for name, value in v.items()}
            if k == "properties" else contract(v, document))
        for k, v in schema.items()
        if k not in ANNOTATIONS and not k.startswith("x-")
    }
    if "allOf" in node:
        members = node["allOf"]
        allowed = {"type", "properties", "required"}
        if all(m.get("type") == "object" and set(m) <= allowed for m in members):
            props = {}
            required = set()
            for member in members:
                for key, value in member.get("properties", {}).items():
                    if key in props and props[key] != value:
                        raise ValueError(f"Incompatible shared field: {key}")
                    props[key] = value
                required.update(member.get("required", []))
            node.pop("allOf")
            closed = node.pop("unevaluatedProperties", None) is False
            node = {"type": "object", "properties": props, **node}
            if required:
                node["required"] = sorted(required)
            if closed:
                node["additionalProperties"] = False
    return node


def compare_contracts(source, document, prefix, version):
    """Check all published input/output constraints independently of generation."""
    errors = []
    for (path, method), original in operations(source).items():
        op = document["paths"].get(path.removeprefix(prefix), {}).get(method)
        if op is None:
            continue  # The exact coverage check reports this.
        where = f"{version}: {method.upper()} {path}"
        left = {(p["in"], p["name"]): p for p in original.get("parameters", [])}
        right = {(p["in"], p["name"]): p for p in op.get("parameters", [])}
        if left.keys() != right.keys():
            errors.append(where + ": parameter names or locations differ")
        for key in left.keys() & right.keys():
            if left[key].get("required", False) != right[key].get("required", False):
                errors.append(where + f": {key} required declaration differs")
            if contract(left[key].get("schema", {}), source) != contract(right[key].get("schema", {}), document):
                errors.append(where + f": {key} parameter schema differs")
        if original.get("requestBody", {}).get("required", False) != op.get("requestBody", {}).get("required", False):
            errors.append(where + ": request body requirement differs")
        if original["responses"].keys() != op["responses"].keys():
            errors.append(where + ": response codes differ")
        pairs = [("request", original.get("requestBody", {}), op.get("requestBody", {}))]
        pairs.extend(("response " + code, response, op["responses"].get(code, {})) for code, response in original["responses"].items())
        for label, before, after in pairs:
            if before.get("headers", {}) != after.get("headers", {}):
                errors.append(where + ": " + label + " headers differ")
            if before.get("content", {}).keys() != after.get("content", {}).keys():
                errors.append(where + ": " + label + " content types differ")
            for media, value in before.get("content", {}).items():
                target = after.get("content", {}).get(media, {})
                if contract(value.get("schema", {}), source) != contract(target.get("schema", {}), document):
                    errors.append(where + ": " + label + " " + media + " schema constraints differ")
    return errors


def validate_examples(document, label, known_issues=()):
    resolver = jsonschema.RefResolver.from_schema(document)
    checked = 0
    errors = []
    recognized_issues = set()

    def example(schema, value, location):
        nonlocal checked
        checked += 1
        validator = jsonschema.Draft202012Validator(
            schema, resolver=resolver, format_checker=FORMATS
        )
        failures = list(validator.iter_errors(value))
        if failures:
            digest = hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            for issue in known_issues:
                if location == issue["location"] and digest == issue["example_sha256"]:
                    print(f"UPSTREAM ISSUE: {label}: {location}: {issue['reason']}")
                    recognized_issues.add(location)
                    return
        for error in failures:
            errors.append(f"{label}: {location}: {list(error.path)}: {error.message}")

    def schema_examples(schema, location):
        if not isinstance(schema, dict):
            return
        if "example" in schema:
            example(schema, schema["example"], location + "/example")
        for i, value in enumerate(schema.get("examples", [])):
            example(schema, value, location + f"/examples/{i}")
        for name, child in schema.get("properties", {}).items():
            schema_examples(child, location + "/properties/" + name)
        if isinstance(schema.get("items"), dict):
            schema_examples(schema["items"], location + "/items")
        for keyword in ("allOf", "anyOf", "oneOf"):
            for i, child in enumerate(schema.get(keyword, [])):
                schema_examples(child, location + f"/{keyword}/{i}")

    def content(media, location):
        schema = media.get("schema", {})
        schema_examples(schema, location + "/schema")
        if "example" in media:
            example(schema, media["example"], location + "/example")
        for name, item in media.get("examples", {}).items():
            if "value" in item:
                example(schema, item["value"], location + "/examples/" + name)
            else:
                errors.append(f"{label}: {location}/{name}: external example cannot be checked offline")

    for (path, method), op in operations(document).items():
        where = method.upper() + " " + path
        for parameter in op.get("parameters", []):
            content(parameter, where + "/parameter/" + parameter["name"])
        for media_type, media in op.get("requestBody", {}).get("content", {}).items():
            content(media, where + "/request/" + media_type)
        for status, response in op.get("responses", {}).items():
            for media_type, media in response.get("content", {}).items():
                content(media, where + "/response/" + str(status) + "/" + media_type)
    for name, schema in document.get("components", {}).get("schemas", {}).items():
        jsonschema.Draft202012Validator.check_schema(schema)
        schema_examples(schema, "components/schemas/" + name)

    def references(node, location):
        if isinstance(node, dict):
            if "$ref" in node:
                ref = node["$ref"]
                if not ref.startswith("#/"):
                    errors.append(f"{label}: external reference {ref} at {location}")
                else:
                    target = document
                    try:
                        for key in ref[2:].split("/"):
                            target = target[key.replace("~1", "/").replace("~0", "~")]
                    except (KeyError, TypeError):
                        errors.append(f"{label}: broken reference {ref} at {location}")
            for key, value in node.items():
                references(value, location + "/" + key)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                references(value, location + f"/{i}")

    references(document, "")
    for issue in known_issues:
        if issue["location"] not in recognized_issues:
            errors.append(f"{label}: recorded upstream issue no longer reproduces: {issue['location']}")
    return checked, errors


def check_version(version):
    source, provenance = read_source(version)
    document = yaml.safe_load((ROOT / "specs" / version / "openapi.yaml").read_text())
    prefix = "/api/V3" if version == "v3" else "/uapi/v4"
    expected = {(p.removeprefix(prefix), m) for p, m in operations(source)}
    actual = set(operations(document))
    errors = []
    if expected != actual:
        errors.append(f"{version}: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    errors.extend(compare_contracts(convert_nullable(source), document, prefix, version))
    issues_path = ROOT / "sources" / version / "issues.json"
    issues = json.loads(issues_path.read_text())["invalid_examples"] if issues_path.exists() else []
    source_count, source_errors = validate_examples(convert_nullable(source), version + " source", issues)
    document_count, document_errors = validate_examples(document, version + " spec")
    errors.extend(source_errors + document_errors)
    print(f"{version}: {len(expected)} published operations; {source_count} source and {document_count} spec examples checked")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("versions", nargs="*", choices=["v3", "v4"])
    args = parser.parse_args()
    versions = args.versions or [p.name for p in sorted((ROOT / "sources").iterdir()) if p.is_dir()]
    errors = []
    for version in versions:
        errors.extend(check_version(version))
    for error in errors:
        print(error)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
