import logging
import os

from src.clients.producer import ProducerClient
from src.handlers.configuration import ConfigurationHandler


def get_configuration() -> ConfigurationHandler:
    config_file = os.environ.get('CONFIG_FILE')
    if config_file:
        config = ConfigurationHandler(config_file)
        config.setup()
        
        return config

    logging.error("CONFIG_FILE environment variable is not defined.")


def start_producer(config: ConfigurationHandler):
    client = ProducerClient()
    client.initialize(config)
    client.produce()


def main():
    config = get_configuration()
    if config:
        start_producer(config)


if __name__ == "__main__":
    main()
