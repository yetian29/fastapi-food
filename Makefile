

.PHONY:

makemigrations:
	alembic revision --autogenerate -m="$(m)"

migrate:
	alembic upgrade head