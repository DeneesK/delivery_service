.PHONY: start_tests
start_tests:
	docker-compose -f docker-compose.test.yaml up --build --exit-code-from tests -d

.PHONY: start_app
start_app:
	docker-compose -f docker-compose.yaml up --build

.PHONY: stop_app
stop_app:
	docker-compose -f docker-compose.yaml down

.PHONY: app_logs
stop_app:
	docker-compose -f docker-compose.yaml logs
