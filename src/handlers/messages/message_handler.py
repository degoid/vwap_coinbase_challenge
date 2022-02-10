from abc import abstractmethod
from decimal import Decimal


class MessageHandler:

    @abstractmethod
    def send_message(self, product: str, vwap: Decimal):
        raise NotImplementedError

