.PHONY: start_app
start_app:
	alembic upgrade head
	uvicorn --factory main:create_app --host 0.0.0.0 --port 8000 --reload