# DAO-ops Triage Spec

## 1. Purpose

`dao-operations/triage` is the public work ledger for a small DAO-ops tracking team.

It exists to:

- capture public work in one canonical place;
- show what is planned, active, blocked, decided, shipped, parked, or rejected;
- keep budget-request targeting visible without pretending everything is committed;
- avoid a second project-management tool.

It is not a private planning system. Anything sensitive, security-relevant, signer-sensitive, commercially confidential, personally identifying, privileged, legal/tax-sensitive, or otherwise unsafe for public tracking belongs outside this repository.

## 2. The 80/20 model

Use exactly three durable layers:

1. **Issues** are the work items and decision records.
2. **Labels** are the public taxonomy that stays useful on the normal Issues page.
3. **One GitHub Project** is the operating board and saved-view layer.

Do not create more boards, mirrored status labels, or complicated sync jobs until repeated manual pain proves they are needed.

## 3. Naming

Repository:

```text
dao-operations/triage
```

Project:

```text
DAO-ops Tracker
```

Owner: `dao-operations` organization Project, linked to `dao-operations/triage`.

Visibility: public.

Rationale: `triage` is short, action-oriented, and honest about the repo's job. `planning` sounds more strategic than this system should be. `tracking` is accurate but too generic inside the `dao-operations` org.

## 4. Repository structure

```text
triage/
  README.md
  SPEC.md
  ROADMAP.md
  CHANGELOG.md
  CONTRIBUTING.md
  AGENTS.md
  Makefile
  .editorconfig
  .gitignore
  .github/
    ISSUE_TEMPLATE/
      issue.md
      config.yml
    workflows/
      taxonomy-check.yml
    PULL_REQUEST_TEMPLATE.md
  config/
    triage.toml
  docs/
    setup.md
    project-views.md
    weekly-update-template.md
    agents/
      triage.md
      issue-refinement.md
      target-planning.md
      weekly-update.md
  scripts/
    _common.py
    bootstrap.py
    sync-labels.py
    sync-project-fields.py
    check-taxonomy.py
```

## 5. Project fields

### `Status`

Type: single select.

Values:

```text
Inbox
Backlog
Next
Doing
Blocked
Done
```

| Status | Meaning |
|---|---|
| `Inbox` | New or untriaged intake. Labels and fields may be incomplete. |
| `Backlog` | Valid work that is not selected for near-term execution. |
| `Next` | Ready or nearly ready work queued for near-term pull. |
| `Doing` | Work actively in progress. |
| `Blocked` | Work waiting on a dependency, decision, access, input, or review. |
| `Done` | Work closed with a final outcome. |

Keep `Inbox` near zero, `Next` under five, and `Doing` at one or two items per person.

### `Scope`

Type: single select.

Values:

```text
styfi
veyfi
yeth
teams
ybc
dao
treasury
governance
operations
```

When an issue spans more than one scope, apply multiple `scope:*` labels. Set Project `Scope` to the primary scope if one is obvious; otherwise leave it blank until triage chooses one.

### `Target`

Type: single select.

Values:

```text
BR3
BR4
BR5
Later
```

`Target` answers: which budget-request bucket is this issue aimed at?

A target means “intended for this bucket,” not “guaranteed to ship.” Blank means not assigned. `Later` means valid and explicitly deferred beyond the currently tracked BRs.

### `Due`

Type: date.

Use only for real external deadlines: votes, launches, reporting dates, grant deadlines, vendor dates, or public commitments. Do not fill it just because work would be nice to finish soon.

## 6. Native GitHub issue fields

Use native GitHub issue metadata for cross-repo classification. Do not duplicate these as labels or custom Project fields.

### Issue Type

Values used by this repo:

```text
Task
Bug
Feature
Idea
Decision
```

| Issue Type | Meaning |
|---|---|
| `Task` | Concrete work item with a clear completion signal. |
| `Bug` | Incorrect or broken behavior that should be fixed. |
| `Feature` | Request for new or changed functionality. |
| `Idea` | Potential improvement or future work needing refinement. |
| `Decision` | Decision record or open question requiring an explicit answer. |

### Priority

Use GitHub's native issue `Priority` field for priority. Do not create `priority:*` labels or a custom Project `Priority` field.

### Effort

Use GitHub's native issue `Effort` field for sizing when useful. Do not create `effort:*` labels or a custom Project `Effort` field.

Values:

```text
High
Medium
Low
```

