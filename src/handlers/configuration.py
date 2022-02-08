import json
import logging
from time import sleep
from typing import Optional, Callable

from src.handlers.coinbase import CoinBaseHandler
from src.handlers.kafka import ProducerHandler
from src.products.calculator import VWAPCalculator


class Configuration:
    def __init__(self, config: dict):
        self.max_size = config.get("max_size")
        self.brokers = config.get("brokers", None)
        self.coinbase_url = config.get("coinbase_url")
        self.log_level = config.get("log_level")
        self.products = config.get("products")
        self.kafka_time = config.get("kafka_time", None)


class ConfigurationHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.configuration = None

    def _open_config(self) -> dict:
        f = open(self.file_path)
        return json.load(f)

    def setup(self):
        raw_config = self._open_config()
        self.configuration = Configuration(raw_config)

        self._setup_logger()

    def setup_brokers(self) -> Optional[ProducerHandler]:
        brokers_json = self.configuration.brokers
        if brokers_json is not None:
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

    def initialize_websocket(self, callback: Callable) -> CoinBaseHandler:
        url = self.configuration.coinbase_url
        products = self.configuration.products

        if url == '' or products is None:
            logging.error(f"Coinbase url must not be empty and at least one product must be provided.")
            exit(1)

        return CoinBaseHandler(url, products, callback)
