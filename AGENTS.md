# Working with our API reference

We own and develop the Payam Resan SMS web service. Our product and engineering
teams maintain this repository as the authoritative machine-readable contract
for our documentation site, language examples, client generators and MCP server.

## Source and scope

Use our development team's approved documentation and each version's Swagger
together. Swagger is incomplete and must not replace verified team knowledge.
Use each version's Swagger independently for additions:
- V3: https://www.payam-resan.com/api/V3/swagger.json
- V4: https://www.payam-resan.com/uapi/v4/swagger.json

V3 publishes 13 operations across 11 paths; V4 publishes 26 across 24.
Specifications and code tables are maintained directly under `specs/v3/`
and `specs/v4/`. Update these files in place. Do not add source-copy
directories, approval manifests, generators or test directories.
Preserve V3 descriptions, constraints, examples, code rows, retry rules,
polling policies, template/panel mappings and confirmed metadata.
An omission in Swagger is not grounds to remove approved information.

## Verified facts and engineering decisions

Never infer missing behavior. The restored V3 information is verified and
approved by our development team. New Swagger declarations are an additional
source and do not invalidate that information. Record the verification
method honestly. `confirmed: false` on a code row means no independent runtime
confirmation; the code and label must still match the source exactly.

If behavior is unclear or information is missing, ask the user directly before
documenting it. Wait for a confirmed answer; do not infer a resolution, create
a public question register or put internal review notes in official documentation.
Only verified, confirmed information belongs in the specification and READMEs.
Preserve the approved V3 retry, polling and sendability values. For V4, do not
copy these policies without confirmation; missing V4 values remain null. Source notes record
provenance, not unresolved questions or instructions for a development team.
Record verification method, environment and date accurately. Never record credentials or customer data.
Do not issue sending, billing, campaign or data-changing requests without
authorization and a defined test environment.

Known invalid Swagger examples must not be included in the specifications. Do not guess timestamps, weaken validation or
mark unresolved questions as resolved to make checks pass.

## Wire contract requirements

- Preserve every operation, HTTP method, path, parameter, request and response
  schema, authentication requirement, content type, example and constraint.
- Preserve required and nullable independently. Report conflicts between prose
  and schema directly to the user before documenting an interpretation.
- V3 `TokenList` and V4 `GetToken` list templates; neither issues login tokens.
  Their request casing, result fields and status enums differ.
- V3 inbox sender is `Form`, not `From`. Keep the current wire name; an
  implementation correction requires an explicit contract change.
- HTTP status is separate from API errors, delivery and campaign enums.
  `default` is not numeric. HTTP 200 requires checking the success envelope.
- The API key is a required query parameter on GET or a JSON property on POST.
  Do not invent a header security scheme for the JSON credential.
- V3 template states are 1–3, with the approved panel mappings and sendability
  rules preserved. V4 independently publishes 1–4, including
  `RejectedPermanently`; its policies require V4-specific evidence.

Our confirmed sandbox bases are V3 `/api/V3SandBox` and V4 `/uapi/v4SandBox`,
as confirmed by the user. Do not replace them with obsolete addresses. V4 `SendMultiple` is
production-only in our published contract. Do not promise other sandbox
behavior that the user has not confirmed.

A version is a folder. Do not move or rename files inside an existing version.
Our V3 code directory contains three enum tables and one HTTP inventory.
V4 contains six enum tables and one HTTP inventory. V3 tables must preserve
the approved team reference, including documented non-current rows marked
`exists: false`. V4 code labels and source hashes must match its own evidence.

## Persian README formatting

Every physical README line containing Persian text must have a Persian first
word after Markdown/HTML formatting is removed. This includes table rows,
wrapped prose, diagrams and code comments, in both READMEs. Latin identifiers,
paths, URLs and numbers cannot come first. Keep code lines free of Persian
trailing comments. Never weaken the README check in `scripts/validate.py` to pass prose.

Use our internal product and engineering perspective in all repository
documentation. Both READMEs must cover the same material and section order.
Preserve the brand spelling `پیام رسان`, with a real space, and the linked
`payam-resan.com` footer. Introduce the Persian brand as `پنل پیامکی پیام رسان`.

## Required checks

```bash
python3 scripts/validate.py
docker run --rm -v "$PWD:/spec" -w /spec redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

Podman may replace Docker. The validator checks code-table consistency,
references, operation metadata and Persian README formatting. Preserve the
original V3 content and verify new operations against Swagger. Warnings remain
explicit; do not convert missing evidence into confirmation. `--strict`
intentionally fails on warnings.

Our existing Redocly exceptions are `security-defined` and
`operation-4xx-response`. Do not disable further rules to hide contract defects.

## Git and downstream changes

Do not commit or push without explicit user approval. Use the approved
repository author identity; never add assistant attribution or co-author trailers.
Use `type(scope): subject` messages without a body. Name changed methods or
fields when updating OpenAPI so consumers know what to regenerate.
Group independent changes into separate commits when requested.

Human documentation: https://docs.payam-resan.com
Language examples: https://github.com/Mojeshahr
