.PHONY: dev test e2e verify symbols

# Contract: every project answers these targets. Replace the TODO recipes.

dev:
	@echo "TODO: define dev for this project"

test:
	@echo "TODO: define test for this project"

e2e:
	@echo "TODO: define e2e for this project"

verify: test e2e

# Repo map (symbol index) for low-token code navigation. Needs the
# code-navigation plugin's script: set TOOLKIT=<agent-toolkit checkout> or
# REPO_MAP=<path to repo_map.py>. Skips (exit 0) when neither points at a file,
# so `make verify` stays green without the toolkit.
TOOLKIT ?=
REPO_MAP ?= $(if $(TOOLKIT),$(TOOLKIT)/plugins/code-navigation/scripts/repo_map.py)

symbols:
	@if [ -n "$(REPO_MAP)" ] && [ -f "$(REPO_MAP)" ]; then \
		python3 "$(REPO_MAP)" . --out docs/symbols.md && echo "wrote docs/symbols.md"; \
	else \
		echo "skip symbols: repo_map.py not found (set TOOLKIT=<agent-toolkit checkout> or REPO_MAP=<path>)"; \
	fi
