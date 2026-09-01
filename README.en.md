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

This repository is the **source of truth**. The documentation at
`docs.payam-resan.com`, the examples for every language and the MCP server are
all derived from it. None of them is kept in step with the service by hand,
because that turns one API change into dozens of scattered edits and a slow,
silent drift.

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
gets its own folder and the validator checks all of them together. Adding a
version means adding a folder and touching nothing that already exists.

## Why the code tables live outside the spec

The `ErrorCode` and `StatusCode` values are needed in two places: as an `enum`
in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the numbers stay in the spec, the text lives in `codes/`, and
[`scripts/validate.py`](scripts/validate.py) fails if the two drift apart.

## Running the checks

Two independent checks, and both have to be green.

**1. The spec against the code tables.** The only dependency is `PyYAML`.

```bash
python3 scripts/validate.py            # check and report
python3 scripts/validate.py --gaps     # list the gaps only, for follow up
python3 scripts/validate.py --strict   # treat warnings as failures
```

**2. The OpenAPI document itself.** With Docker, nothing to install.

```bash
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml
```

The two disabled rules and the reason for each are in
[`redocly.yaml`](redocly.yaml).

## Coverage

Nothing is left open. Every code the service declares has a name, a
description, a cause and a remedy, and none of them was filled in by guessing.

| Table | Coverage | How it was confirmed |
|---|---|---|
| Error codes | 20 existing codes, each with a `retry` class | the service team |
| SMS status | 22 codes, `0` to `21`, each with a `disposition` | the service team, code `8` against a live response |
| Template status | 3 codes, all three measured against a live `TokenList` | panel compared with the API |

Three things the retired public list did not have, documented here:

- the `GetInbox` method and the `POST` variant of `SendTokenSingle`
- error codes `16` to `20` and `100`, and status codes `18` to `21`
- error code `7`, which was removed and is no longer returned

Two inconsistencies are recorded exactly as they are, because they live in the
service, and correcting them here would separate the generated code from the
real response:

| Inconsistency | Detail |
|---|---|
| Misspelling | the sender field in `GetInbox` is named `Form`, not `From` |
| Template status | the panel has four states and distinguishes two kinds of rejection, but the API returns `3` for both |

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
