# Variables
ENV_NAME = bsk-scraper  # Replace with your environment name

# Default target
.PHONY: all
all: install

# Install dependencies with Poetry in Micromamba environment
.PHONY: install
install:
	micromamba run -n $(ENV_NAME) poetry install

# Run tests
# .PHONY: test
# test:
# 	micromamba run -n $(ENV_NAME) poetry run pytest

# Run application
.PHONY: run
run:
	micromamba run -n $(ENV_NAME) poetry run python bsk_scraper/main.py

# Help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make          - Install dependencies with Poetry in Conda environment"
#	@echo "  make test     - Run tests"
	@echo "  make run      - Run the application"
