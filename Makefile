isort:
	@isort --settings-path .isort.cfg ./das-query-engine/tests

black:
	@black --config .black.cfg ./das-query-engine/tests

flake8:
	@flake8 --config .flake8.cfg ./das-query-engine/tests/

lint: isort black flake8

unit-tests:
	./scripts/run-tests.sh unit

unit-tests-coverage:
	./scripts/run-tests.sh unit-coverage

integration-tests: build
	./scripts/run-tests.sh integration

build:
	docker compose build --no-cache

pre-commit: lint unit-tests-coverage unit-tests integration-tests

serve:
	@docker compose up --build --force-recreate

stop:
	@docker compose down
