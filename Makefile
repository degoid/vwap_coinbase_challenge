.EXPORT_ALL_VARIABLES:
CONFIG_FILE = $(PWD)/config/setup_no_mq.json

setup_env:
	@pip install -r setup/requirements.txt

run_consumer: ## Initialize a consumer service to receive messages from topic --topic
	python consumer.py --topic=$(topic)

run_producer: ## Initialize a listener service to receive messages from web socket
	python main.py

kafka_cluster:
	@docker compose up --build

stop_kafka_cluster:
	@docker compose down

test: ## Run all tests.
	@python -m pytest --cov-report term-missing --cov=src
