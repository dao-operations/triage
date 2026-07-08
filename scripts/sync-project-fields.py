#!/usr/bin/env python3
"""Create the GitHub Project if needed and create missing Project fields."""

from __future__ import annotations

import argparse

from _common import (
    add_common_args,
    find_or_create_project,
    load_config,
    require_gh,
    resolve_owner_repo_project,
    sync_project_fields,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_args(parser)
    args = parser.parse_args()

    config = load_config()
    owner, _repo, project_title = resolve_owner_repo_project(args, config)

    if not args.dry_run:
        require_gh()
    project_number = find_or_create_project(owner, project_title, dry_run=args.dry_run)
    sync_project_fields(owner, project_number, config["fields"], dry_run=args.dry_run)


if __name__ == "__main__":
    main()
