import argparse

from src.client import Client


class ChatCLI:
    def __init__(self) -> None:
        self.chat_client = Client()

    def mainloop(self):
        ...


if __name__ == '__main__':
    cli = ChatCLI()
