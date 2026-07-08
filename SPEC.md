# DAO-ops Triage Spec

## 1. Purpose

`DAO-ops/triage` is the public work ledger for a small DAO-ops tracking team.

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
DAO-ops/triage
```

Project:

```text
DAO-ops Tracker
```

Rationale: `triage` is short, action-oriented, and honest about the repo's job. `planning` sounds more strategic than this system should be. `tracking` is accurate but too generic inside the `DAO-ops` org.

## 4. Repository structure

```text
triage/
  README.md
  SPEC.md
  ROADMAP.md
  CHANGELOG.md
  SECURITY.md
  CONTRIBUTING.md
  AGENTS.md
  Makefile
  .editorconfig
  .gitignore
  .github/
    ISSUE_TEMPLATE/
      task.yml
      bug.yml
      idea.yml
      decision.yml
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
| `Inbox` | New or untriaged. No one should rely on its labels yet. |
| `Backlog` | Valid public work, not actively planned. |
| `Next` | Small near-term queue. Candidate for the next work pull. |
| `Doing` | Actively being worked by someone. |
| `Blocked` | Cannot progress without input, access, review, dependency, approval, or decision. |
| `Done` | Completed, rejected, superseded, duplicated, private-only, or no longer relevant. |

Keep `Inbox` near zero, `Next` under five, and `Doing` at one or two items per person.

### `Priority`

Type: single select.

Values:

```text
P0
P1
P2
P3
```

| Priority | Meaning |
|---|---|
| `P0` | Interrupt-level: active incident, severe blocker, deadline, or public commitment risk. |
| `P1` | Important and should be deliberately planned. |
| `P2` | Normal useful backlog work. |
| `P3` | Opportunistic cleanup, polish, or nice-to-have. |
| blank | Not triaged or priority not useful. |

Do not add `P4`. Low-priority work is `P3`, `Backlog`, or `target:later`.

### `Effort`

Type: single select.

Values:

```text
S
M
L
Unknown
```

| Effort | Meaning |
|---|---|
| `S` | Less than half a day. |
| `M` | Roughly one to two days. |
| `L` | Several days, cross-cutting, risky, or coordination-heavy. |
| `Unknown` | Needs discovery before sizing. |
| blank | Effort not worth tracking. |

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

## 6. Labels

Labels are lowercase kebab-case with namespaces. Labels classify issues; Project `Status` tracks workflow. The `Meaning` text below is the source of truth for GitHub label descriptions in `config/triage.toml`.

### Type labels

Use exactly one.

```text
type:task
type:bug
type:idea
type:decision
```

| Label | Meaning |
|---|---|
| `type:task` | Concrete work item. |
| `type:bug` | Broken or incorrect behavior. |
| `type:idea` | Suggestion, rough improvement, or possible future work. |
| `type:decision` | Public decision that needs an explicit answer. |

### Priority labels

Use zero or one.

```text
priority:p0
priority:p1
priority:p2
priority:p3
```

| Label | Meaning |
|---|---|
| `priority:p0` | Interrupt-level blocker or deadline risk. |
| `priority:p1` | Important and should be planned. |
| `priority:p2` | Normal useful backlog work. |
| `priority:p3` | Opportunistic cleanup or polish. |

Mirror the Project `Priority` field when useful. If they drift, fix both during triage.

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
| `scope:styfi` | styfi / `styfi.yearn.fi`. |
| `scope:veyfi` | veyfi / `veyfi.yearn.fi`. |
| `scope:yeth` | yeth app, protocol, contracts, research, or operations. |
| `scope:teams` | teams app or teams-facing surface. |
| `scope:ybc` | ybc app/domain. |
| `scope:dao` | `dao.yearn.fi` or dao-facing product surface. |
| `scope:treasury` | treasury admin, accounting, capital allocation, reporting. |
| `scope:governance` | YIPs, votes, proposals, approvals, delegates, voter coordination. |
| `scope:operations` | Recurring ops, team process, reporting, tracking, public updates, repo hygiene. |

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
| `kind:frontend` | UI, UX, frontend app work. |
| `kind:backend` | APIs, indexing, databases, backend services. |
| `kind:contracts` | Smart contracts, deployments, on-chain integration/review. |
| `kind:data` | Data extraction, analytics, dashboards, exports, reporting pipelines. |
| `kind:ops` | Runbooks, monitoring, deployments, support, operational execution. |
| `kind:research` | Investigation, analysis, design exploration. |
| `kind:admin` | Coordination, repository hygiene, public updates, budget-process admin. |

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
| `target:br3` | Targeted for BR3. |
| `target:br4` | Targeted for BR4. |
| `target:br5` | Targeted for BR5. |
| `target:later` | Valid but explicitly deferred beyond active BRs. |

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
| `needs:decision` | Blocked or waiting on a decision. |
| `needs:input` | Blocked or waiting on external input. |
| `needs:access` | Blocked or waiting on access/permissions. |
| `needs:review` | Blocked or waiting on review. |

