STORAGE=docker-compose/storage.yaml

.PHONY:
up_storage:
	docker-compose --env-file .env -f ${STORAGE} up -d 

down_storage:
	docker-compose --env-file .env -f ${STORAGE} down

makemigrations:
	alembic revision --autogenerate -m="$(m)"

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1