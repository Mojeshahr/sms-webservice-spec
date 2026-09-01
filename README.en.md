<div align="center">

<a href="https://payam-resan.com">
  <img src=".github/assets/logo.svg" width="64" height="64" alt="Payam Resan">
</a>

<h1>Payam Resan SMS web service reference</h1>

The machine readable description of the <a href="https://payam-resan.com"><b>Payam Resan SMS panel</b></a> API<br>
the single source that the documentation, the language examples and the MCP server derive from

[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-0a7cbd)](specs/v3/openapi.yaml)
[![API](https://img.shields.io/badge/API-V3-777bb4)](https://payam-resan.com)
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
└── v3/
    ├── openapi.yaml              the OpenAPI 3.1 description
    └── codes/
        ├── error-codes.yaml      the ErrorCode values
        ├── status-codes.yaml     the StatusCode values
        └── template-status.yaml  the template approval states
scripts/
└── validate.py                   the spec against the tables
```

A version is a folder, not a branch and not a tag. Older versions of the service
are still live and have to be readable next to the current one, so each version
has its own folder, and adding a new version changes no file inside the folders
that already exist.

## What you need to know about the responses

Three behaviours of the service that shape every integration:

| Behaviour | What it means for you |
|---|---|
| Every response is `200` | success is read from the `Success` field, never from the HTTP status |
| `ErrorCode` means something only on failure | until `Success` is `false`, reading it is meaningless |
| The key travels inside the request | a query parameter on `GET`, a body field on `POST`, never a header |

All three are described in full in the `info` section of
[`openapi.yaml`](specs/v3/openapi.yaml).

## Why the code tables live outside the spec

The `ErrorCode` and `StatusCode` values are needed in two places: as an `enum`
in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the numbers stay in the spec, the text lives in `codes/`, and
[`scripts/validate.py`](scripts/validate.py) fails if the two drift apart.

## Coverage

| Table | What it holds |
|---|---|
| [`error-codes.yaml`](specs/v3/codes/error-codes.yaml) | 20 error codes, each with a cause, a remedy and a `retry` class |
| [`status-codes.yaml`](specs/v3/codes/status-codes.yaml) | 22 message states, `0` to `21`, each with a `disposition` |
| [`template-status.yaml`](specs/v3/codes/template-status.yaml) | 3 template approval states |

The `retry` class says whether repeating a request can help, and `disposition`
says when a status polling loop should stop. Both exist so that a program can
decide without guessing.

## Two things your code has to handle

| Detail | What to do |
|---|---|
| The sender field in `GetInbox` | it is named `Form`, not `From`. It is documented exactly that way so your code matches the real response |
| Template status | the panel shows four states and separates two kinds of rejection, but the API returns `3` for both |

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
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml
```

The disabled rules and the reason for each are in
[`redocly.yaml`](redocly.yaml).

## Consumers

| Consumer | What it takes |
|---|---|
| `docs.payam-resan.com` | the API reference pages and the code tables |
| the per-language example repositories | method signatures and field names |
| the MCP server | the tool definitions |

## License

[MIT](LICENSE)

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
