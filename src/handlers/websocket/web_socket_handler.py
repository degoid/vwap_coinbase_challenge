import logging
from abc import abstractmethod
from typing import Callable

from websocket import WebSocketApp


class WebSocketHandler:
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
        logging.info("Connecting to web socket...")
        ws = self.get_websocket()
        ws.run_forever()

    @staticmethod
    def _on_error(*kwargs):
        logging.error(f"WebSocket unexpected error: {kwargs[1:]}")

    @staticmethod
    def _on_close(*kwargs):
        logging.warning(f"Websocket closed [{kwargs[1:]}]")

    @abstractmethod
    def _new_message(self, ws: WebSocketApp, raw_message: str):
        raise NotImplementedError

    @abstractmethod
    def _connection_opened(self, ws: WebSocketApp):
        raise NotImplementedError