| Effort | Meaning |
|---|---|
| `Low` | Small, straightforward work. |
| `Medium` | Moderate work that needs planning or coordination. |
| `High` | Large, complex, cross-cutting, or discovery-heavy work. |
| blank | Effort not worth tracking yet. |

## 7. Labels

Labels are lowercase kebab-case with namespaces. Labels classify issues; Project `Status` tracks workflow. The `Meaning` text below is the source of truth for GitHub label descriptions in `config/triage.toml`.

### Scope labels

Use one or more once triaged.

```text
scope:styfi
scope:veyfi
scope:yeth
scope:teams
scope:ybc
scope:dao
scope:treasury
scope:governance
scope:operations
```

| Label | Meaning |
|---|---|
| `scope:styfi` | Work primarily related to styfi. |
| `scope:veyfi` | Work primarily related to veyfi. |
| `scope:yeth` | Work primarily related to yeth. |
| `scope:teams` | Work primarily related to teams-facing systems. |
| `scope:ybc` | Work primarily related to ybc. |
| `scope:dao` | Work primarily related to DAO-facing surfaces. |
| `scope:treasury` | Work primarily related to treasury operations or reporting. |
| `scope:governance` | Work primarily related to governance process or coordination. |
| `scope:operations` | Work primarily related to recurring operations, process, or repo hygiene. |

Use both `scope:dao` and `scope:governance` if work touches `dao.yearn.fi` and the governance process.

### Kind labels

Optional. Use only when they add signal.

```text
kind:frontend
kind:backend
kind:contracts
kind:data
kind:ops
kind:research
kind:admin
```

| Label | Meaning |
|---|---|
| `kind:frontend` | Frontend, UI, or user-experience work. |
| `kind:backend` | Backend, API, indexing, or service work. |
| `kind:contracts` | Smart contract, deployment, or on-chain integration work. |
| `kind:data` | Analytics, reporting, export, or data pipeline work. |
| `kind:ops` | Operational execution, runbook, deployment, or support work. |
| `kind:research` | Investigation, analysis, or design exploration. |
| `kind:admin` | Coordination, tracking, documentation, or repository hygiene. |

### Target labels

Use zero or one.

```text
target:br3
target:br4
target:br5
target:later
```

These mirror the Project `Target` field.

| Label | Meaning |
|---|---|
| `target:br3` | Intended for the BR3 target window. |
| `target:br4` | Intended for the BR4 target window. |
| `target:br5` | Intended for the BR5 target window. |
| `target:later` | Valid work deferred beyond active target windows. |

### Needs labels

Optional. Use these to make blockers visible on the Issues page without creating status labels.

```text
needs:decision
needs:input
needs:access
needs:review
```

| Label | Meaning |
|---|---|
| `needs:decision` | Waiting on a decision. |
| `needs:input` | Waiting on input or clarification. |
| `needs:access` | Waiting on access or permission. |
| `needs:review` | Waiting on review. |

When an issue is blocked, set Project `Status = Blocked`, add the relevant `needs:*` label if useful, and leave a blocker comment.

## 8. Labels deliberately not used

Do not create these initially:

```text
type:*
status:*
priority:*
effort:*
br:*
area:*
br:unscheduled
bug
documentation
duplicate
enhancement
good first issue
help wanted
invalid
question
wontfix
```

Reasons:

- Issue classification belongs in GitHub's native issue type, not in labels.
- Status belongs in the Project `Status` field, not in labels.
- Priority belongs in GitHub's native issue `Priority` field, not in labels.
- Effort belongs in GitHub's native issue `Effort` field, not in labels or Project fields.
- `target:*` replaces the older `br:*` namespace and works if targets later stop being BR-only.
- `area:*` overlaps with `scope:*` and `kind:*`.
- Default GitHub labels are too broad for this tracker; use the namespaced taxonomy instead.

## 9. Issue templates

Use one minimal template named `Issue`.

The template does not set labels, require body fields, or add title prefixes. Title-only issues are acceptable at intake. Choose the native issue type manually in the GitHub issue UI, then let triage add detail, labels, and fields when needed.

## 10. Views

Create saved Project views manually once. Recommended views are in `docs/project-views.md`.

Initial set:

1. **Board** — grouped by `Status`.
2. **Focus** — `Next`, `Doing`, and `Blocked` only.
3. **Blocked** — blocked issues grouped by `needs:*` or `Scope`.
4. **By target** — grouped by `Target`.
5. **By scope** — grouped by `Scope`.
6. **Bugs** — native issue type `Bug`, grouped by `Status`.
7. **Done** — recently closed/completed items.

