.PHONY: build-pythonpackage dev-requirements format help release release-push \
        release-tag release-unsafe requirements test test-format test-install \
        test-lint test-pythonpackage test-types upgrade version

.DEFAULT_GOAL := help

PACKAGE=tutoraspects
PROJECT=tutor_contrib_aspects

SOURCES=./src/$(PACKAGE)
BLACK_OPTS = --exclude templates ${SOURCES}

TUTOR_ROOT=$(PWD)/.ci
###### Development

upgrade: ## update python dependencies
	uv run --with edx-lint edx_lint write_uv_constraints pyproject.toml
	uv lock --upgrade

requirements: ## Install packages from base requirement files
	uv sync

dev-requirements: ## Install packages from developer requirement files
	uv sync --group dev

translation-requirements: ## Install packages from translation requirements
	uv sync --group translations

build-pythonpackage: ## Build Python packages ready to upload to pypi
	uv run python -m build

test: dev-requirements test-lint test-format test-pythonpackage ## Run all tests by decreasing order of priority

test-format: ## Run code formatting tests
	uv run black --check --diff $(BLACK_OPTS)
	uv run sqlfmt src/tutoraspects/templates/openedx-assets/queries --check

test-lint: ## Run code linting tests
	uv run pylint ${SOURCES}

test-install: ## Run installation test script
	tests/test-install.sh

test-pythonpackage: build-pythonpackage ## Test that package can be uploaded to pypi
	uv run twine check dist/$(PROJECT)-$(shell make version).tar.gz

format: ## Format code automatically
	uv run black $(BLACK_OPTS)
	uv run sqlfmt src/tutoraspects/templates/openedx-assets/queries

###### Deployment

release: test release-unsafe ## Create a release tag and push it to origin
release-unsafe:
	$(MAKE) release-tag release-push TAG=v$(shell make version)
release-tag:
	@echo "=== Creating tag $(TAG)"
	git tag -d $(TAG) || true
	git tag $(TAG)
release-push:
	@echo "=== Pushing tag $(TAG) to origin"
	git push origin
	git push origin :$(TAG) || true
	git push origin $(TAG)

###### Additional commands
extract_translations: translation-requirements
	uv run python src/tutoraspects/translations/translate.py . extract

version: ## Print the current tutor version
	@uv run python -c 'from importlib.metadata import version; print(version("tutor-contrib-aspects"))'

ESCAPE =
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
