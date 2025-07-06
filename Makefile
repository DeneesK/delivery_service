.PHONY: start_tests
start_tests:
	docker compose -f docker-compose.test.yaml up --build --exit-code-from tests

.PHONY: start_app
start_app:
	docker compose -f docker-compose.yaml up --build