.PHONY: run \
	lint \
	mypy \
	env \
	test \
	coverage \
	help

env: ## Create environment
	poetry install

run: ## Run project
	poetry run python entry.py

lint: ## Run linter
	poetry run ruff format --config ./pyproject.toml . && poetry run ruff check --fix --config ./pyproject.toml .

mypy: ## Run mypy
	poetry run mypy ./

test: ## Run test <filename>
	poetry run pytest -v $(filter-out $@,$(MAKECMDGOALS)) -s

coverage: ## Make tests coverage
	poetry run pytest --cov=src tests/


# Just help
help: ## Display help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
