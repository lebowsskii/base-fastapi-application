down:
	docker compose -f docker-compose.yml down

reload:
	docker compose build
	docker compose up -d

.PHONY: install-isort
install-isort:
	python -c "import isort" || pip install isort

.PHONY: isort
isort: install-isort
	isort ./ --ca --skip app/pb --skip alembic --skip .venv

.PHONY: install-black
install-black:
	python -c "import black" || pip install black

.PHONY: black
black: install-black
	black ./ --exclude "app/pb|alembic|.venv"

.PHONY: install-autoflake
install-autoflake:
	python -c "import autoflake" || pip install --upgrade autoflake

.PHONY: autoflake
autoflake: install-autoflake
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive --exclude "pb,alembic,.venv" .

.PHONY: lint
lint: autoflake isort black