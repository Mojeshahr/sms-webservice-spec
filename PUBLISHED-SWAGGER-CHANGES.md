# Published Swagger changes

Compared the published Swagger documents with the repository's existing V3
specification and V4 draft on 10 November 2026.

Sources:

- [V3 Swagger UI](https://www.payam-resan.com/api/V3/) ·
  [V3 OpenAPI JSON](https://www.payam-resan.com/api/V3/swagger.json)
- [V4 Swagger UI](https://www.payam-resan.com/uapi/v4) ·
  [V4 OpenAPI JSON](https://www.payam-resan.com/uapi/v4/swagger.json)
- Repository: [`specs/v3/openapi.yaml`](specs/v3/openapi.yaml) and
  [`specs/v4/openapi.yaml`](specs/v4/openapi.yaml)

This report describes differences in the published documents. A Swagger
declaration is not, by itself, runtime verification of the service.

## V3 differences

The published V3 document describes 13 operations on 11 paths. The repository
spec described 11 operations on 10 paths at comparison time.

- New `GET` and `POST` operations at `/SendTokenSingleConcatParam` send a
  template with one `p` value containing semicolon-separated parameters. The
  existing `SendTokenSingle` operations use separate `p1` through `p10` values.
- All published operations declare an optional `source-app` header, up to 100
  characters, for request attribution. It is not the API key.
- All published operations list `200`, `429`, and `default` responses. The
  `429` description says rate-limited callers should read the retry time from a
  response header. The repository's V3 contract records that responses are
  always `200`; this discrepancy needs provider/runtime confirmation before
  changing that behavioral claim.
- Published paths include the `/api/V3` prefix; the repository uses paths
  relative to its configured server.
- The published error-code enum and message status-code values match the
  repository's V3 code tables. No new code values were found.

## What published V4 documents

The public V4 Swagger describes 26 production operations on 24 paths. It
provides typed JSON request and response schemas, in contrast to the local
draft's binary/unconfirmed response declarations. The schema shapes below are
what Swagger documents and have not been independently confirmed against live
responses.

| Area | Documented capabilities |
|---|---|
| Messaging | Single and bulk SMS; per-recipient messages; templated SMS using `p1`–`p10` or a semicolon-concatenated `p`; fixed-message SMS OTP with a 4–8 digit code; voice OTP |
| Account and delivery | Account credit and sender lines; unread inbox messages; template listing; status lookup by message ID or caller trace ID |
| Campaigns | Draft creation with a price preview; draft finalization; one-call submission; campaign search and retrieval; paginated recipient delivery statuses and net credit |
| Phonebook | List and create groups; create a group with contacts; upsert contacts; remove contacts |

As in V3, every published V4 operation declares `source-app` and `200`, `429`,
and `default` responses. The production paths in the published file are
prefixed by `/uapi/v4`; the repository can keep its configured V4 server URL
and use relative paths.

The public Swagger does not include the V4 `/sandbox/` operations. The
repository's sandbox routes are retained separately because they are known to
work; their absence from the public document does not establish that they are
unavailable.

## Follow-up before treating documentation as runtime fact

Confirm the V3 `429` behavior and retry header, and confirm the published V4
response shapes against the provider or live service. Until then, regard these
as Swagger claims rather than independently verified behavior.
