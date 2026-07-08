# Setup

## Prerequisites

- GitHub CLI authenticated for the target org.
- Python 3.11+.
- Permission to create/update labels and organization Projects.

Refresh GitHub CLI project scope:

```bash
gh auth refresh -s project
```

## Create or prepare the repo

If the repo does not exist yet:

```bash
gh repo create DAO-ops/triage \
  --public \
  --description "Public DAO-ops triage and work tracker"
```

Then commit this skeleton into `DAO-ops/triage`.

## Bootstrap labels and Project fields

```bash
make bootstrap OWNER=DAO-ops REPO=triage
```

Equivalent direct command:

```bash
./scripts/bootstrap.py \
  --owner DAO-ops \
  --repo triage \
  --project-title "DAO-ops Tracker"
```

Use dry-run first if desired:

```bash
make bootstrap OWNER=DAO-ops REPO=triage DRY_RUN=1
# or
./scripts/bootstrap.py --owner DAO-ops --repo triage --dry-run
```

## Manual Project setup

Open the created Project and verify:

1. Project title is `DAO-ops Tracker`.
2. `Status` has exactly: `Inbox`, `Backlog`, `Next`, `Doing`, `Blocked`, `Done`.
3. Custom fields exist: `Priority`, `Effort`, `Scope`, `Target`, `Due`.
4. Saved views match `docs/project-views.md`.

`Status` often exists on new Projects by default, so scripts warn instead of destructively mutating it.

## Built-in Project workflows

Enable or verify these in the Project UI:

- item added -> `Status = Inbox`;
- closed issue -> `Status = Done`;
- merged PR -> `Status = Done`;
- auto-add issues from `DAO-ops/triage` with filter `is:issue`.

Avoid custom Actions for Project item mutation until manual operation becomes painful.

## Check taxonomy

```bash
make check OWNER=DAO-ops REPO=triage
```

Strict mode also fails on open issues missing `scope:*`:

```bash
make check-strict OWNER=DAO-ops REPO=triage
```

The default scheduled workflow runs non-strict checks so fresh Inbox issues do not fail CI solely because they are not fully triaged yet.

## Optional Codex setup

This skeleton includes `AGENTS.md` for Codex/project-agent guidance. After the repo is committed, see `docs/codex.md` for local Codex CLI and Codex Cloud setup.
