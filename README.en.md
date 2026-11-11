<div align="center">

<a href="https://payam-resan.com">
  <img src=".github/assets/logo.svg" width="64" height="64" alt="Payam Resan">
</a>

<h1>Payam Resan SMS web service reference</h1>

The machine readable description of the <a href="https://payam-resan.com"><b>Payam Resan SMS panel</b></a> API<br>
the single source that the documentation, the language examples and the MCP server derive from

[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-0a7cbd)](specs/v3/openapi.yaml)
[![API](https://img.shields.io/badge/API-V3%20%2B%20V4-777bb4)](https://payam-resan.com)
[![Lint](https://img.shields.io/badge/redocly-clean-2ea44f)](redocly.yaml)
[![License](https://img.shields.io/badge/license-MIT-6e7781)](LICENSE)

<a href="README.md">فارسی</a> · <b>English</b>

</div>

---

This repository is the official machine readable description of the web
service. The documentation at
[`docs.payam-resan.com`](https://docs.payam-resan.com), the examples for every
language and the MCP server are all derived from these files, so that one
question has one answer everywhere.

If you are looking for a guide to read, go to
[`docs.payam-resan.com`](https://docs.payam-resan.com). What lives here is the
description itself, for tools and code generators.

## Layout

```
specs/
├── v3/
│   ├── openapi.yaml              the OpenAPI 3.1 description
│   └── codes/
│       ├── error-codes.yaml      the ErrorCode values
│       ├── status-codes.yaml     the StatusCode values
│       ├── template-status.yaml  the template approval states
│       └── http-status.yaml      HTTP responses for every V3 operation
└── v4/
    ├── openapi.yaml              the published V4 operations and models
    └── codes/                   HTTP responses and all six status/error enums
sources/                         Swagger snapshots, hashes and upstream issues
scripts/
├── validate.py                   structure and code-table consistency checks
├── sync_swagger.py               reproducible reconciliation from snapshots
├── validate_swagger.py           operation coverage and schema/example checks
└── validate_readmes.py           Persian first-word checks on every README line
```

A version is a folder, not a branch and not a tag. Older versions of the service
are still live and have to be readable next to the current one, so each version
has its own folder, and adding a new version changes no file inside the folders
that already exist. V3 contains 13 published operations across 11 paths; V4
contains 26 across 24 paths. The former 25 V4 sandbox operations are preserved
in [a historical snapshot](sources/v4/previous-sandbox.json), with an inventory
in the V4 specification. They are absent from public Swagger and were not
retested. Published request and response contracts have been reconciled
independently for each version. Empty descriptions use the published summary
and are marked explicitly. See
[`PUBLISHED-SWAGGER-CHANGES.md`](PUBLISHED-SWAGGER-CHANGES.md) for the full review,
source ambiguities and validation results.

The maintainer-confirmed sandbox bases are
`https://www.payam-resan.com/api/V3SandBox` and
`https://www.payam-resan.com/uapi/v4SandBox`. V4 Swagger still prints an older
base; the correction is recorded separately from the unchanged source capture.
Swagger excludes V4 `SendMultiple` from sandbox. No sandbox operation was tested.

## What the published V4 Swagger describes

The public V4 Swagger documents single and bulk SMS, template messages, SMS and
voice OTP, delivery and account queries, inbox, phonebook management, and
campaign management. Most operations use `POST` with the API key in the JSON
body; two template-send operations also offer `GET` with the key in the query.
Prefer `POST` when possible to avoid exposing the key in URLs. `GetToken`
lists templates; it does not generate a login token. Compared with V3
`TokenList`, it uses camel-case fields, omits `VoiceTemplate`, and distinguishes
template status 4. The exact comparison is in the reconciliation report.

The Swagger declares `200`, `429`, and `default` responses for V4 operations.
These response codes and shapes are documented claims, not independently
verified runtime behavior. V3 now records the same HTTP response declarations. Check the response
envelope only when present; a transport/server failure may use another shape.

## What you need to know about V3 responses

Three published V3 declarations that shape an integration:

| Behaviour | What it means for you |
|---|---|
| Swagger publishes `200`, `429`, and `default` | HTTP 200 alone does not imply success; inspect `Success`. Other HTTP errors may have another response shape |
| `ErrorCode` means something only on failure | until `Success` is `false`, reading it is meaningless |
| The key travels inside the request | a query parameter on `GET`, a body field on `POST`, never a header |

V3 contains 13 published operations across 11 paths, including GET and POST
`SendTokenSingleConcatParam`. An optional `source-app` header attributes calls
to an application; it is not a credential. `POST /api/V3/TokenList` accepts
a JSON body containing `ApiKey` and lists templates with `Key`, `TextTemplate`,
`VoiceTemplate`, and `Status` fields.

All three V3 declarations are described in full in the `info` section of
[`openapi.yaml`](specs/v3/openapi.yaml).

## Why the V3 code tables live outside the spec

The V3 `ErrorCode` and `StatusCode` values are needed in two places: as an
`enum` in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the V3 numbers stay in the spec, the text lives in `specs/v3/codes/`, and
[`scripts/validate.py`](scripts/validate.py) fails if the two drift apart.

## V3 and V4 code-table coverage

| Table | What it holds |
|---|---|
| [`error-codes.yaml`](specs/v3/codes/error-codes.yaml) | 20 error codes, each with a cause, a remedy and a `retry` class |
| [`status-codes.yaml`](specs/v3/codes/status-codes.yaml) | 22 message states, `0` to `21`, each with a `disposition` |
| [`template-status.yaml`](specs/v3/codes/template-status.yaml) | 3 template approval states |
| [V3 HTTP responses](specs/v3/codes/http-status.yaml) | Per-operation responses for all 13 operations |
| [V4 HTTP responses](specs/v4/codes/http-status.yaml) | Per-operation responses for all 26 operations: `200`, `429`, `default` |
| [V4 error codes](specs/v4/codes/error-codes.yaml) | 24 published error codes and labels |
| [V4 delivery statuses](specs/v4/codes/status-codes.yaml) | 22 message delivery statuses, 0–21 |
| [V4 template states](specs/v4/codes/template-status.yaml) | 4 states, including permanently rejected (4) |
| [V4 campaign progress](specs/v4/codes/campaign-status.yaml) | 6 progress states, 0–5 |
| [V4 campaign filters](specs/v4/codes/campaign-filter-status.yaml) | 3 filter values, 1–3 |
| [V4 campaign recipient statuses](specs/v4/codes/campaign-recipient-status.yaml) | 32 statuses, separate from message delivery-query codes |

The table text follows the captured Swagger. Supplementary guidance and prior
provider observations retain their historical provenance; they were not
retested against the service during this reconciliation.

The `retry` class says whether repeating a request can help, and `disposition`
says when a status polling loop should stop. Both exist so that a program can
decide without guessing.

HTTP status, API error codes and delivery statuses are different namespaces.
`default` is not a numeric HTTP status. Swagger does not name the HTTP 429
retry header or provide its body schema. Unpublished V4 retry, polling and
sendability policies remain `null` with notes; they are not copied from V3.
Swagger-only rows remain unconfirmed by independent service observation and
produce explicit validation warnings.

## Two things your code has to handle

| Detail | What to do |
|---|---|
| The sender field in V3 `GetInbox` | it is named `Form`, not `From`. It is documented exactly that way so your code matches the real response |
| V3 template status | Swagger publishes three values; older panel distinctions remain historical evidence in the table |

## Validation

Two independent checks, and both have to be green.

**1. The spec against the code tables.** The only dependency is `PyYAML`.

```bash
python3 scripts/validate.py            # check and report
python3 scripts/validate.py --gaps     # list the gaps only
python3 scripts/validate.py --strict   # treat warnings as failures
```

**2. The OpenAPI document itself.** With Docker, nothing to install.

```bash
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

Docker can be replaced by Podman. With the image already downloaded, use
`podman run --rm --pull=never --network=none` with the same mount and arguments.

Check source agreement and every explicit example (PyYAML and jsonschema):

```bash
python3 scripts/sync_swagger.py v3 --check
python3 scripts/sync_swagger.py v4 --check
python3 scripts/validate_swagger.py v3 v4
python3 scripts/validate_readmes.py
```

Three V4 campaign success examples have invalid timezone-free `date-time`
values in Swagger. Their originals remain in `x-invalid-source-examples` and
the captured source; no guessed timestamps are presented as valid examples.

The disabled rules and the reason for each are in
[`redocly.yaml`](redocly.yaml).

## Consumers

| Consumer | What it takes |
|---|---|
| `docs.payam-resan.com` | the API reference pages and the code tables |
| the per-language example repositories | method signatures and field names |
| the MCP server | the tool definitions |

## Documentation and support

The full guide to the web service is at
[docs.payam-resan.com](https://docs.payam-resan.com).

Question or bug? [Open an issue](https://github.com/Mojeshahr/sms-webservice-spec/issues)
or contact [support](https://payam-resan.com).

## License

Released under the MIT license. Full text in [`LICENSE`](LICENSE).

<br>
<div align="center">
  <sub>
    <img src=".github/assets/logo.svg" width="16" height="16" alt="" align="top">
    &nbsp;<b>Payam Resan SMS panel - Moje Shahr</b>&nbsp;
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/mojeshahr-dark.svg">
      <img src=".github/assets/mojeshahr-light.svg" width="16" height="16" alt="" align="top">
    </picture>
  </sub>
  <br>
  <sub>
    <a href="https://payam-resan.com">payam-resan.com</a>
    &nbsp;·&nbsp;
    <a href="https://mojeshahr.ir">mojeshahr.ir</a>
  </sub>
</div>
