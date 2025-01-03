APP_NAME := bot

VENV_DIR := venv
PYTHON := $(VENV_DIR)/Scripts/python
PIP := $(VENV_DIR)/Scripts/pip
BLACK := $(VENV_DIR)/Scripts/black
FLAKE8 := $(VENV_DIR)/Scripts/flake8
ALEMBIC := $(VENV_DIR)/Scripts/alembic
PYBABEL := $(VENV_DIR)/Scripts/pybabel

DOCKER_BUILD_NAME := cover_dance_bot

LOCALES_DIR := locales
LOCALES_DOMAIN := messages

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@test -d $(VENV_DIR) || python -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"

# Install dependencies into venv
install: venv
	@echo "Installing dependencies..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PIP) install -r requirements/dev.txt

# lint
lint: black flake8

# black check
black:
	@$(BLACK) --check --config pyproject.toml .

# flake8 check
flake8:
	@$(FLAKE8) --verbose

# Clean cache
clean:
	@echo "Clearing cache..."
	@$(PYTHON) -c "import os, shutil; [shutil.rmtree(os.path.join(root, d), ignore_errors=True) for root, dirs, _ in os.walk('.') for d in dirs if d in {'__pycache__', '.pytest_cache', '.mypy_cache'}]"


# Apply migrations
migrate: venv docker-database
	@echo "Applying migrations..."
	@cd $(APP_NAME) && ../$(ALEMBIC) upgrade head

# Run the application
run: venv docker-database
	@$(PYTHON) $(APP_NAME)

# Build Docker image
docker-build: clean
	@docker build -t $(DOCKER_BUILD_NAME):latest .

# Run containers with docker-compose
docker-up:
	@echo "Starting containers..."
	@docker-compose up --build

# Start database
docker-database:
	@echo "Starting database..."
	@docker-compose up -d redis postgres

# Stop containers
docker-down:
	@echo "Stopping containers..."
	@docker-compose down

# Restart containers
docker-restart: docker-down docker-up

# Pybabel texts update
texts-update:
	@${PYBABEL} extract . \
		-o ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot \
		--ignore-dirs=venv
	@${PYBABEL} update \
		-i ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot \
		-d ${LOCALES_DIR} \
		-D ${LOCALES_DOMAIN}

# Pybabel texts compile
texts-compile:
	@${PYBABEL} compile \
		-d ${LOCALES_DIR} \
		-D ${LOCALES_DOMAIN}

# Pybabel create new language
texts-create-language:
	@${PYBABEL} init \
		-i ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot \
		-d ${LOCALES_DIR} \
		-D ${LOCALES_DOMAIN} \
		-l ${language}
