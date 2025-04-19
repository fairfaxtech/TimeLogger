.PHONY: install dev clean test

install:
	pip install -e .

dev:
	pip install -e .[dev]

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

test:
	python timelogger.py --help

run-example:
	@echo "Running example commands..."
	python timelogger.py start "Testing the app" --category testing
	sleep 2
	python timelogger.py status
	python timelogger.py stop
	python timelogger.py list