Avoid BR-specific views unless they are actively used. A grouped `By target` view is usually enough.

## 11. Operating process

### Capture

Create an issue for anything that may need doing, deciding, explaining, remembering, or showing publicly.

New issues start as `Inbox`. The creator does not need to classify perfectly.

### Triage

Run triage once or twice per week.

For each Inbox issue:

1. Close it if duplicate, obsolete, unsafe for public tracking, invalid, too vague, or not actionable.
2. Set the native GitHub issue type.
3. Add one or more `scope:*` labels if the issue stays open.
4. Add `kind:*` labels only when useful.
5. Set native GitHub issue `Priority` and `Effort` when useful.
6. Add at most one `target:*` label if the work is targeted.
7. Set Project fields: `Status`, `Scope`, `Target`, `Due`.
8. Move to `Backlog`, `Next`, `Blocked`, or `Done`.

### Planning a target / BR

Before a new BR or target window:

1. Review `Backlog`, `Next`, high-priority, urgent, and blocked issues.
2. Select fewer issues than feels comfortable.
3. Apply the relevant `target:*` label and Project `Target` value.
4. Keep only near-term pullable work in `Next`.
5. Use `target:later` for valid work explicitly deferred beyond active BRs.

### Working

When starting work:

1. Assign yourself.
2. Move the issue to `Doing`.
3. Link PRs where applicable.
4. Use closing keywords in PRs when the PR truly completes the issue.

Example:

```md
Closes #123
```

### Blocking

When blocked:

1. Move to `Blocked`.
2. Add `needs:*` if useful.
3. Leave a short blocker comment.

Recommended format:

```md
Blocked on: [decision / access / external input / review / dependency].

Next action: [person/team] to [action] by [date if real].
```

### Done / closed

When work is done, rejected, duplicated, private-only, or obsolete:

1. Close the issue.
2. Ensure Project `Status = Done`.
3. Add a short closing comment if the outcome is not obvious.
4. Add a `CHANGELOG.md` entry only for externally meaningful progress.

### Weekly public update

Use `docs/weekly-update-template.md` as a pinned issue comment.

Keep it factual:

- shipped;
- in progress;
- blocked;
- next;
- decisions.

If nothing meaningful changed, say so plainly.

## 12. Invariants

- One repo.
- One GitHub Project.
- One canonical issue tracker.
- No mirrored status labels.
- Triaged issues use a native GitHub issue type, not a `type:*` label.
- At least one `scope:*` label on triaged open issues.
- At most one `target:*` label.
- `kind:*` and `needs:*` are optional.
- `Next` is small.
- `Doing` is smaller.
- `Blocked` always has a comment explaining the blocker.
- Close aggressively.
- Public context beats silent board movement.

## 13. Automation boundary

Automate:

- repo label creation/update;
- Project creation;
- creation of missing Project fields;
- taxonomy checks;
- built-in Project workflows for closed/merged -> `Done` and auto-add.

Do not initially automate:

- status-label mirroring;
- forced label-to-field sync;
- Project view creation;
- complex form parsing;
- issue field administration at the organization level.

The organization owns native issue types and issue fields. This repo consumes those fields, but the bootstrap scripts do not create or mutate organization-level issue metadata.

## 14. Setup order

1. Commit this skeleton into `dao-operations/triage`.
2. Run `gh auth refresh -s project`.
3. Run `make bootstrap OWNER=dao-operations REPO=triage`.
4. Open the created organization Project.
5. Verify `Status` options manually.
6. Verify native issue types: `Task`, `Bug`, `Feature`, `Idea`, `Decision`.
7. Verify native issue fields: `Priority`, `Effort`.
8. Create the saved views in `docs/project-views.md`.
9. Enable built-in Project workflows.
10. Run `make check OWNER=dao-operations REPO=triage`.
11. Start using it.

## 15. When to evolve this system

Add complexity only after repeated manual pain.

Good reasons to evolve:

- more than two maintainers actively triaging;
- external contributors are confused by the taxonomy;
- Project status and labels drift often;
- weekly updates are hard to produce;
- BR planning needs historical metrics.

Bad reasons:

- a label might be useful someday;
- every field should be represented everywhere;
- the board should encode every possible state;
- the system should look like a mature PMO.
