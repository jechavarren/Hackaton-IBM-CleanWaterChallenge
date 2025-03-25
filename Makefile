run:
	docker compose --env-file .env up --build

clean:
	black --line-length 79 ./

	sudo find . -type d -name __pycache__ -exec sudo rm -r {} \;
	sudo find . -type d -name .pytest_cache -exec sudo rm -r {} \;
	sudo find . -type d -name .venv -exec sudo rm -r {} \;
