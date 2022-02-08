import logging
from decimal import Decimal
from time import sleep
from typing import List, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

MAX_RETRIES = 3
TIME_TO_WAIT = 5
CLIENT_ID = 'vwap'


class BrokerMap:
    def __init__(self, address: str, products: List[str], producer: KafkaProducer):
        self.address = address
        self.products = products
        self.producer = producer


class ProducerHandler:
    def __init__(self, brokers_json: dict):
        self.brokers = []
        self._initialize_producers(brokers_json)

    def _initialize_producers(self, brokers_json: dict):
        for address in brokers_json:
            broker_map = BrokerMap(address, brokers_json[address], self._create_producer(address))
            self.brokers.append(broker_map)

    @staticmethod
    def _create_kafka_producer(address: str):
        return KafkaProducer(bootstrap_servers=address, client_id=CLIENT_ID)

    def _create_producer(self, address):
        connected = False
        retries = 0
        producer = None

        while not connected and retries < MAX_RETRIES:
            producer = self._create_kafka_producer(address)

            connected = (producer is not None) and producer.bootstrap_connected()

            if not connected:
                retries = retries + 1
                logging.warning(f"Producer is not ready, waiting {TIME_TO_WAIT}s")
                sleep(TIME_TO_WAIT)

        if retries == MAX_RETRIES:
            raise KafkaError(f"Error creating producer with address: {address}")

        return producer

    def _get_producer_by_product(self, product_id: str) -> Optional[KafkaProducer]:
        for broker in self.brokers:
            if str(product_id) in broker.products:
                return broker.producer

        return None

    def send_message(self, product_id, vwap: Decimal):
        producer = self._get_producer_by_product(product_id)

        if producer is not None:
            logging.debug(f"Sending a new message - topic {product_id}: message {vwap}")
            producer.send(f"{product_id}", f"{vwap}".encode('utf-8'))
            return

        raise KafkaError(f"Kafka producer is not defined for product {product_id}")

