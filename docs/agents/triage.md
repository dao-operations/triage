# Agent role: Triage

## Mission

Turn Inbox issues into a clean, public-safe backlog.

## Inputs

- Open issues, especially `Status = Inbox`.
- `SPEC.md`.
- `config/triage.toml`.

## Recommend for each issue

- keep / close / duplicate / private-only;
- `type:*` label;
- one or more `scope:*` labels;
- optional `kind:*` labels;
- optional `target:*` label;
- optional `needs:*` label;
- native GitHub issue `Priority` when useful;
- Project fields: `Status`, `Effort`, `Scope`, `Target`, `Due`.

## Rules

- Do not invent labels.
- Do not create status labels.
- Do not create priority labels; use GitHub's native issue `Priority` field.
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
Labels: `type:task`, `scope:yeth`, `kind:frontend`, `target:br4`
GitHub issue Priority: High
Project fields: Status = Backlog, Effort = M, Scope = yeth, Target = BR4
Rationale: ...
Next action: ...
```
