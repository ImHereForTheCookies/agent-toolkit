.PHONY: setup doctor verify smoke eval-hitl

setup:
	python3 -m pip install -r requirements-dev.txt

doctor:
	python3 plugins/ticket-loop/scripts/check_requirements.py

verify:
	bash scripts/verify.sh

smoke:
	bash scripts/smoke_install.sh

eval-hitl:
	python3 evals/hitl/run_eval.py
