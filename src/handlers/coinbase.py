import json
import logging
from typing import Callable

from websocket import WebSocketApp


class CoinBaseHandler:
    def __init__(self, url: str, products: list, callback: Callable):
        self.url = url
        self.products = products
        self.callback = callback

    def get_websocket(self) -> WebSocketApp:
        return WebSocketApp(
            self.url,
            on_open=self._connection_opened,
            on_message=self._new_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

    def connect(self):
        logging.info("Connecting to Coinbase...")
        ws = self.get_websocket()
        ws.run_forever()

    def _connection_opened(self, ws: WebSocketApp):
        logging.info("Sending subscription message...")
        ws.send(self._build_subscription_message())

    def _build_subscription_message(self) -> str:
        return json.dumps({
            "type": "subscribe",
            "product_ids": self.products,
            "channels": [
                {
                    "name": "matches",
                    "product_ids": self.products
                }
            ]
        })

    def _new_message(self, ws: WebSocketApp, raw_message: str):
        message = json.loads(raw_message)

        if message['type'] == 'error':
            logging.error('Error subscribing to Coinbase. info=', message)
            return

        if message['type'] == 'subscriptions':
            logging.info('Subscription confirmed. Waiting for messages...')
            return

        if message['type'] == 'match':
            logging.debug(f"handling message {message}")
            self.callback(message)
            return

        logging.info('Message ignored: ' + str(message))

    @staticmethod
    def _on_error(*kwargs):
        logging.error(f"Error:{kwargs[1:]}")

    @staticmethod
    def _on_close(*kwargs):
        logging.warning(f"Websocket closed [{kwargs[1:]}]")
