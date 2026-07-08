OWNER ?= dao-operations
REPO ?= triage
PROJECT_TITLE ?= DAO-ops Tracker
DRY_RUN ?=
DRY_RUN_ARG := $(if $(DRY_RUN),--dry-run,)

.PHONY: bootstrap labels project check check-strict help

help:
	@echo "Targets:"
	@echo "  make bootstrap OWNER=dao-operations REPO=triage"
	@echo "  make labels OWNER=dao-operations REPO=triage"
	@echo "  make project OWNER=dao-operations REPO=triage"
	@echo "  make check OWNER=dao-operations REPO=triage"
	@echo "  make bootstrap OWNER=dao-operations REPO=triage DRY_RUN=1"

bootstrap:
	./scripts/bootstrap.py --owner "$(OWNER)" --repo "$(REPO)" --project-title "$(PROJECT_TITLE)" $(DRY_RUN_ARG)

labels:
	./scripts/sync-labels.py --owner "$(OWNER)" --repo "$(REPO)" $(DRY_RUN_ARG)

project:
	./scripts/sync-project-fields.py --owner "$(OWNER)" --repo "$(REPO)" --project-title "$(PROJECT_TITLE)" $(DRY_RUN_ARG)

check:
	./scripts/check-taxonomy.py --owner "$(OWNER)" --repo "$(REPO)" --state open $(DRY_RUN_ARG)

check-strict:
	./scripts/check-taxonomy.py --owner "$(OWNER)" --repo "$(REPO)" --state open $(DRY_RUN_ARG) --strict
