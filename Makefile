setup_env:
	export CONFIG_FILE=$(PWD)/config/setup_no_mq.json
	pip install -r setup/requirements.txt

run_consumer: setup_env ## Initialize a consumer service to receive messages from topic --topic
	python consumer.py --topic=$(topic)

run_producer: setup_env
	python main.py

kafka_cluster:
	@docker compose up --build

stop_kafka_cluster:
	@docker compose down

test: ## Run all tests.
	@python -m pytest --cov-report term-missing --cov=src
