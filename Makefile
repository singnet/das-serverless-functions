isort:
	@isort --settings-path .isort.cfg ./hyperon_das ./tests

black:
	@black --config .black.cfg ./hyperon_das ./tests

flake8:
	@flake8 --config .flake8.cfg ./hyperon_das ./tests --exclude ./hyperon_das/grpc/

lint: isort black flake8

unit-tests:
	./scripts/run-tests.sh unit

unit-tests-coverage:
	./scripts/run-tests.sh unit-coverage

integration-tests:
	./scripts/run-tests.sh integration

build:
	docker compose build --no-cache

pre-commit: lint unit-tests-coverage unit-tests integration-tests

serve:
	@docker compose up --build --force-recreate

stop:
	@docker compose down
