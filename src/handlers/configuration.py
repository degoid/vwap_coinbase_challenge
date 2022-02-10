import json
import logging
from time import sleep
from typing import Optional, Callable

from src.handlers.websocket.coinbase import CoinBaseHandler
from src.handlers.kafka import ProducerHandler
from src.handlers.websocket.web_socket_handler import WebSocketHandler
from src.products.calculator import VWAPCalculator


class Configuration:
    def __init__(self, config: dict):
        self.max_size = config.get("max_size")
        self.brokers = config.get("brokers", None)
        self.ws_url = config.get("ws_url")
        self.log_level = config.get("log_level")
        self.products = config.get("products")
        self.kafka_time = config.get("kafka_time", None)


class ConfigurationHandler:
    """
    Helper class to handle with all initializations
    """
    def __init__(self, file_path: str, is_local: bool = False):
        self.file_path = file_path
        self.configuration = None
        self.is_local = is_local

    def _open_config(self) -> dict:
        f = open(self.file_path)
        return json.load(f)

    def setup(self):
        raw_config = self._open_config()
        self.configuration = Configuration(raw_config)

        self._setup_logger()

    def setup_brokers(self) -> Optional[ProducerHandler]:
        brokers_json = self.configuration.brokers
        if brokers_json is not None and len(brokers_json.keys()) > 0:
            if self.is_local:
                sleep(self.configuration.kafka_time)

            return ProducerHandler(brokers_json)

        return None

    def _setup_logger(self):
        log_level = self.configuration.log_level
        numeric_level = getattr(logging, log_level.upper(), None)

        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')

        logging.basicConfig(level=numeric_level)

    def initialize_vwap(self) -> VWAPCalculator:
        max_size = int(self.configuration.max_size)
        return VWAPCalculator(max_size)

    def initialize_websocket(self, callback: Callable) -> WebSocketHandler:
        url = self.configuration.ws_url
        products = self.configuration.products

        if url == '' or products is None:
            raise ValueError("WS URL cannot be empty and at least one product must be provided.")

        return CoinBaseHandler(url, products, callback)
