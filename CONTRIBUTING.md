# Contributing

Our product and engineering teams maintain this repository as the authoritative
API contract for the Payam Resan SMS web service. Changes propagate to our
documentation, language examples, client generators and MCP server.

## Evidence before changes

Our development team's approved V3 reference and its verified observations
are authoritative. Preserve all descriptions, constraints, error handling,
retry and polling rules, code rows and examples. Swagger is incomplete; an
omission there does not justify deleting approved content. The
reference is maintained directly under `specs/v3/`.

Use each version's own Swagger for additions and V4 details. Do not infer
functionality. As authorized by our product owner, use approved V3 policies as
references for V4 only after checking the corresponding functionality and
meaning independently in V4. Record that policy source separately from runtime
verification. Preserve version-specific differences.

Keep runtime testing distinct from published-contract verification.
`confirmed: false` means a code has not been independently tested; it does
not invalidate an exact extraction from our Swagger. V3 retains the original
confirmed flags and policy values supplied by our team. V4-only policies remain
null when neither V4 evidence nor an applicable approved V3 policy supplies them.

Ask the user directly about missing details and schema/prose disagreements
before documenting them. Wait for a confirmed answer; do not infer behavior.
Official documentation contains verified facts, not unresolved questions,
internal review remarks or instructions asking a development team to fix things.
Verification needs a recorded source, date and scope. Do not request or store
secrets. Tests that send messages, incur costs or change data need explicit
authorization and defined test data.

## Preserve the current wire contract

V3 uses `TokenList`; V4 uses `GetToken`. Both list templates, but their
request and response structures differ. Preserve exact names, casing, required
fields and nullability. V3 inbox sender `Form` remains the wire name.

We can fix our service and its documentation together. Do not silently rename
a field in this reference while the implementation still uses the old name.
Any breaking change needs an explicit compatibility and release decision.

A version is a folder under `specs/`. Do not move or rename existing version
files. Add only released versions. Preserve the verified V3 content; do not
classify it as obsolete or unsupported just because Swagger omits it.

## Validate changes

Edit the specifications and code tables directly under `specs/`.
Use approved team information and each version's Swagger together. Preserve
the existing verified content; do not replace it with incomplete metadata.

```bash
python3 scripts/validate.py
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

Podman may replace Docker. Never weaken validators to pass a contract defect.
Examples in the specification must match their schemas. V4 timestamp strings
are timezone-free Tehran local time (UTC+03:30). Use `date-time-local` with its
pattern for these fields; preserve their values without appending an offset.

## Documentation conventions

Write from our internal product and technical perspective. Both
[Persian](README.md) and [English](README.en.md) READMEs cover the same material
in the same section order. Explain verified behavior directly. Ask the user
about anything unclear before adding it to either README or the specification.

Every physical README line containing Persian text must have a Persian first
word after Markdown/HTML formatting is removed, including tables, code
comments, wrapped prose and diagrams. Apply this to the English README too.
Keep code lines free of Persian trailing comments. Do not weaken the check.

Spell the brand `پیام رسان` with a real space. Introduce it in Persian as
`پنل پیامکی پیام رسان`. Preserve a linked `payam-resan.com` footer in both
READMEs. Method and field identifiers retain their exact wire spellings.

## Review and Git

A specification change must identify affected operations, fields, examples and
downstream consumers, and include its verification results. Ask the user about
open questions in the conversation; do not put them in official documentation.
Use Issues to track implementation defects, contract decisions and future
maintenance. Do not create external issues or messages without authorization.

Do not commit or push without explicit approval. Use the approved repository
identity, no assistant attribution and no co-author trailers.
Commit messages use `type(scope): subject` without a body and name changed
methods or fields when the specification changes. Group independent operations
separately so each change remains reviewable.
