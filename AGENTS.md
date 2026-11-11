# Working with this repository

This is the machine-readable description of the Payam Resan SMS web service,
an Iranian SMS provider. It is the source that the documentation site, the
per-language example repositories and the MCP server derive from.

It is not a client library and not a guide. If someone wants working code,
send them to their language's repository at <https://github.com/Mojeshahr>; if
they want something to read, send them to <https://docs.payam-resan.com>. What
lives here is the description itself, for tools and code generators.

## What you would use this for

Generating a client, or building the V3 error and status tables into an
application. `specs/v3/openapi.yaml` has thirteen published operations across eleven paths;
`specs/v3/codes/` has three enum tables and a per-operation HTTP response table.
`specs/v4/openapi.yaml` records 26 published operations across 24 paths.
`specs/v4/codes/` has the same HTTP response inventory plus all six published
enum tables: errors, message delivery, templates, campaign progress, campaign
filters and campaign recipients. HTTP status is distinct from every API enum;
`default` is not a numeric HTTP code. Do not copy V3 retry/polling policies to V4.
Unpublished policies remain null with a note. V4 Swagger-only rows have
`confirmed: false` and produce explicit validation warnings, not errors.
The former 25 sandbox definitions are preserved in
`sources/v4/previous-sandbox.json`, explicitly as historical evidence, not a
current published contract. Never silently discard them or infer their current
behavior from the production schema. Both specifications record Swagger claims,
not newly observed live behavior. Four operations in each version use the
published summary because the longer description is empty.

`sources/` holds exact Swagger captures, provenance hashes and upstream issues.
`sources/sandbox-servers.json` records maintainer-confirmed sandbox bases:
V3 `/api/V3SandBox` and V4 `/uapi/v4SandBox`. The V4 Swagger capture still
contains the obsolete `/uapi/v4/sandbox` address; never restore that as current
guidance. V4 `SendMultiple` is production-only according to Swagger.
`scripts/sync_swagger.py <v3|v4> --check` detects drift; omit `--check` only to
regenerate from a reviewed snapshot, including the HTTP/V4 enum tables.
`scripts/validate_swagger.py v3 v4` checks every operation's HTTP declarations,
all six V4 enum tables, and
coverage, references and examples using PyYAML and jsonschema. Three upstream
V4 campaign success examples omit a timezone: their exact originals are kept
under `x-invalid-source-examples`, with hash-bound issues recorded separately.
Never guess a timezone or weaken a validator to make an example pass.

A version is a folder, not a branch and not a tag. Nothing inside an existing
version folder is ever moved or renamed.

## Persian README line starts

Every physical README line containing Persian text must have a Persian first
word after Markdown/HTML formatting is removed. This includes table rows,
wrapped prose, diagrams and code comments. English identifiers, URLs, paths
and numbers cannot precede the first Persian word on such a line. Keep pure
code/path lines free of Persian trailing comments or put the comments on their
own Persian-leading lines. Check every README, including the English file.
`python3 scripts/validate_readmes.py` enforces this rule; the baseline
`scripts/validate.py` also runs it. Do not weaken the check to pass a document.

## Three behaviours any generated client must encode

These published details matter to generated clients. Treat them as Swagger
claims; this reconciliation did not independently test service behavior:

**HTTP 200 alone does not imply success.** V3 Swagger publishes `200`, `429`,
and `default`. Read `Success` when the usual response envelope is present;
other HTTP errors can have a different shape. These are published claims,
not live-service tests from this reconciliation.

**In V3, `ErrorCode` means something only on failure.** Until `Success` is
`false`, reading it is meaningless.

**In V3, the key travels inside the request** — a query parameter on `GET`, a
body field on `POST`, never a header. This is why the spec declares no
`securityScheme`: OpenAPI cannot express a credential that sits in a JSON body.
The key is an explicit required query parameter or body property instead.
Published required and nullable declarations must remain distinct, even when
the provider’s prose disagrees. `GetToken` exists in V4 and lists templates;
V3 calls this operation `TokenList`. Neither generates a login token.

## V3 spellings your code has to match

The sender field in V3 `GetInbox` is named **`Form`, not `From`**. It is
documented exactly that way so generated code matches the real response. Do not
correct it.

V3 Swagger publishes three template states. Prior panel observations separated
two kinds of rejection, both recorded as API code `3`; that historical evidence
is retained in `specs/v3/codes/template-status.yaml` and has not been retested.
V4 independently publishes four states, including `RejectedPermanently`.

## Why the V3 code tables live outside the spec

The `ErrorCode` and `StatusCode` values are needed in two places: as an `enum`
in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the V3 numbers stay in the spec, the text lives in `specs/v3/codes/`, and
`scripts/validate.py` fails if the two drift apart.

What the tables carry beyond the text:

- `retry` on each error code — `never`, `backoff` or `limit-reset`. A client
  that ignores this will hammer a code that can never succeed until the account
  hits error `20`.
- `disposition` on each status code — `pending`, `final`, `not-sent` or
  `not-found`. This is what tells a polling loop when to stop.
- `sendable` on each template state.

Rows also carry their provenance: `in_api`, `in_legacy_docs`, `confirmed`. A
row that is not `confirmed` is a gap in the service, not in this repository, and
it is a warning rather than an error.

## If you are changing something here

Never guess. If you do not know what an error code means, write `null` and say
why in `note`. A guessed description in a reference file is worse than a missing
one, because it propagates into the documentation, the language examples and the
MCP server, and nobody reviews it again downstream.

This repository describes an external service. Nothing here is ever "fixed" —
what is recorded is exactly how the service behaves, misspellings included.

Two checks must be green, and the way to pass them is to satisfy them, never to
silence them:

```bash
python3 scripts/validate.py
docker run --rm -v "$PWD:/spec" redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

Redocly has exactly two rules disabled: `security-defined`, because the key is
a body field on `POST`; and the existing `operation-4xx-response` exception.
Both current Swagger documents now publish HTTP 429 responses.
Treat the V4 status codes as documented claims, not independently verified
runtime behavior.

A change to `openapi.yaml` reaches three consumers. Name the method or the field
that changed in the commit message, so those repositories know what to
regenerate.

## Where to go next

- Human documentation: <https://docs.payam-resan.com>
- Working code in twenty languages: <https://github.com/Mojeshahr>
