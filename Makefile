APP = restapi
VENV = .venv

# Remember to Install Flake8 at your venv

test:
	@$(VENV)/Scripts/flake8 app.py

compose:
	@docker-compose build
	@docker-compose up