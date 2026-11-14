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

We own and develop the Payam Resan SMS web service. This repository is our
authoritative machine-readable API reference. Our documentation site, language
examples, client generators and MCP server consume these contracts. Our product
and engineering teams are responsible for keeping them consistent with the service.

## Layout

```text
specs/
├── v3/
│   ├── openapi.yaml
│   └── codes/
└── v4/
    ├── openapi.yaml
    └── codes/
scripts/
└── validate.py
```

[V3](specs/v3/openapi.yaml) contains 13 operations across 11 paths;
[V4](specs/v4/openapi.yaml) contains 26 operations across 24 paths.
Each version has its own folder. Adding a version does not move or rename
existing version files.

OpenAPI definitions and code tables are maintained directly under `specs/`.
Changes must preserve each version's verified technical information.

## Contract evidence

V3 combines the development team's approved reference with additive Swagger
information. Descriptions, errors, retry and polling policies are preserved
in [the V3 reference](specs/v3/openapi.yaml).
An omission in Swagger is not a reason to remove approved information.
V4 uses the same documentation structure with independently verified V4 details.
V3 behavior is not copied into V4 without confirmation.

Our confirmed sandbox bases are:

- V3: `https://www.payam-resan.com/api/V3SandBox`
- V4: `https://www.payam-resan.com/uapi/v4SandBox`

Our published contract excludes V4 `SendMultiple` from sandbox.

## V4 contract

V4 covers single and bulk SMS, template sending, SMS and voice OTP, delivery
and account queries, inbox, phonebook management and campaigns. Most operations
use POST; two template-send operations also offer GET. The API key travels
in JSON or query parameters. The optional `source-app` header attributes calls.

`POST /uapi/v4/GetToken` accepts `{"apiKey":"YOUR_API_KEY"}` and lists
templates and their approval states. It does not issue login tokens.
The key must be a non-null string. Its response fields are `success`,
`errorCode`, `error`, `moreInfo` and `result`. Template items contain `key`,
`textTemplate` and `status`, with no voice-template property. There are four
template states, including `RejectedPermanently` (4).

V4 timestamps are timezone-free Tehran local time, based on `UTC+03:30`.
Fields with `format: date-time-local` use `YYYY-MM-DDTHH:mm:ss` with an
optional fractional second and no timezone suffix. Campaign examples retain
this wire format.

Following comparison of functionality and code meanings, the approved V3
policies provide the V4 reference for 19 equivalent errors, all 22 delivery
states, batch polling at intervals of a few minutes, and sending only approved
templates. V4 exposes permanent template rejection separately as state `4`.
V4 API error `20` means an OTP quota limit; HTTP rate limiting uses `429`.
The V4 code tables record the source of each policy.

## What you need to know about V3 responses

Three V3 behaviours of the service that shape every integration:

| Behaviour | What it means for you |
|---|---|
| Every response is `200` | success is read from the `Success` field, never from the HTTP status |
| `ErrorCode` means something only on failure | until `Success` is `false`, reading it is meaningless |
| The key travels inside the request | a query parameter on `GET`, a body field on `POST`, never a header |

All three V3 behaviours are described in full in the `info` section of
[`openapi.yaml`](specs/v3/openapi.yaml).

## Why the V3 code tables live outside the spec

The V3 `ErrorCode` and `StatusCode` values are needed in two places: as an
`enum` in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the V3 numbers stay in the spec, the text lives in `specs/v3/codes/`, and
[`scripts/validate.py`](scripts/validate.py) fails if the two drift apart.

## V3 code-table coverage

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
| The sender field in V3 `GetInbox` | it is named `Form`, not `From`. It is documented exactly that way so your code matches the real response |
| V3 template status | the panel shows four states and separates two kinds of rejection, but the API returns `3` for both |

## Added V3 operations

`SendTokenSingleConcatParam` has GET and POST operations.
Template values travel in one `p` string, separated by `;`.
POST takes the key and values in the JSON body. These additions are extracted
from V3 Swagger; existing V3 methods remain unchanged.

## V4 code-table coverage

| Table | Contents |
| --- | --- |
| [V4 HTTP responses](specs/v4/codes/http-status.yaml) | 26 operations |
| [V4 errors](specs/v4/codes/error-codes.yaml) | 24 codes |
| [V4 delivery](specs/v4/codes/status-codes.yaml) | 22 states |
| [V4 templates](specs/v4/codes/template-status.yaml) | 4 states |
| [Campaign progress](specs/v4/codes/campaign-status.yaml) | 6 states |
| [Campaign filters](specs/v4/codes/campaign-filter-status.yaml) | 3 values |
| [Campaign recipients](specs/v4/codes/campaign-recipient-status.yaml) | 32 states |

## Validation

Structural, code-table and README formatting checks require PyYAML.

```bash
python3 scripts/validate.py
```

Run the independent OpenAPI check with Redocly:

```bash
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

Podman can replace Docker. With the image already downloaded,
`--pull=never --network=none` permits an offline run.
[Our Redocly configuration](redocly.yaml) records validation rules and exceptions.

## Consumers

| Consumer | Input |
| --- | --- |
| [Our documentation site](https://docs.payam-resan.com) | Reference pages and code tables |
| [Our language example repositories](https://github.com/Mojeshahr) | Method and field contracts |
| MCP server and client generators | Operations, schemas and codes |

## Maintenance

We track contract defects, implementation discrepancies and technical questions
in [Issues](https://github.com/Mojeshahr/sms-webservice-spec/issues).

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
