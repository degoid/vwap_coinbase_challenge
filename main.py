import os

from src.clients.producer import ProducerClient
from src.handlers.configuration import ConfigurationHandler


def get_configuration() -> ConfigurationHandler:
    config_file = os.environ['CONFIG_FILE']
    config = ConfigurationHandler(config_file)
    config.setup()

    return config


def start_producer(config: ConfigurationHandler):
    client = ProducerClient()
    client.initialize(config)
    client.produce()


def main():
    config = get_configuration()
    start_producer(config)


if __name__ == "__main__":
    main()