When an issue is blocked, set Project `Status = Blocked`, add the relevant `needs:*` label if useful, and leave a blocker comment.

## 7. Labels deliberately not used

Do not create these initially:

```text
status:*
br:*
area:*
priority:p4
br:unscheduled
```

Reasons:

- Status belongs in the Project `Status` field, not in labels.
- `target:*` replaces the older `br:*` namespace and works if targets later stop being BR-only.
- `area:*` overlaps with `scope:*` and `kind:*`.
- `priority:p4` overlaps with `Backlog`, blank `Target`, and `target:later`.

## 8. Issue templates

Use four templates:

- Task
- Bug
- Idea
- Decision

Templates set only the `type:*` label. Scope, priority, effort, target, due date, and needs labels are triage decisions.

Every template asks for public-safe content. The checkbox is not legal cover; it is a friction point to prevent accidental leakage.

## 9. Views

Create saved Project views manually once. Recommended views are in `docs/project-views.md`.

Initial set:

1. **Board** — grouped by `Status`.
2. **Focus** — `Next`, `Doing`, and `Blocked` only.
3. **Blocked** — blocked issues grouped by `needs:*` or `Scope`.
4. **By target** — grouped by `Target`.
5. **By scope** — grouped by `Scope`.
6. **Done** — recently closed/completed items.

Avoid BR-specific views unless they are actively used. A grouped `By target` view is usually enough.

## 10. Operating process

### Capture

Create an issue for anything that may need doing, deciding, explaining, remembering, or showing publicly.

New issues start as `Inbox`. The creator does not need to classify perfectly.

### Triage

Run triage once or twice per week.

For each Inbox issue:

1. Close it if duplicate, obsolete, unsafe for public tracking, invalid, too vague, or not actionable.
2. Ensure exactly one `type:*` label.
3. Add one or more `scope:*` labels if the issue stays open.
4. Add `kind:*` labels only when useful.
5. Add at most one `priority:*` label.
6. Add at most one `target:*` label if the work is targeted.
7. Set Project fields: `Status`, `Priority`, `Effort`, `Scope`, `Target`, `Due`.
8. Move to `Backlog`, `Next`, `Blocked`, or `Done`.

### Planning a target / BR

Before a new BR or target window:

1. Review `Backlog`, `Next`, P0/P1, and blocked issues.
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

## 11. Invariants

- One repo.
- One GitHub Project.
- One canonical issue tracker.
- No mirrored status labels.
- Exactly one `type:*` label on triaged issues.
- At least one `scope:*` label on triaged open issues.
- At most one `priority:*` label.
- At most one `target:*` label.
- `kind:*` and `needs:*` are optional.
- `Next` is small.
- `Doing` is smaller.
- `Blocked` always has a comment explaining the blocker.
- Close aggressively.
- Public context beats silent board movement.

## 12. Automation boundary

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
- issue fields at the organization level.

GitHub issue fields are a possible later upgrade if the organization standardizes them, but the initial system uses labels + Project fields because they are portable, scriptable, and easy to understand.

## 13. Setup order

1. Commit this skeleton into `DAO-ops/triage`.
2. Run `gh auth refresh -s project`.
3. Run `make bootstrap OWNER=DAO-ops REPO=triage`.
4. Open the created Project.
5. Verify `Status` options manually.
6. Create the saved views in `docs/project-views.md`.
7. Enable built-in Project workflows.
8. Run `make check OWNER=DAO-ops REPO=triage`.
9. Start using it.

## 14. When to evolve this system

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
