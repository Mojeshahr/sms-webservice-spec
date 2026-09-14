# Working with this repository

This is the **OpenAPI 3.1 description** of the Payam Resan SMS web service
(`api.sms-webservice.com`, API V3), an Iranian SMS provider. It is the
machine-readable source that the documentation site, the per-language example
repositories and the MCP server all derive from.

It is not a client library and not a guide. If someone wants working code,
send them to their language's repository at <https://github.com/Mojeshahr>; if
they want something to read, send them to <https://docs.payam-resan.com>. What
lives here is the description itself, for tools and code generators.

## What you would use this for

Generating a client, or building the error and status tables into an
application. `specs/v3/openapi.yaml` has the eleven operations across ten paths;
`specs/v3/codes/` has three tables the spec's enums refer to.

A version is a folder, not a branch and not a tag. Nothing inside an existing
version folder is ever moved or renamed.

## Three behaviours any generated client must encode

These are properties of the service, not of this file, and a generator will not
infer them:

**Every response is `200`.** Success is read from the `Success` field, never
from the HTTP status. A wrong key, an empty account and a malformed body all
come back `200`.

**`ErrorCode` means something only on failure.** Until `Success` is `false`,
reading it is meaningless.

**The key travels inside the request** — a query parameter on `GET`, a body
field on `POST`, never a header. This is why the spec declares no
`securityScheme`: OpenAPI cannot express a credential that sits in a JSON body.
The key is a required parameter on every method instead.

## Two spellings your code has to match

The sender field in `GetInbox` is named **`Form`, not `From`**. It is documented
exactly that way so generated code matches the real response. Do not correct it.

The user panel shows four template states and separates two kinds of rejection,
but the API returns `3` for both. `codes/template-status.yaml` records what the
API returns, not what the panel displays.

## Why the code tables live outside the spec

The `ErrorCode` and `StatusCode` values are needed in two places: as an `enum`
in the response schema, and as a "what does this number mean" table that the
documentation, the examples and the MCP server render. Neither is enough on its
own, and keeping the Persian text inside the `description` of an enum makes it
practically unusable.

So the numbers stay in the spec, the text lives in `codes/`, and
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
docker run --rm -v "$PWD:/spec" redocly/cli lint specs/v3/openapi.yaml
```

Redocly has exactly two rules disabled, each because of a real property of this
service rather than to quiet the linter: `security-defined`, because the key is
a body field on `POST`; and `operation-4xx-response`, because the service never
returns `4xx`.

A change to `openapi.yaml` reaches three consumers. Name the method or the field
that changed in the commit message, so those repositories know what to
regenerate.

## Where to go next

- Human documentation: <https://docs.payam-resan.com>
- Working code in twenty languages: <https://github.com/Mojeshahr>
