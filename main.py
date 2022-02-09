import logging
import os
from typing import Optional

from src.handlers.coinbase import CoinBaseHandler
from src.handlers.configuration import ConfigurationHandler
from src.handlers.kafka import ProducerHandler
from src.products.calculator import VWAPCalculator
from src.products.product import Product
from src.utils.config_utils import get_configuration


class ProducerClient:
    def __init__(self):
        self.socket_handler: Optional[CoinBaseHandler] = None
        self.vwap_calculator: Optional[VWAPCalculator] = None
        self.kafka_handler: Optional[ProducerHandler] = None

    def initialize(self, configuration: ConfigurationHandler):
        self.socket_handler = configuration.initialize_websocket(self.callback)
        self.vwap_calculator = configuration.initialize_vwap()
        self.kafka_handler = configuration.setup_brokers()

    def callback(self, message: dict):
        logging.debug("creating product")
        product = Product(message)
        logging.debug("computing vwap")
        new_vwap = self.vwap_calculator.calculate_vwap(product)

        logging.debug("checking kafka")
        if self.kafka_handler is not None:
            logging.debug("sending kafka message")
            self.kafka_handler.send_message(product.id, new_vwap)

        logging.info(f"[{product.id}] {new_vwap}")

    def produce(self):
        self.socket_handler.connect()


def main():
    config_file = os.environ.get('CONFIG_FILE')
    is_local = bool(os.environ.get('LOCAL_RUN', False))

    config = get_configuration(config_file, is_local)
    if config:
        client = ProducerClient()
        client.initialize(config)
        client.produce()


if __name__ == "__main__":
    main()
