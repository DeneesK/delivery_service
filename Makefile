.PHONY: start_tests
start_tests:
	docker compose -f docker-compose.test.yaml up --build --exit-code-from tests