from unittest.mock import patch, MagicMock

import pytest

from src.handlers.configuration import ConfigurationHandler
import os


@patch("src.handlers.configuration.ProducerHandler")
def test_setup_initializations(producer_handler):
    producer_handler._create_kafka_producer = MagicMock()
    config = ConfigurationHandler(os.getcwd() + "/config/test_setup.json")

    config_dict = config._open_config()

    assert config_dict['ws_url'] == 'wss://url'
    assert config_dict['kafka_time'] == 1

    config.setup()
    # no exception was raised
    ph = config.setup_brokers()

    constructor_args = producer_handler.call_args._get_call_arguments()[0][0]

    assert producer_handler.call_count == 1
    assert constructor_args['b1'] == ['p1', 'p2']
    assert constructor_args['b2'] == ['p3']

    assert ph is not None

    vwap = config.initialize_vwap()
    assert vwap.max_size == 20

    ws = config.initialize_websocket(MagicMock())
    assert ws.url == 'wss://url'


def test_bad_configuration():
    with pytest.raises(FileNotFoundError):
        config = ConfigurationHandler(os.getcwd() + "/config/test_setup_other.json")
        config.setup()

    config = ConfigurationHandler(os.getcwd() + "/config/bad_setup.json")
    with pytest.raises(ValueError):
        config.setup()

    with pytest.raises(ValueError):
        config.initialize_websocket(MagicMock())

    ph = config.setup_brokers()
    assert ph is None




