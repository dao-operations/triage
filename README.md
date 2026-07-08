# DAO-ops Triage

Public work tracker for `DAO-ops/triage`.

This repo is the public ledger for DAO-ops work: intake, triage, planning, blockers, decisions, and visible progress. It deliberately stays inside GitHub Issues + one GitHub Project so two maintainers can run it without another project-management system.

## Start here

- System spec: [`SPEC.md`](SPEC.md)
- Setup guide: [`docs/setup.md`](docs/setup.md)
- Project views: [`docs/project-views.md`](docs/project-views.md)
- Taxonomy/config: [`config/triage.toml`](config/triage.toml)
- Agent instructions: [`AGENTS.md`](AGENTS.md)
- Codex setup: [`docs/codex.md`](docs/codex.md)

## Repo and Project

Recommended repository:

```text
DAO-ops/triage
```

Recommended GitHub Project:

```text
DAO-ops Tracker
```

## Quick setup

```bash
gh auth refresh -s project
make bootstrap OWNER=DAO-ops REPO=triage
make check OWNER=DAO-ops REPO=triage
```

Then open the Project UI, verify the `Status` options, create the saved views in `docs/project-views.md`, and enable the built-in Project workflows listed in `docs/setup.md`. For Codex, see `docs/codex.md`; the repo-level `AGENTS.md` is already prepared.

## Daily use

1. Capture work as an issue.
2. Triage Inbox issues into clear labels and Project fields.
3. Keep `Next` small and `Doing` smaller.
4. Comment when blocked.
5. Close aggressively when done, duplicated, invalid, private, or obsolete.
6. Post one public weekly update.

## Public-safety rule

This repo is public. Do not post secrets, private URLs, private commercial context, personal data, exploitable security detail, signer/control details, or legal/tax-sensitive material unless it is intentionally public.

When in doubt, write a public-safe placeholder issue and track the sensitive details privately.
