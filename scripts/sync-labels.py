#!/usr/bin/env python3
"""Create or update repository labels from config/triage.toml."""

from __future__ import annotations

import argparse

from _common import add_common_args, load_config, require_gh, resolve_owner_repo_project, sync_labels


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_args(parser)
    args = parser.parse_args()

    config = load_config()
    owner, repo, _project_title = resolve_owner_repo_project(args, config)

    if not args.dry_run:
        require_gh()
    sync_labels(owner, repo, config["labels"], dry_run=args.dry_run)


if __name__ == "__main__":
    main()
