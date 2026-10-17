.PHONY: dev test e2e verify

PORT ?= 8765

dev:
	PANTRY_DB=pantry.db python3 -m uvicorn app.server:app --host 127.0.0.1 --port $(PORT)

test:
	python3 -m pytest -q tests

e2e:
	bash scripts/e2e.sh

verify: test e2e
