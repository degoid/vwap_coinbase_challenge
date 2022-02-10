from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from kafka.errors import KafkaError

import src.handlers.messages.kafka

from src.handlers.messages.kafka import KafkaHandler


def test_initialize_producers_with_empty_json():
    handler = KafkaHandler({})
    assert len(handler.brokers) == 0


def test_initialize_producers_with_one_broker():
    KafkaProducerMock = MagicMock()
    src.handlers.messages.kafka.KafkaProducer = KafkaProducerMock
    KafkaProducerMock.bootstrap_connected = MagicMock(return_value=True)

    handler = src.handlers.messages.kafka.KafkaHandler({"address": ["p1", "p2"]})
    assert len(handler.brokers) == 1

    broker = handler._get_producer_by_product("p1")
    assert broker is not None

    broker = handler._get_producer_by_product("p3")
    assert broker is None


def test_send_messages():
    KafkaProducerMock = MagicMock()
    src.handlers.messages.kafka.KafkaProducer = KafkaProducerMock
    KafkaProducerMock.bootstrap_connected = MagicMock(return_value=True)

    handler = src.handlers.messages.kafka.KafkaHandler({"address": ["p1", "p2"]})
    broker = handler._get_producer_by_product("p1")
    handler.send_message("p1", Decimal(10.9))

    assert broker.send.call_count == 1


def test_initialization_retries():

    kafka_producer_mock = MagicMock()
    kafka_producer_mock.bootstrap_connected = MagicMock(return_value=False)
    KafkaHandler._create_kafka_producer = MagicMock(return_value=kafka_producer_mock)

    with pytest.raises(KafkaError):
        KafkaHandler({"address": ["p1", "p2"]})


def test_send_message_wo_producer():

    kafka_producer_mock = MagicMock()
    kafka_producer_mock.bootstrap_connected = MagicMock(return_value=True)
    KafkaHandler._create_kafka_producer = MagicMock(return_value=kafka_producer_mock)

    handler = KafkaHandler({"address": ["p1", "p2"]})

    with pytest.raises(KafkaError):
        handler.send_message("p3", Decimal(1))

