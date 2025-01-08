ENV_NAME = bsk-scraper

.PHONY: all
all: install

.PHONY: install
install:
	poetry install

# Run tests
# .PHONY: test
# test:
# 	micromamba run -n $(ENV_NAME) poetry run pytest

.PHONY: run
run:
	poetry run python bsk_scraper/main.py

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make          - Install dependencies with Poetry in Conda environment"
#	@echo "  make test     - Run tests"
	@echo "  make run      - Run the application"
