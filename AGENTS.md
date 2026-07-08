# AGENTS.md

This repository is a public DAO-ops tracker. Preserve the system's simplicity.

## Prime directive

Do not turn this repo into heavyweight project management.

Preserve:

- one repo;
- one GitHub Project;
- issues as work items and decision records;
- labels as public taxonomy;
- Project fields as board/view metadata;
- minimal automation;
- public-safe content.

## Public-safety rules

Never add or suggest adding these to public issues:

- credentials, tokens, mnemonics, passwords, private RPC URLs;
- undisclosed vulnerabilities with exploitable detail;
- signer, wallet-control, or operational-security details;
- private commercial terms;
- personal data;
- privileged legal/tax material.

If a request contains sensitive material, rewrite it into a public-safe placeholder and recommend private tracking for details.

## Taxonomy

Use `SPEC.md` and `config/triage.toml`.

Allowed namespaces:

- `type:*`
- `scope:*`
- `kind:*`
- `target:*`
- `needs:*`

Do not create status labels. Do not create priority labels; use GitHub's native issue Priority field. Do not use `br:*`; use `target:*`.

## Issue quality bar

Title-only issues are acceptable at intake. A good triaged issue has:

- clear title;
- desired outcome;
- context;
- acceptance criteria or completion signal;
- public-safe language;
- useful labels and Project fields after triage.

Split issues that combine unrelated work. Close issues that cannot become actionable.

## Agent roles

Focused prompts live in `docs/agents/`. Codex setup guidance lives in `docs/codex.md`.

Focused prompts:

- `triage.md`
- `issue-refinement.md`
- `target-planning.md`
- `weekly-update.md`

## Changing the system

When changing taxonomy or process:

1. Update `SPEC.md`.
2. Update `config/triage.toml`.
3. Update scripts and docs.
4. Explain migration impact.
5. Prefer additive changes over destructive renames.
