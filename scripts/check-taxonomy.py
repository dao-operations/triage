#!/usr/bin/env python3
"""Check open issues for taxonomy drift.

Default mode fails on clear taxonomy errors and warns about missing scope.
Use --strict to fail on missing warn_open namespaces too.
"""

from __future__ import annotations

import argparse
import sys

from _common import add_common_args, full_repo, gh_json, load_config, require_gh, resolve_owner_repo_project


def labels_for(issue: dict) -> list[str]:
    return [label["name"] for label in issue.get("labels", []) if "name" in label]


def count_prefix(labels: list[str], prefix: str) -> list[str]:
    return [name for name in labels if name.startswith(prefix)]


def config_errors(config: dict) -> list[str]:
    errors: list[str] = []
    labels = config.get("labels", [])
    label_names = {label.get("name") for label in labels}

    for label in labels:
        description = str(label.get("description", "")).strip()
        if not description:
            errors.append(f"config label {label.get('name')!r} must have a GitHub label description")
        if description.lower().startswith("meaning:"):
            errors.append(f"config label {label.get('name')!r} description should not include the old 'Meaning:' prefix")

    if "scope:dao" not in label_names:
        errors.append("config must define scope:dao")
    legacy_dao_scope = "scope:dao" + "-app"
    if legacy_dao_scope in label_names:
        errors.append("config must not define the legacy DAO-app scope label")

    for field in config.get("fields", []):
        if field.get("name") == "Scope":
            options = [str(option) for option in field.get("options", [])]
            non_lower = [option for option in options if option != option.lower()]
            if non_lower:
                errors.append(f"Scope field options must be lower-case: {', '.join(non_lower)}")
            multi_scope_terms = {"cross" + "-scope", "multiple / cross" + "-scope"}
            if any(option.lower() in multi_scope_terms for option in options):
                errors.append("Scope field must not include a multi-scope option; use multiple scope labels instead")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_args(parser)
    parser.add_argument("--state", choices=["open", "closed", "all"], default="open")
    parser.add_argument("--strict", action="store_true", help="Treat warn_open namespace misses as errors.")
    args = parser.parse_args()

    config = load_config()
    owner, repo, _project_title = resolve_owner_repo_project(args, config)
    taxonomy = config["taxonomy"]

    if not args.dry_run:
        require_gh()

    allowed = {label["name"] for label in config["labels"]}
    namespaces = tuple(taxonomy["namespaces"])
    single = tuple(taxonomy["single"])
    required_open = tuple(taxonomy.get("required_open", []))
    warn_open = tuple(taxonomy.get("warn_open", []))
    forbidden_prefixes = tuple(taxonomy.get("forbidden_prefixes", []))
    forbidden_labels = set(taxonomy.get("forbidden_labels", []))

    errors = config_errors(config)

    issues = gh_json([
        "gh", "issue", "list",
        "--repo", full_repo(owner, repo),
        "--state", args.state,
        "--limit", "1000",
        "--json", "number,title,labels,state",
    ], dry_run=args.dry_run) or []

    warnings: list[str] = []

    for issue in issues:
        prefix = f"#{issue['number']} {issue['title']}"
        names = labels_for(issue)
        taxonomy_labels = [name for name in names if name.startswith(namespaces)]

        unknown = [name for name in taxonomy_labels if name not in allowed]
        if unknown:
            errors.append(f"{prefix}: unknown taxonomy label(s): {', '.join(unknown)}")

        forbidden = [name for name in names if name in forbidden_labels or name.startswith(forbidden_prefixes)]
        if forbidden:
            errors.append(f"{prefix}: forbidden legacy label(s): {', '.join(forbidden)}")

        for ns in single:
            matches = count_prefix(names, ns)
            if len(matches) > 1:
                errors.append(f"{prefix}: multiple {ns} labels: {', '.join(matches)}")

        if issue.get("state") == "OPEN":
            for ns in required_open:
                if not count_prefix(names, ns):
                    errors.append(f"{prefix}: missing required {ns} label")
            for ns in warn_open:
                if not count_prefix(names, ns):
                    msg = f"{prefix}: missing recommended {ns} label"
                    if args.strict:
                        errors.append(msg)
                    else:
                        warnings.append(msg)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"Found {len(errors)} error(s) and {len(warnings)} warning(s).", file=sys.stderr)
        sys.exit(1)

    if warnings:
        print(f"No taxonomy errors. Found {len(warnings)} warning(s).")
    else:
        print("No taxonomy problems found.")


if __name__ == "__main__":
    main()
