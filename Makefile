.PHONY: build-pythonpackage format help requirements test test-format test-install \
        test-lint test-pythonpackage upgrade

.DEFAULT_GOAL := help

PACKAGE=tutoraspects
PROJECT=tutor_contrib_aspects

SOURCES=./src/$(PACKAGE)
BLACK_OPTS = --exclude templates ${SOURCES}

TUTOR_ROOT=$(PWD)/.ci
###### Development

upgrade: ## Upgrade and regenerate pinned dependencies
	uv run --with edx-lint edx_lint write_uv_constraints pyproject.toml
	uv lock --upgrade

requirements: ## Install dev dependencies
	uv sync --group dev
	uv tool install tox --with tox-uv

translation-requirements: ## Install packages for translations
	uv sync --group dev

build-pythonpackage: ## Build Python packages ready to upload to pypi
	uv run python -m build

test: test-lint test-format test-pythonpackage ## Run all tests by decreasing order of priority

test-format: ## Run code formatting tests
	uv run black --check --diff $(BLACK_OPTS)
	uv run sqlfmt src/tutoraspects/templates/openedx-assets/queries --check

test-lint: ## Run code linting tests
	uv run tox -e lint

test-install: ## Run installation test script
	tests/test-install.sh

test-pythonpackage: build-pythonpackage ## Test that package can be uploaded to pypi
	uv run twine check dist/$(PROJECT)-*.tar.gz

format: ## Format code automatically
	uv run black $(BLACK_OPTS)
	uv run sqlfmt src/tutoraspects/templates/openedx-assets/queries

###### Additional commands
extract_translations: translation-requirements
	uv run python src/tutoraspects/translations/translate.py . extract

ESCAPE =
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
