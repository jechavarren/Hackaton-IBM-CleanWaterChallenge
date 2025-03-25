run_api:
	python main.py

run_etl:
	python -m src.etl.main

test:
	python -m pytest test/


clean:
	black --line-length 79 ./
	find . -type d -name __pycache__ -exec sudo rm -r {} \;
