#!/usr/bin/env python3
"""Bootstrap labels and GitHub Project fields for DAO-ops/triage."""

from __future__ import annotations

import argparse

from _common import (
    add_common_args,
    find_or_create_project,
    load_config,
    require_gh,
    resolve_owner_repo_project,
    run,
    sync_labels,
    sync_project_fields,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_args(parser)
    parser.add_argument("--skip-labels", action="store_true", help="Do not create/update labels.")
    parser.add_argument("--skip-project", action="store_true", help="Do not create/update the Project.")
    args = parser.parse_args()

    config = load_config()
    owner, repo, project_title = resolve_owner_repo_project(args, config)

    if not args.dry_run:
        require_gh()
    run(["gh", "auth", "status"], dry_run=args.dry_run, check=False)

    if not args.skip_labels:
        print("\nSyncing labels...")
        sync_labels(owner, repo, config["labels"], dry_run=args.dry_run)

    if not args.skip_project:
        print("\nCreating/finding Project...")
        project_number = find_or_create_project(owner, project_title, dry_run=args.dry_run)
        print(f"Project number: {project_number if project_number is not None else '[dry-run]'}")

        print("\nSyncing Project fields...")
        sync_project_fields(owner, project_number, config["fields"], dry_run=args.dry_run)

    print("\nDone.")
    print("Next: open the Project UI, verify Status options, create saved views, and enable built-in workflows.")


if __name__ == "__main__":
    main()
