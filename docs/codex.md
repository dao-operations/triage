# Codex setup

This repo is already prepared for Codex through the top-level `AGENTS.md`. Do not run `/init` over it unless you intentionally want to regenerate that file.

## Local Codex CLI

Install Codex CLI on macOS/Linux:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Alternative installers:

```bash
npm install -g @openai/codex
brew install --cask codex
```

Then clone and enter the repo:

```bash
gh repo clone dao-operations/triage
cd triage
```

Start Codex:

```bash
codex
```

On first run, sign in with your ChatGPT account or API key.

## First local prompt

Use this as the first prompt in the repo:

```text
Read AGENTS.md, SPEC.md, config/triage.toml, and docs/setup.md.
Summarize the operating model and list the exact checks you would run before changing anything.
Do not edit files yet.
```

Then use small, bounded tasks:

```text
Using docs/agents/triage.md, review the open issues and suggest label/project-field changes.
Do not apply changes directly; output the gh commands I should review first.
```

```text
Update SPEC.md and config/triage.toml for this taxonomy change: <change>.
Run make check locally if possible.
Keep the system simple and explain migration impact.
```

```text
Prepare this week's public update using docs/weekly-update-template.md.
Use only public-safe issue/PR information.
```

## Recommended permissions

Start conservative. Let Codex read and edit the local checkout, but require approval before it runs commands that touch GitHub state. For this repo, commands that change GitHub state include:

- `gh label create` / `gh label edit`;
- `gh project create`;
- `gh project field-create`;
- `gh issue edit`;
- `gh pr create`;
- `git push`.

Use dry-runs first:

```bash
make bootstrap OWNER=dao-operations REPO=triage DRY_RUN=1
make check OWNER=dao-operations REPO=triage
```

## Codex Cloud / GitHub review

For cloud tasks and PR review:

1. Open Codex in ChatGPT.
2. Connect the GitHub repo `dao-operations/triage` in Codex environment settings.
3. Ensure the environment can run Python 3.11+ and GitHub CLI if you expect it to run the setup scripts.
4. Enable Codex code review for the repo if you want PR reviews.
5. In a pull request, comment:

```text
@codex review
```

For one-off focused reviews:

```text
@codex review for taxonomy drift and public-safety regressions
```

## Two-person operating pattern

- Person A uses Codex CLI for local edits to docs, scripts, and weekly-update drafts.
- Person B uses GitHub PR review plus `@codex review` for a second pass.
- Only humans run final `make bootstrap` against the live repo until there is repeated pain worth automating.

## Good Codex tasks for this repo

- review issue intake friction;
- compare `SPEC.md` and `config/triage.toml`;
- draft weekly updates;
- propose labels for a batch of issues;
- generate migration notes after taxonomy changes;
- review PRs for public-safety leakage.

## Bad Codex tasks for this repo

- mass-edit live issues without a reviewed command list;
- create new Projects or labels without dry-run output;
- infer private context from public placeholders;
- add process complexity because it is technically possible.
