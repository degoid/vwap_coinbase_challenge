from src.handlers.websocket.coinbase import CoinBaseHandler
from unittest.mock import MagicMock

URL = 'localhost'
PORT = 8765
PRODUCT = "ETH-USD"


def test_on_connect():
	ws = MagicMock()

	coinbase = CoinBaseHandler(f"wss://{URL}:{PORT}", ["ETH-USD"], None)
	coinbase.get_websocket = MagicMock(return_value=ws)
	coinbase.connect()

	assert ws.run_forever.call_count == 1


def test_subscription_message():
	ws = MagicMock()

	coinbase = CoinBaseHandler(f"wss://{URL}:{PORT}", ["ETH-USD"], None)
	coinbase._connection_opened(ws)

	assert ws.send.call_count == 1
	assert PRODUCT in ws.send.call_args._get_call_arguments()[0][0]


def test_message_sent():
	ws = MagicMock()
	callback = MagicMock()

	coinbase = CoinBaseHandler(f"wss://{URL}:{PORT}", ["ETH-USD"], callback)

	coinbase._new_message(ws, '{"type": "error"}')
	assert callback.call_count == 0

	coinbase._new_message(ws, '{"type": "subscriptions"}')
	assert callback.call_count == 0

	coinbase._new_message(ws, '{"type": "match"}')
	assert callback.call_count == 1
	assert {'type': 'match'} == callback.call_args._get_call_arguments()[0][0]





