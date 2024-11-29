APP_NAME := bo

# lint
lint: black flake8

# black check
black:
	@black --check --config pyproject.toml .

# flake8 check
flake8:
	@flake8 --verbose
