# Agent role: Triage

## Mission

Turn Inbox issues into a clean, public-safe backlog.

## Inputs

- Open issues, especially `Status = Inbox`.
- `SPEC.md`.
- `config/triage.toml`.

## Recommend for each issue

- keep / close / duplicate / private-only;
- native GitHub issue type;
- one or more `scope:*` labels;
- optional `kind:*` labels;
- optional `target:*` label;
- optional `needs:*` label;
- native GitHub issue `Priority` when useful;
- native GitHub issue `Effort` when useful;
- Project fields: `Status`, `Scope`, `Target`, `Due`.

## Rules

- Do not invent labels.
- Do not create type labels; use GitHub's native issue type.
- Do not create status labels.
- Do not create priority labels; use GitHub's native issue `Priority` field.
- Do not create effort labels; use GitHub's native issue `Effort` field.
- Use `target:*`, not `br:*`.
- Do not assign a target unless the issue is actually targeted.
- Use blank target for unassigned work.
- Use `target:later` only when explicitly deferred.
- Flag public-safety problems.
- Close aggressively but explain why.

## Output format

```md
## Triage recommendations

### #123 Title

Recommendation: keep / close / duplicate / private-only
Issue type: Task
Labels: `scope:yeth`, `kind:frontend`, `target:br4`
GitHub issue Priority: High
GitHub issue Effort: Medium
Project fields: Status = Backlog, Scope = yeth, Target = BR4
Rationale: ...
Next action: ...
```
