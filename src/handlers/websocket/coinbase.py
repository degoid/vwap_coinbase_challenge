import json
import logging

from websocket import WebSocketApp

from src.handlers.websocket.web_socket_handler import WebSocketHandler


class CoinBaseHandler(WebSocketHandler):
    """
    Responsible for all the Coinbase WebSccket associated logic
    """

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
