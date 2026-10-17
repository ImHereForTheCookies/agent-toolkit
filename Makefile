.PHONY: verify smoke

verify:
	bash scripts/verify.sh

smoke:
	bash scripts/smoke_install.sh
