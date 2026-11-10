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
application. `specs/v3/openapi.yaml` has the eleven operations across ten paths;
`specs/v3/codes/` has three tables the spec's enums refer to.
`specs/v4/openapi.yaml` records 26 published production operations across 24
paths, plus 25 known-working sandbox operations across 23 paths. Its typed
responses reflect the published Swagger and have not been independently
verified against live responses. Four operations use their published summary
as the description because the Swagger has no longer description. Do not infer
V4 behavior from V3.

A version is a folder, not a branch and not a tag. Nothing inside an existing
version folder is ever moved or renamed.

## Three behaviours any generated client must encode

These are properties of the service, not of this file, and a generator will not
infer them:

**In V3, every response is `200`.** Success is read from the `Success` field,
never from the HTTP status. A wrong key, an empty account and a malformed body
all come back `200`.

**In V3, `ErrorCode` means something only on failure.** Until `Success` is
`false`, reading it is meaningless.

**In V3, the key travels inside the request** — a query parameter on `GET`, a
body field on `POST`, never a header. This is why the spec declares no
`securityScheme`: OpenAPI cannot express a credential that sits in a JSON body.
The key is a required parameter on every method instead.

## V3 spellings your code has to match

The sender field in V3 `GetInbox` is named **`Form`, not `From`**. It is
documented exactly that way so generated code matches the real response. Do not
correct it.

The V3 user panel shows four template states and separates two kinds of
rejection, but the API returns `3` for both. `specs/v3/codes/template-status.yaml`
records what the API returns, not what the panel displays.

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
a body field on `POST`; and `operation-4xx-response`, because V3 uses HTTP 200
for API failures while the public V4 Swagger documents HTTP 429 responses.
Treat the V4 status codes as documented claims, not independently verified
runtime behavior.

A change to `openapi.yaml` reaches three consumers. Name the method or the field
that changed in the commit message, so those repositories know what to
regenerate.

## Where to go next

- Human documentation: <https://docs.payam-resan.com>
- Working code in twenty languages: <https://github.com/Mojeshahr>
