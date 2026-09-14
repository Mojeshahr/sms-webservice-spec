# Contributing

Maintainer notes for this repository: the rules that keep it consistent with the
other repositories in this organisation and with the documentation site.

If you came here to use this repository rather than change it, read `AGENTS.md`
instead.

## Rule one: never guess

If you do not know what an error code means, what a field holds or how a method
behaves, write `null` and say why in `note`. A guessed description in a
reference file is worse than a missing one, because it propagates into the
documentation, the language examples and the MCP server, and nobody reviews it
again downstream.

The tables under `codes/` carry `in_api` and `in_legacy_docs` so the origin of
every row stays visible. A row with neither is a row from nowhere, and it should
be removed.

## Rule two: do not correct the service's mistakes

The sender field in `GetInbox` is spelled `Form`. That spelling lives in the
service. Correct it here and the generated code stops matching the real
response, and somebody loses hours finding out why.

Record the mistake verbatim and warn about it in the neighbouring
`description`.

## Rule three: a version is a folder

A new version means a new `specs/v<n>/`. No file inside an existing version
folder is moved, renamed or rearranged; older versions of the service still
have customers.

No folder is created for a version the service has not released, not even an
empty one.

## Rule four: satisfy the validator, never silence it

```bash
python3 scripts/validate.py
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml
```

An error means the spec and the tables have drifted apart, and one of them has
to be corrected.

A warning means there is a gap in the service itself. Do not quiet a warning by
filling a table with a guess, and do not remove its condition from
`validate.py`. A warning goes away when somebody from the service team supplies
the real answer.

## Rule five: after every change to the spec

A change in `openapi.yaml` reaches three consumers: the documentation site, the
per-language examples, and the MCP server. Name the method or the field that
changed in the commit message, so those repositories know what to regenerate.

## Two languages, two files

The repository carries two READMEs and both stay in step:

| File | Language | Direction |
|---|---|---|
| `README.md` | Persian | right to left |
| `README.en.md` | English | left to right |

The English file is named exactly `README.en.md`. GitHub renders only
`README.md` on its own, so both files open with a language switch line so that
either one leads to the other:

```
<b>فارسی</b> · <a href="README.en.md">English</a>
```

**The English text is not a literal translation of the Persian.** Same material,
written for a reader who does not know Persian and most likely arrived from
outside Iran. The structure and the section order stay identical, which is what
makes keeping them in step cheap.

## Persian text

Follow the wording, spelling and punctuation already in the repository. When you
add a passage or rewrite one, match the surrounding text instead of bringing
your own conventions to it. This covers the README, the comments in the YAML
files, and every value shown to a reader.

**The brand name takes a real space, not a ZWNJ:** `پیام رسان`. The joined form
is the common noun for social messaging apps and collides with the brand.

Where the brand is first introduced, use the full phrase
**پنل پیامکی پیام رسان**.

Every README carries `payam-resan.com` in the footer, written out and linked,
not merely a link sitting on the brand name.

## Style

- The prose is Persian. Field names and method names are English, spelled
  exactly as the service spells them.
- The description of a method says **when to reach for it**, rather than listing
  its parameters. The schema already lists the parameters.
- Where a method has a better alternative, say so. `Send` puts the key in the
  URL, so `SendBulk` is the one for production.

## Git

Semantic messages, `type(scope): subject`, with no explanatory body and no
mention of any tool or assistant. Do not commit without explicit approval.
