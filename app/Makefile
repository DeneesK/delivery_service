.PHONY: start_app
start_app:
	export LOG_LEVEL=$([ "$IS_DEV_MODE=true" = "true" ] && echo DEBUG || echo INFO)
	envsubst < logging.template.yaml > logging.yaml
	alembic upgrade head
	uvicorn --factory main:create_app --reload --log-config logging.yaml