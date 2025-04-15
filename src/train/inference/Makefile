ENV ?= local
PROCESS_VERSION ?= v0.0.1
PROCESS_ID = python-example

# ROOT_DIR := YOUR ROOT DIR HERE
PRODUCT_NAME := $(shell basename $(wildcard $(ROOT_DIR).kai/$(ENV)/*.yaml) .yaml)

UV ?= uv
KLI ?= kli

# targets
.PHONY: push-image lint clean

push-image:
	$(KLI) process-registry register task $(PROCESS_ID) \
		--dockerfile "Dockerfile" \
		--product $(PRODUCT_NAME) \
		--src "." \
		--version $(PROCESS_VERSION)

lint:
	$(UV) run ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

.PHONY: outdated-libraries
outdated-libraries: ## Check outdated libraries
	uv pip list --outdated
