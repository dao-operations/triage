from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "triage.toml"


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def require_gh() -> None:
    if shutil.which("gh") is None:
        print("GitHub CLI 'gh' not found on PATH.", file=sys.stderr)
        sys.exit(2)


def run(cmd: list[str], *, dry_run: bool = False, check: bool = True) -> subprocess.CompletedProcess[str] | None:
    print("+", shlex.join(cmd))
    if dry_run:
        return None
    result = subprocess.run(cmd, text=True, capture_output=True)
    if check and result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    return result


def gh_json(cmd: list[str], *, dry_run: bool = False) -> Any:
    result = run(cmd, dry_run=dry_run)
    if dry_run or result is None or not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--owner", default=os.environ.get("OWNER"), help="GitHub org/user owner. Default: config or OWNER env.")
    parser.add_argument("--repo", default=os.environ.get("REPO"), help="Repository name. Default: config or REPO env.")
    parser.add_argument("--project-title", default=os.environ.get("PROJECT_TITLE"), help="GitHub Project title. Default: config or PROJECT_TITLE env.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")


def resolve_owner_repo_project(args: argparse.Namespace, config: dict[str, Any]) -> tuple[str, str, str]:
    owner = args.owner or config.get("repo", {}).get("owner")
    repo = args.repo or config.get("repo", {}).get("name")
    project_title = args.project_title or config.get("project", {}).get("title")
    missing = [name for name, value in (("owner", owner), ("repo", repo), ("project_title", project_title)) if not value]
    if missing:
        print(f"Missing required value(s): {', '.join(missing)}", file=sys.stderr)
        sys.exit(2)
    return str(owner), str(repo), str(project_title)


def full_repo(owner: str, repo: str) -> str:
    return f"{owner}/{repo}"


def label_description(label: dict[str, str]) -> str:
    """Return the configured GitHub label description verbatim, after trimming whitespace."""
    description = label.get("description", "").strip()
    if not description:
        return "See SPEC.md."
    return description


def sync_labels(owner: str, repo: str, labels: list[dict[str, str]], *, dry_run: bool = False) -> None:
    repository = full_repo(owner, repo)
    existing = gh_json([
        "gh", "label", "list",
        "--repo", repository,
        "--json", "name",
        "--limit", "1000",
    ], dry_run=dry_run) or []
    names = {item["name"] for item in existing if "name" in item}

    for label in labels:
        name = label["name"]
        color = label["color"]
        description = label_description(label)
        if name in names:
            run([
                "gh", "label", "edit", name,
                "--repo", repository,
                "--color", color,
                "--description", description,
            ], dry_run=dry_run)
        else:
            run([
                "gh", "label", "create", name,
                "--repo", repository,
                "--color", color,
                "--description", description,
            ], dry_run=dry_run)


def get_project_number(owner: str, title: str, *, dry_run: bool = False) -> int | None:
    data = gh_json(["gh", "project", "list", "--owner", owner, "--format", "json"], dry_run=dry_run)
    for project in (data or {}).get("projects", []):
        if project.get("title") == title:
            return int(project["number"])
    return None


def create_project(owner: str, title: str, *, dry_run: bool = False) -> int | None:
    data = gh_json([
        "gh", "project", "create",
        "--owner", owner,
        "--title", title,
        "--format", "json",
    ], dry_run=dry_run)
    if dry_run:
        return None
    return int(data["number"])


def find_or_create_project(owner: str, title: str, *, dry_run: bool = False) -> int | None:
    number = get_project_number(owner, title, dry_run=dry_run)
    if number is not None:
        print(f"Project exists: {title} (#{number})")
        return number
    print(f"Creating project: {title}")
    return create_project(owner, title, dry_run=dry_run)


def option_names(field: dict[str, Any]) -> list[str]:
    raw = field.get("options") or field.get("configuration", {}).get("options") or []
    names: list[str] = []
    for option in raw:
        if isinstance(option, dict):
            name = option.get("name")
            if name:
                names.append(str(name))
        else:
            names.append(str(option))
    return names


def sync_project_fields(owner: str, project_number: int | None, fields: list[dict[str, Any]], *, dry_run: bool = False) -> None:
    if project_number is None and dry_run:
        project_number = 0
    if project_number is None:
        print("Cannot sync fields without a project number.", file=sys.stderr)
        sys.exit(2)

    data = gh_json([
        "gh", "project", "field-list", str(project_number),
        "--owner", owner,
        "--format", "json",
    ], dry_run=dry_run) or {"fields": []}

    existing_by_name = {field.get("name"): field for field in data.get("fields", []) if field.get("name")}

    for wanted in fields:
        name = wanted["name"]
        existing = existing_by_name.get(name)
        if existing:
            print(f"Field exists: {name}")
            wanted_options = wanted.get("options") or []
            existing_options = option_names(existing)
            if wanted_options and existing_options:
                missing = [opt for opt in wanted_options if opt not in existing_options]
                if missing:
                    print(f"WARNING: field {name!r} is missing option(s) {missing}. Update manually in the Project UI.")
            elif wanted.get("manual_verify"):
                print(f"NOTE: verify {name!r} options manually in the Project UI.")
            continue

        cmd = [
            "gh", "project", "field-create", str(project_number),
            "--owner", owner,
            "--name", name,
            "--data-type", wanted["type"],
        ]
        if wanted["type"] == "SINGLE_SELECT":
            cmd += ["--single-select-options", ",".join(wanted["options"])]
        run(cmd, dry_run=dry_run)
