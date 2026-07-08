# Project views

Create these saved views manually in the GitHub Project UI.

## 1. Board

Layout: board.

Group by: `Status`.

Visible fields:

- `Effort`
- `Scope`
- `Target`
- `Due`
- Assignees
- Labels

Purpose: default operating board.

## 2. Focus

Filter:

```text
status:Next,Doing,Blocked
```

Group by: `Status`.

Sort: due date ascending, then recently updated.

Purpose: what the two maintainers actually need to look at.

## 3. Blocked

Filter:

```text
status:Blocked
```

Group by: `Scope` or Labels.

Visible fields: `Target`, `Due`, Assignees, Labels.

Purpose: make external input, access, review, dependencies, and decisions visible.

## 4. By target

Filter:

```text
is:open
```

Group by: `Target`.

Purpose: BR planning and public target visibility without one view per BR.

## 5. By scope

Filter:

```text
is:open
```

Group by: `Scope`.

Purpose: see work by product/domain/workstream.

## 6. Bugs

Filter:

```text
label:"type:bug" is:open
```

Group by: `Status`.

Purpose: defects by workflow state.

## 7. Done

Filter:

```text
status:Done
```

Sort: recently updated first.

Purpose: public progress and weekly update review.

## Notes

Use the Project filter bar autocomplete if exact filter syntax differs in the UI. Avoid creating more views until one of these is clearly insufficient.
