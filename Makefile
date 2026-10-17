.PHONY: verify smoke eval-hitl

verify:
	bash scripts/verify.sh

smoke:
	bash scripts/smoke_install.sh

eval-hitl:
	python3 evals/hitl/run_eval.py
