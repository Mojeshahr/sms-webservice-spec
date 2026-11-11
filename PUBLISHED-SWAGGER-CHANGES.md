# Published Swagger reconciliation

## Scope and evidence

Reconciled on 11 November 2026, starting from repository commit `50f9a72`.
V3 was completed and validated before downloading and inspecting V4.
This repository supplies machine-readable specifications; the readable site
and per-language example repositories are separate consumers and are not
modified by this change. No authenticated API requests, SMS sends, inbox reads,
account queries, or other live-service tests were performed.

- [V3 Swagger UI](https://www.payam-resan.com/api/V3/)
- [V3 OpenAPI JSON](https://www.payam-resan.com/api/V3/swagger.json)
- Exact downloaded bytes: [V3 snapshot](sources/v3/swagger.json)
- Capture date, URL and SHA-256: [V3 provenance](sources/v3/provenance.json)
- Reconciled output: [V3 OpenAPI](specs/v3/openapi.yaml)

The snapshots are the evidence for this review, not substitutes for checking
the provider again at the next update. Swagger declarations and examples are
not proof of observed service behavior. Historical provider/panel observations
in the V3 code tables retain their prior dates and are supplementary guidance,
not newly verified runtime claims.

## V3 result

All **13 published operations across 11 paths** are represented, grouped under
the existing five navigation categories. The previous file had 11 operations
across 10 paths. Published controller class names are unavailable; Swagger
provides operation tags, which are retained as `x-source-tags` alongside the
existing navigation names. Existing local operation IDs and schema aliases
remain stable; `x-source-operation-id` records the provider's identifiers.

| Existing group | Method | Published path |
| --- | --- | --- |
| ارسال | GET | `/api/V3/Send` |
| ارسال | POST | `/api/V3/SendBulk` |
| ارسال | POST | `/api/V3/SendMultiple` |
| قالب | GET | `/api/V3/SendTokenSingle` |
| قالب | POST | `/api/V3/SendTokenSingle` |
| قالب | GET | `/api/V3/SendTokenSingleConcatParam` |
| قالب | POST | `/api/V3/SendTokenSingleConcatParam` |
| قالب | POST | `/api/V3/SendTokenMulti` |
| قالب | POST | `/api/V3/TokenList` |
| گزارش | POST | `/api/V3/StatusById` |
| گزارش | POST | `/api/V3/StatusByUserTraceId` |
| حساب | POST | `/api/V3/AccountInfo` |
| دریافت | POST | `/api/V3/GetInbox` |

The server is `https://www.payam-resan.com/api/V3`, with relative operation
paths. The document's own sandbox-base instruction is represented separately
as `https://www.payam-resan.com/api/V3SandBox`; no sandbox behavior was tested.
Previous hostnames and claims about sandbox-specific responses are no longer
presented as the current production contract.

### Newly introduced method

`SendTokenSingleConcatParam` sends an approved template to one destination,
with ordered values joined by `;` in a single `p` string. It is distinct from
`SendTokenSingle`, which keeps `p1` through `p10`.

| Field | GET location | POST location | Swagger schema |
| --- | --- | --- | --- |
| `ApiKey` | query | JSON field | nullable string; required |
| `TemplateKey` | query | JSON field | nullable string; described as mandatory, but absent from the schema's required list |
| `Destination` | query | JSON field | int64; not formally required |
| `p` | query | JSON field | nullable string; semicolon-separated values; not formally required |
| `source-app` | header | header | optional string, maximum 100 characters; not a credential |

The POST body is required and uses `application/json`. The key needs `Send`
permission and the account's OTP access enabled. Swagger declares no bearer
scheme or token-generation dependency. The published request example uses
`YOUR_API_KEY`, `YOUR_APPROVED_TEMPLATE`, destination `989120000001`, and
`p: "123456;علی"`. These placeholders must be replaced by the integrator.

HTTP 200 contains the V3 envelope (`Success`, nullable `ErrorCode`, nullable
`Error`, and nullable `Result`). Each successful result item declares int64
`Id`, nullable int64 `UserTraceId`, int64 `Sender`, and nullable `FinalText`.
The published request has no `UserTraceId` input, although its success example
returns `10001`; do not infer trace-ID input support from that example.
All published success and failure examples are retained, including invalid
key (1), invalid input (9), and insufficient credit (19).

HTTP 429 describes a retry time in a response header, but does not name or
model that header. `default` warns that transport/server errors may have a
different body. Neither response supplies a schema or example, so none was
invented. Escaping a literal semicolon inside a template value, maximum
parameter length/count, and the handling of missing/extra values are not
specified.

### TokenList: published V3 template-list contract

V3 publishes `POST /api/V3/TokenList` (`LegacyV3_TokenList`). It lists account
templates and their approval status. Its required JSON body contains the
required, nullable `ApiKey` property. The key needs `Send` permission and the
account must have OTP access enabled. The optional `source-app` header is
a string of at most 100 characters, not a credential.

The JSON response uses `Success`, `ErrorCode`, `Error` and nullable `Result`.
Each result item has nullable `Key`, `TextTemplate`, `VoiceTemplate`, and a
`Status` enum: 1 `Pending`, 2 `Approved`, 3 `Rejected`. The published response
properties are not declared required; nullable and optional remain distinct.
HTTP declarations are `200`, `429` and `default`; HTTP 200 still requires
checking `Success`. The latter two have no published body schema, and the
429 description refers to a retry header without naming it.

The updated documentation includes:

- the new production hostname, `source-app`, HTTP 429 and `default`;
- explicit nullable API key (still required), nullable `Key` and `TextTemplate`,
  nullable `VoiceTemplate`, and closed object declarations;
- the published `Send` permission and OTP-access requirement;
- the provider's request, success, invalid-key and invalid-input examples;
- published status labels for codes 1–3, with the previous text retained in
  code-table `previous_fa` fields;
- removal of the old unverified-current claims that TokenList is exempt from
  credit checks or that this host's sandbox returns a particular mock list.

`SendTokenSingle` also retains its GET/POST routes and `p1`–`p10` input names,
while adopting the common response/header/schema changes. Template-key
case-insensitivity and template-to-sender selection details from the previous
prose are not asserted because the current Swagger does not establish them.

### Other V3 differences

- Swagger publishes `200`, `429`, and `default` for every operation. The former
  blanket statement that every HTTP response is 200 has been replaced. HTTP
  200 alone is insufficient; inspect the normal envelope when present.
- Every operation declares optional `source-app` (string, maximum 100).
- Source summaries, descriptions, permissions, content types, request and
  response examples are retained. Four empty descriptions use the published
  summary, explicitly marked by `x-description-source`.
- POST request schemas formally require only `ApiKey`. Previous additional
  required fields, recipient `maxItems: 99`, key-format assumptions,
  and assumptions about absent trace IDs are not imposed on the new contract.
- Required and nullable are independent: required ApiKey may be null according
  to Swagger. That is a declaration inconsistency with authentication prose,
  not a claim that null keys authenticate successfully.
- Nullable strings, arrays, recipient items and trace IDs are represented
  exactly. Objects preserve `additionalProperties: false`. V3 `InboxItem.Id`
  changes from int32 to int64; account credit changes from `double` to the
  source's `decimal` format. No unit conversion was invented.
- Numeric error/status/template enums are unchanged. Published error labels
  differ in punctuation and at codes 11 (`ورودی`, formerly `روردی`) and 100
  (`خطای داخلی سیستم`). Source labels are now recorded with previous text
  retained; this does not claim that live response text was retested.
- The exact inbox field `Form` is preserved. Code 7 remains a historical
  removed error row and retains its existing validator warning.

## Reproduction and V3 validation

The source OpenAPI 3.0 nullable declarations are converted to OpenAPI 3.1
null unions. Single-element `oneOf` wrappers are reduced without changing
validation meaning. Source error/status enums remain synchronized with tables.
The shared V3 key and envelope models and existing public schema aliases are
retained. No linter or validation rule was disabled to pass these checks.

```bash
python3 scripts/sync_swagger.py v3 --check
python3 scripts/validate_swagger.py v3
python3 scripts/validate.py
podman run --rm --pull=never --network=none -v "$PWD:/spec:ro" -w /spec \
  docker.io/redocly/cli:latest lint specs/v3/openapi.yaml
```

`sync_swagger.py v3` regenerates from the captured source; `--check` fails on
drift without writing. The capture hash is checked before either action.
`validate_swagger.py` independently checks exact operation coverage, all
references, JSON Schema declarations, independent input/output constraint
equality against the source (expanding aliases and shared envelopes), and every
explicit request, response,
parameter and schema example in both source and output. It requires PyYAML
and jsonschema. The baseline consistency validator still requires only PyYAML.

V3 validation completed before V4 work: source agreement passed; 13/13
operations covered; 79 source examples and 70 output examples passed schema
validation (shared schemas consolidate repeated schema examples). Redocly
2.77.0 passed without warnings. The baseline validator reports zero errors
and its one existing historical-code warning.

## V4 result

After V3 validation, the V4 UI and its complete OpenAPI document were fetched
independently. Both official UIs returned HTTP 200 and each advertises exactly
one document: `/api/V3/swagger.json` and `/uapi/v4/swagger.json`, respectively.
No alternate document was silently skipped.

- [V4 Swagger UI](https://www.payam-resan.com/uapi/v4)
- [V4 OpenAPI JSON](https://www.payam-resan.com/uapi/v4/swagger.json)
- [Exact V4 snapshot](sources/v4/swagger.json) and [provenance](sources/v4/provenance.json)
- [Reconciled V4 specification](specs/v4/openapi.yaml)
- [Upstream example issues](sources/v4/issues.json)

All **26 published operations across 24 paths**, with all **66 component
schemas**, are represented. The existing V4 file already contained these
production operations and model shapes; this work completes their independent
source reconciliation, provenance, grouping, example checks and treatment of
unpublished routes. It does not claim that 26 previously absent endpoints
were newly invented or that V4 was rebuilt from V3.

The source's seven navigation groups are exposed: campaigns, messaging,
OTP/templates, delivery reports, account, inbox, and phonebook. Production
operation IDs and model names remain unchanged. Four empty descriptions
(`StatusById`, `StatusByUserTraceId`, `GetAccountInfo`, `GetInbox`) explicitly
reuse their published summaries. The source does not publish controller class
metadata beyond operation IDs and tags.

### Complete V4 operation inventory


| Source group | Method | Published path | Request schema |
| --- | --- | --- | --- |
| کمپین | POST | `/uapi/v4/campaign/draft` | `ApiCampaignSubmitRequest` |
| کمپین | POST | `/uapi/v4/campaign/draft/finalize` | `ApiCampaignIdRequest` |
| کمپین | POST | `/uapi/v4/campaign/submit` | `ApiCampaignSubmitRequest` |
| کمپین | POST | `/uapi/v4/campaign/get` | `ApiCampaignIdRequest` |
| کمپین | POST | `/uapi/v4/campaign/search` | `ApiCampaignSearchRequest` |
| کمپین | POST | `/uapi/v4/campaign/recipients` | `ApiCampaignRecipientsRequest` |
| ارسال پیامک | POST | `/uapi/v4/Send` | `SendBulkRequest` |
| ارسال پیامک | POST | `/uapi/v4/SendBulk` | `SendBulkRequest` |
| ارسال پیامک | POST | `/uapi/v4/SendMultiple` | `SendMultipleRequest` |
| کد تأیید و الگوها | POST | `/uapi/v4/SendOtp` | `CodeOtpRequest` |
| کد تأیید و الگوها | POST | `/uapi/v4/SendVoiceOtp` | `VoiceOtpRequest` |
| کد تأیید و الگوها | POST | `/uapi/v4/SendTokenMulti` | `OtpRequest` |
| کد تأیید و الگوها | POST | `/uapi/v4/SendTokenSingle` | `OtpSingleRequest` |
| کد تأیید و الگوها | GET | `/uapi/v4/SendTokenSingle` | `query parameters` |
| کد تأیید و الگوها | GET | `/uapi/v4/SendTokenSingleConcatParam` | `query parameters` |
| کد تأیید و الگوها | POST | `/uapi/v4/SendTokenSingleConcatParam` | `OtpSingleConcatRequest` |
| کد تأیید و الگوها | POST | `/uapi/v4/GetToken` | `TokenListRequest` |
| گزارش تحویل | POST | `/uapi/v4/StatusById` | `StatusByIdRequest` |
| گزارش تحویل | POST | `/uapi/v4/StatusByUserTraceId` | `StatusByUserTraceIdRequest` |
| اطلاعات حساب | POST | `/uapi/v4/GetAccountInfo` | `AccountInfoRequest` |
| صندوق دریافت | POST | `/uapi/v4/GetInbox` | `GetInboxRequest` |
| دفترچه تلفن | POST | `/uapi/v4/phonebook/groups` | `PhonebookGroupsRequest` |
| دفترچه تلفن | POST | `/uapi/v4/phonebook/group` | `CreatePhonebookGroupRequest` |
| دفترچه تلفن | POST | `/uapi/v4/phonebook/group-with-contacts` | `CreatePhonebookGroupWithContactsRequest` |
| دفترچه تلفن | POST | `/uapi/v4/phonebook/contacts` | `UpsertPhonebookContactsRequest` |
| دفترچه تلفن | POST | `/uapi/v4/phonebook/contacts/remove` | `RemovePhonebookContactsRequest` |

### V4 request, response and authentication coverage

The base URL is `https://www.payam-resan.com/uapi/v4`. POST uses required
`application/json` bodies and a required non-null `apiKey` property. The two
GET template variants use a required non-null `ApiKey` query parameter.
`source-app` is optional (maximum 100 characters) on every operation and is
not authentication. No bearer header, OAuth scheme or login-token acquisition
step is declared. Permission notes distinguish `Send`, `SendCampaign`, and
`Phonebook`; template and OTP operations also require account OTP access.
Where the source leaves permissions unspecified, none were invented.

Every operation includes the source's HTTP 200 JSON schema and available
request/response examples, plus HTTP 429 and `default` descriptions. The usual
response fields are `success`, nullable `errorCode`, nullable `error`, nullable
`moreInfo`, and nullable `result`. Unlike a successful HTTP exchange, the
`success` field records API-level success. Transport errors may have a different
shape. A retry response-header name, schema and example are not published.

Messaging responses retain string IDs and nullable string trace IDs, `parts`,
and `credit`. OTP responses add `sender` and `finalText`; the voice description
explains the billing interpretation of parts/pulses. Source descriptions cover
4–8 digit codes (including Persian digits), voice `repeat`, and scheduling.
No numeric code is generated by the documented request: the caller supplies
`code`. A verification/expiry/storage policy is not documented.

Campaign descriptions and schemas preserve draft cost preview, finalization,
one-step submission, search filters, paging, recipient readiness, progress,
net credit and campaign-specific status enums. Phonebook schemas preserve group
creation/listing, bulk contacts, upsert/removal, and per-row error information.
All field names, types, required lists, nullability, enum values, examples,
formats and additional-property policies are taken from the V4 document.
Descriptions do not justify inventing absent `minItems`, `pattern`, or other
machine-enforced constraints.

### GetToken: exact scope and cross-version differences

V4 actually publishes `POST /uapi/v4/GetToken` (`V4_GetToken`). Its purpose is
**template listing**, not API-key creation, JWT issuance or login. In V3 the
corresponding published operation is `POST /api/V3/TokenList`. These are
independently specified contracts; their request and response structures
must not be interchanged.

| Aspect | V3 TokenList | V4 GetToken |
| --- | --- | --- |
| Path | `/api/V3/TokenList` | `/uapi/v4/GetToken` |
| HTTP method/body | POST, required JSON body | POST, required JSON body |
| Key field | required nullable `ApiKey` | required non-null string `apiKey` |
| Credential kind | existing API key | existing API key; no token generation |
| Permission | `Send` and OTP account access | same published requirements |
| Optional attribution header | `source-app`, at most 100 | same |
| Envelope | `Success`, `ErrorCode`, `Error`, `Result` | `success`, `errorCode`, `error`, `result`, plus nullable `moreInfo` |
| Template fields | nullable `Key`, `TextTemplate`, `VoiceTemplate`; `Status` | non-null `key`, `textTemplate`; `status`; no voice-template field |
| Status enum | 1 pending, 2 approved, 3 rejected | also 4 `RejectedPermanently` |
| HTTP responses | 200, 429, default | same declarations |
| Error codes | V3 enum | V4 enum; code 20 has a different meaning and codes 21–24 are added |
| Expiry/refresh/access-token response | not documented | not documented; not this method's purpose |

Compared with the V4 file already in commit `50f9a72`, the current official
GetToken request, response and component schemas are identical after OpenAPI
3.0-to-3.1 normalization. There is no evidence of an additional functional
GetToken change against that baseline. The changes above describe the actual
V3-to-V4 contract differences, not a fabricated change history.

### Unpublished sandbox definitions

The maintainer confirmed these sandbox bases on 11 November 2026:

- V3: `https://www.payam-resan.com/api/V3SandBox`
- V4: `https://www.payam-resan.com/uapi/v4SandBox`

The confirmation is recorded in [sandbox-servers.json](sources/sandbox-servers.json).
V4 Swagger still prints `/uapi/v4/sandbox`; that obsolete guidance is corrected
in the generated description and server list without editing the raw capture.
The `x-sandbox-source` extension identifies this additional evidence. The V4
`SendMultiple` operation overrides the server list to production only, because
Swagger explicitly excludes it from sandbox. Address confirmation does not
verify individual operation availability or response behavior.

Public V4 Swagger advertises the older sandbox base in prose and explicitly excludes
`SendMultiple`, but does not enumerate sandbox paths as operations. The former
file mixed 25 sandbox operations into the production operation list. Their
full previous definitions and all shared schemas are preserved in
[previous-sandbox.json](sources/v4/previous-sandbox.json), extracted from
`50f9a72`; the V4 specification carries an explicit inventory, origin and hash
in `x-unpublished-sandbox`. They are historical repository evidence, not an
official Swagger capture or newly tested service behavior. No operation is
silently discarded and no production response shape is asserted for them.
Their current availability still needs provider confirmation or a separately
authorized service test. Production client generation now uses only the
26 current published contracts.

| Historical method | Relative path | Prior operation ID |
| --- | --- | --- |
| POST | `/sandbox/Send` | `SandboxV4_SendSingle` |
| POST | `/sandbox/SendBulk` | `SandboxV4_SendBulk` |
| POST | `/sandbox/SendOtp` | `SandboxV4_SendOtp` |
| POST | `/sandbox/SendVoiceOtp` | `SandboxV4_SendVoiceOtp` |
| POST | `/sandbox/SendTokenMulti` | `SandboxV4_SendTokenMulti` |
| POST | `/sandbox/SendTokenSingle` | `SandboxV4_SendTokenSingle` |
| GET | `/sandbox/SendTokenSingle` | `SandboxV4_SendTokenSingleByQuery` |
| GET | `/sandbox/SendTokenSingleConcatParam` | `SandboxV4_SendTokenSingleConcatByQuery` |
| POST | `/sandbox/SendTokenSingleConcatParam` | `SandboxV4_SendTokenSingleConcat` |
| POST | `/sandbox/GetToken` | `SandboxV4_GetToken` |
| POST | `/sandbox/StatusById` | `SandboxV4_StatusById` |
| POST | `/sandbox/StatusByUserTraceId` | `SandboxV4_StatusByUserTraceId` |
| POST | `/sandbox/GetAccountInfo` | `SandboxV4_GetAccountInfo` |
| POST | `/sandbox/GetInbox` | `SandboxV4_GetInbox` |
| POST | `/sandbox/phonebook/groups` | `SandboxV4_PhonebookGroups` |
| POST | `/sandbox/phonebook/group` | `SandboxV4_CreatePhonebookGroup` |
| POST | `/sandbox/phonebook/group-with-contacts` | `SandboxV4_CreatePhonebookGroupWithContacts` |
| POST | `/sandbox/phonebook/contacts` | `SandboxV4_UpsertPhonebookContacts` |
| POST | `/sandbox/phonebook/contacts/remove` | `SandboxV4_RemovePhonebookContacts` |
| POST | `/sandbox/campaign/draft` | `SandboxV4_CreateCampaignDraft` |
| POST | `/sandbox/campaign/draft/finalize` | `SandboxV4_FinalizeCampaignDraft` |
| POST | `/sandbox/campaign/submit` | `SandboxV4_SubmitCampaign` |
| POST | `/sandbox/campaign/get` | `SandboxV4_GetCampaign` |
| POST | `/sandbox/campaign/search` | `SandboxV4_SearchCampaigns` |
| POST | `/sandbox/campaign/recipients` | `SandboxV4_GetCampaignRecipients` |

### Upstream example defects

Three V4 success examples conflict with their `date-time` schemas:

| Operation | Field | Original value |
| --- | --- | --- |
| POST `/campaign/get` | `result.createdAt` | `2026-01-01T10:00:00` |
| POST `/campaign/search` | `result.items[0].createdAt` | `2026-01-01T10:00:00` |
| POST `/campaign/recipients` | `result.items[0].sentAt` | `2026-01-01T10:30:00` |

RFC 3339 date-time requires a timezone. Although provider prose says Iran time,
no offset was appended and no response field was removed or schema relaxed to
make the examples pass. The exact examples remain in the raw source and
`x-invalid-source-examples` under their original response media types. Response
descriptions warn about them. The issue file names exact operations, fields,
values and hashes of the entire examples. Offline validation must reproduce
those exact source failures; an unexpected failure or changed example fails
the check. They are not offered as schema-valid success examples. Other valid
examples and all response schemas remain usable.

The initial installed jsonschema package lacked its optional date-time format
checker; Redocly exposed the issue. The validator now supplies an explicit
RFC 3339 timezone/calendar check, so the optional dependency cannot silently
skip this format. No linter rule was disabled and no source bytes were edited.
The provider must clarify its serialized timestamp format before these three
success examples can be presented as valid without qualification.

## Meaningful V3 / V4 differences

| Area | V3 | V4 |
| --- | --- | --- |
| API key | `ApiKey` in POST JSON; nullable by schema | `apiKey` in POST JSON, non-null; GET retains `ApiKey` |
| Response casing | PascalCase | camelCase, plus `moreInfo` |
| Template listing | `TokenList` | `GetToken`, no voice-template field, four status codes |
| Template GET values | `p1`–`p10`, `p` | `P1`–`P10`, `P`; POST still uses lower-case `p1`–`p10` / `p` |
| Message and trace IDs | int64 (trace IDs nullable) | strings (trace IDs nullable); keep strings intact |
| Send response details | ID and caller trace ID | also parts and cost; OTP includes sender/final text |
| Status response details | ID, caller trace ID, code, text | additionally nullable `rejectionReason` |
| Inbox sender field | exact `Form` | exact `from`; inbox ID is string |
| Account route | `AccountInfo` | `GetAccountInfo` |
| Credit unit | legacy unit, not numerically specified | explicitly rial; no conversion guessed |
| Error 20 | `TooManyRequests` | `OtpApiLimitReached`; HTTP 429 is separate |
| Added V4 error codes | absent | 21 daily parts; 22 daily credit; 23 send time; 24 voice-recipient limit |
| Additional capabilities | published basic messaging/template/account operations | fixed-code SMS and voice OTP, scheduling, phonebook, campaigns |

Both versions use API keys inside requests, optional `source-app`, HTTP
200/429/default declarations, and the same numeric 0–21 message delivery status
values. These similarities are retained. Campaign recipient statuses are a
separate V4 enum and must not be interpreted as the delivery-query status enum.
No extra difference in credential acquisition was invented.

## Remaining ambiguities

- Swagger prose calls template keys, group names and phonebook mobiles mandatory,
  while several corresponding fields are absent from required lists. V3 also
  declares a required API key nullable. Formal schema and prose are both
  preserved rather than silently choosing one interpretation.
- HTTP 429 has no named retry header or body schema. Default errors have no
  body schema/examples. Do not assume the normal response envelope for them.
- The three V4 campaign timestamps conflict with declared date-time formats.
- Historical sandbox availability, V3 legacy code-table guidance, and every
  production runtime behavior remain outside this Swagger-only verification.
- V4 summaries/descriptions sometimes use PascalCase identifiers while actual
  JSON schemas use camelCase. Actual parameter/property spellings are preserved;
  examples are never case-normalized from prose.
- Maximum batch sizes, literal-semicolon escaping, token expiry and unsupported
  validation constraints were not inferred when absent from Swagger.

## Final validation and build results

| Check | V3 | V4 |
| --- | --- | --- |
| Published operation coverage | 13/13, 11 paths | 26/26, 24 paths |
| Output component schemas | 26 (stable aliases/shared models) | 66 |
| Snapshot hash and deterministic source agreement | passed | passed |
| Independent input/output schema constraints, headers and content types | passed | passed |
| Published explicit examples examined | 79 valid | 143 examined: 140 valid, 3 recorded upstream defects |
| Active output examples | 70 valid | 140 valid; 3 originals retained with invalid-source labels |
| Redocly 2.77.0 lint | passed, no warnings | passed, no warnings |
| Redocly bundle | passed | passed |

The baseline consistency validator returns zero errors and one pre-existing
warning for historical removed V3 error code 7. Required rules remain enabled;
the repository's existing two exceptions are unchanged. Validation, lint and
bundling ran locally through Podman with the repository mounted read-only;
Redocly ran with networking disabled and the already downloaded official image.
No Docker installation or other machine was needed.

This repository has no documentation-site application or site build command.
Redocly bundling is the checked machine-readable build. No build/deploy of the
separate docs-site repository was claimed. Local documentation links and
provenance paths were checked: 33 links/paths, zero errors. No per-language
consumer was modified. Bundle artifacts were written outside the repository
to `/tmp/sms-webservice-spec-build-ofi0_twh/`.

```bash
python3 scripts/sync_swagger.py v3 --check
python3 scripts/sync_swagger.py v4 --check
python3 scripts/validate_swagger.py v3 v4
python3 scripts/validate.py
podman run --rm --pull=never --network=none -v "$PWD:/spec:ro" -w /spec \
  docker.io/redocly/cli:latest lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

## Changed and new files

Modified:

- `specs/v3/openapi.yaml`: complete current V3 contract and examples.
- `specs/v4/openapi.yaml`: current published V4 contract, issue annotations,
  source navigation and explicit historical sandbox inventory.
- `specs/v3/codes/error-codes.yaml`, `status-codes.yaml`, `template-status.yaml`:
  current source labels/provenance, prior text retained.
- `README.md`, `README.en.md`: synchronized architecture, behavior and checks.
- `AGENTS.md`: current operation counts, evidence boundaries and checks.
- `redocly.yaml`: outdated explanatory comments corrected; rule settings unchanged.
- `PUBLISHED-SWAGGER-CHANGES.md`: this complete reconciliation report.

New:

- `sources/v3/swagger.json`, `sources/v3/provenance.json`.
- `sources/v4/swagger.json`, `sources/v4/provenance.json`.
- `sources/v4/issues.json`: three exact upstream example defects.
- `sources/sandbox-servers.json`: maintainer-confirmed sandbox addresses.
- `sources/v4/previous-sandbox.json`: historical definitions with origin metadata.
- `scripts/sync_swagger.py`: offline reproducible reconciliation and drift checks.
- `scripts/validate_swagger.py`: coverage, references, schemas and explicit examples.

At the initial reconciliation stage, no files inside existing version directories
were moved or renamed, and no commits or pushes had been made. The six subsequent
commits were individually authorized and pushed separately. No history rewrite,
permission change, author-identity change or assistant attribution was added.

## Follow-up: Persian README formatting and V4 code-table parity

Reviewed the live official V4 Swagger again on 11 November 2026. Its SHA-256
is still `3406d26a3258370a7034ebdb8fa42f8b775938ecd2e0785991b3f8bf9e5ab968`,
identical to the retained capture. No response code or enum was guessed from
V3 or from a previous implementation.

The earlier V4 OpenAPI already recorded `200`, `429`, and `default` for all
26 published operations. The missing parity was the external code-reference
tables and their baseline validation: V3 had enum tables, while V4 did not.
These are different namespaces and are now documented separately:

| Reference | V3 | V4 |
| --- | --- | --- |
| HTTP responses per operation | 13 operations | 26 operations |
| API errors | 20 current codes plus one historical removed row | 24 codes |
| Message delivery | 22 codes | 22 codes |
| Template approval | 3 states | 4 states |
| Campaign progress | not published | 6 states |
| Campaign search filter | not published | 3 values |
| Campaign recipient status | not published | 32 codes |

New per-operation HTTP inventories are
[`specs/v3/codes/http-status.yaml`](specs/v3/codes/http-status.yaml) and
[`specs/v4/codes/http-status.yaml`](specs/v4/codes/http-status.yaml).
Each retains every method, full source path, operation ID, HTTP response key,
description, declared header and response media/schema reference. Schema
references resolve against the explicitly named official `schema_document`.
Every operation publishes HTTP 200 and 429 plus `default`; `default` is not a
third numeric HTTP status. No 401, 403, 404 or 500 response declaration was
invented, and no retry-header name or error body was inferred.

All six V4 enums have separate tables:

- [API errors](specs/v4/codes/error-codes.yaml): `ApiErrorType`, 24 codes.
- [Delivery statuses](specs/v4/codes/status-codes.yaml): `ApiMessageStatus`, 22 codes.
- [Template states](specs/v4/codes/template-status.yaml): `TokenListItemStatus`, 4 states.
- [Campaign progress](specs/v4/codes/campaign-status.yaml): `CampaignProgressStatus`, 6 states.
- [Campaign filters](specs/v4/codes/campaign-filter-status.yaml): `CampaignState`, 3 values.
- [Campaign recipients](specs/v4/codes/campaign-recipient-status.yaml): `SentMessageStatus`, 32 codes.

Names and Persian labels come from the enum metadata or, for `ApiErrorType`,
the error table in Swagger's info description. That table's numeric label
prefixes are preserved. Campaign recipient enum names are absent in Swagger,
so their `name` values remain null. Unpublished detailed causes/actions,
retry policies, polling dispositions and explicit sendability policies remain
null with notes. They were not copied from V3 or inferred from labels.

The generated V4 rows intentionally have `confirmed: false`: publication in
Swagger is not independent observation of the running service. The baseline
validator now checks all six V4 enums rather than skipping them because their
schema names differ from V3. It returns **zero errors and 92 warnings**:
91 unconfirmed Swagger-only rows plus the existing removed V3 error-code
warning. These warnings are disclosed, not suppressed; strict mode continues
to fail on warnings as designed.

The Persian first-word rule is applied to every physical README line, including
wrapped prose, tables, diagrams and code comments. Both READMEs are checked
after removing Markdown/HTML formatting; Latin-only code remains untouched.
The new `scripts/validate_readmes.py` is also called by the required baseline
validator, and the rule is recorded in AGENTS.md and CONTRIBUTING.md. A
regression check found 30 violations in the previously committed Persian
README and zero in the corrected file. Both current READMEs pass.

`sync_swagger.py` now writes/checks the HTTP and V4 enum tables as well as the
OpenAPI outputs. `validate_swagger.py` independently compares every HTTP row
and every enum code, name and label with the captured source. It also detects
missing/extra enum tables and unsupported confirmation/policy claims. Focused
regression checks confirmed that deleting one operation's HTTP 429 response
or changing an enum label causes validation failure.

Validation for this follow-up: exact source/output agreement, all 39 published
operations, all 91 V4 enum rows, all 210 active examples and both README checks
pass. Redocly 2.77.0 validates V3 and V4 without warnings. The three original
V4 timestamp example defects remain preserved and explicitly reported. No API
operation was called and no endpoint behavior was newly claimed as tested.
This follow-up remains uncommitted and unpushed pending approval.

## Token-list naming correction and current validation

Both official Swagger JSON documents were fetched again on 2026-11-11 and
match the saved captures byte for byte. V3 uses `POST /api/V3/TokenList`;
V4 uses `POST /uapi/v4/GetToken`. Earlier report wording treating the intended
V3 name as unresolved was incorrect and has been removed. V3-specific prose
now describes `TokenList`; V4 retains its independently published name.
The operation schemas and source examples already use these correct names.
The V4 HTTP inventory correctly records `V4_GetToken` and its own response
schema; it must not be renamed to the V3 method. No service operation was called.

V3 reconciliation and both README checks pass. Baseline validation reports
0 errors and 92 provenance warnings. Before committing, delivery-status code
11 in [`status-codes.yaml`](specs/v4/codes/status-codes.yaml) was aligned with
the captured and freshly fetched Swagger label `دریافت کننده نامعتبر`.
Full V3 and V4 reconciliation now passes. The three previously recorded
campaign timestamp defects remain upstream issues. Redocly lint passes for
both specifications. These are Swagger-based checks, not service tests.
