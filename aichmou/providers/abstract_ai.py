from abc import ABC, abstractmethod


class AbstractAI(ABC):
    def __init__(self, api_key: str, server_url: str, model=None):
        self.api_key = api_key
        self.server_url = server_url
        self.model = model

    @abstractmethod
    def complete(self, prompt: str, text: str) -> str:
        pass
