.PHONY: bootstrap test demo validate clean help

PYTHON ?= ./venv/bin/python3
PIP ?= ./venv/bin/pip

bootstrap:
	python3 -m venv venv
	$(PIP) install -r requirements.txt pytest

test:
	$(PYTHON) -m pytest tests/

demo-ecommerce:
	$(PYTHON) -m dw_agent demo --scenario ecommerce

demo-bfs:
	$(PYTHON) -m dw_agent demo --scenario bfs-credit-risk

clean:
	rm -rf output/ .pytest_cache/ __pycache__/ src/*/__pycache__/ src/*/*/__pycache__

help:
	@echo "Available commands:"
	@echo "  make bootstrap      Initialize virtual environment and install dependencies"
	@echo "  make test           Run unit and integration test suite"
	@echo "  make demo-ecommerce Run the e-commerce scenario demo"
	@echo "  make demo-bfs       Run the BFS credit risk scenario demo"
	@echo "  make clean          Clean generated outputs and cache"
