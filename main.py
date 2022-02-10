import logging
import os
from typing import Optional

from src.handlers.websocket.coinbase import CoinBaseHandler
from src.handlers.configuration import ConfigurationHandler
from src.handlers.messages.kafka import KafkaHandler
from src.products.calculator import VWAPCalculator
from src.products.product import Product
from src.utils.config_utils import get_configuration


class ProducerClient:
    """
    Client to process the connection with the socket, listen each message and calculate the VWAP for each pair and,
    if there is one cluster running, send the message to the Kafka Cluster.
    """
    def __init__(self):
        self.socket_handler: Optional[CoinBaseHandler] = None
        self.vwap_calculator: Optional[VWAPCalculator] = None
        self.kafka_handler: Optional[KafkaHandler] = None

    def initialize(self, configuration: ConfigurationHandler):
        self.socket_handler = configuration.initialize_websocket(self.callback)
        self.vwap_calculator = configuration.initialize_vwap()
        self.kafka_handler = configuration.setup_brokers()

    def callback(self, message: dict):
        logging.debug("creating product")
        product = Product(message)

        logging.debug("computing vwap")
        new_vwap = self.vwap_calculator.calculate_vwap(product)

        if self.kafka_handler is not None:
            logging.debug("sending kafka message")
            self.kafka_handler.send_message(product.id, new_vwap)

        logging.info(f"[{product.id}] {new_vwap}")

    def start(self):
        logging.info("Initialize the connection")
        self.socket_handler.connect()


def main():
    config_file = os.environ.get('CONFIG_FILE')
    is_local = bool(os.environ.get('LOCAL_RUN', False))

    config = get_configuration(config_file, is_local)
    if config:
        client = ProducerClient()
        client.initialize(config)
        client.start()


if __name__ == "__main__":
    main()
