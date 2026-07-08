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
- optional `priority:*` label;
- optional `target:*` label;
- optional `needs:*` label;
- Project fields: `Status`, `Priority`, `Effort`, `Scope`, `Target`, `Due`.

## Rules

- Do not invent labels.
- Do not create status labels.
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
Labels: `type:task`, `scope:yeth`, `kind:frontend`, `priority:p1`, `target:br4`
Project fields: Status = Backlog, Priority = P1, Effort = M, Scope = yeth, Target = BR4
Rationale: ...
Next action: ...
```
