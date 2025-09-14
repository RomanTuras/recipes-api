.PHONY: run \
	lint \
	mypy \
	env \
	test \
	coverage \
	req \
	help

env: ## Create environment
	uv sync

run: ## Run project
	uv run entry.py

lint: ## Run linter
	uv run ruff format --config ./pyproject.toml . && uv run ruff check --fix --config ./pyproject.toml .

mypy: ## Run mypy
	uv run mypy ./

test: ## Run test <filename>
	uv run pytest -v $(filter-out $@,$(MAKECMDGOALS)) -s

coverage: ## Make tests coverage
	uv run pytest --cov=src tests/

req: ## Make Requirements.txt
	uv pip compile pyproject.toml -o requirements.txt

# Just help
help: ## Display help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
