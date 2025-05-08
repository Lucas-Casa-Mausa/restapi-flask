APP = restapi


# Remember to Install Flake8 at your venv

test:
	@bandit -r --exclude "./.venv,./tests" .
	@black .
	@flake8 . --exclude .venv
	@pytest -v --disable-warnings

compose:
	@docker-compose build
	@docker-compose up

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web
