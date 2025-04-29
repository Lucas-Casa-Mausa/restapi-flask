APP = restapi
VENV = .venv

# Remember to Install Flake8 at your venv

test:
	@$(VENV)/Scripts/flake8 . --exclude .venv
	@$(VENV)/Scripts/pytest -v --disable-warnings

compose:
	@docker-compose build
	@docker-compose up

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web
