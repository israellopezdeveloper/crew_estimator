.PHONY: lint format typecheck qa

lint:
	@echo ""
	@echo "LINT"
	@echo "===="
	@poetry run ruff check .

format:
	@echo ""
	@echo "FORMAT"
	@echo "======"
	@poetry run black .

typecheck:
	@echo ""
	@echo "TYPECHECK"
	@echo "========="
	@poetry run mypy .

qa: lint format typecheck

check:
	@echo ""
	@echo "RUN TESTS"
	@echo "========="
	@poetry run pytest

check-stats-dev:
	@echo "RUN TESTS (Development environment)"
	@echo "==================================="
	@HYPOTESIS_PROFILE=dev poetry run pytest \
		tests/test_estimator_hypothesis.py \
		--hypothesis-show-statistics -v

check-stats-ci:
	@echo "RUN TESTS (CI environment)"
	@echo "=========================="
	@HYPOTESIS_PROFILE=ci poetry run pytest \
		tests/test_estimator_hypothesis.py \
		--hypothesis-show-statistics -v
