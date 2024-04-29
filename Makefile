isort:
	@isort ./das-query-engine ./das-query-engine/tests --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100

black:
	@black ./das-query-engine ./das-query-engine/tests --line-length 100 -t py37 --skip-string-normalization

flake8:
	@flake8 ./das-query-engine ./das-query-engine/tests --show-source --extend-ignore E501

lint: isort black flake8

unit-tests:
	./scripts/run-tests.sh unit

unit-tests-coverage:
	./scripts/run-tests.sh unit-coverage

integration-tests:
	./scripts/run-tests.sh integration

build: 
	docker compose build --no-cache

pre-commit: unit-tests-coverage lint

serve:
	@docker compose up --build --force-recreate

stop:
	@docker compose down
