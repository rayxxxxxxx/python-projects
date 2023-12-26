from modules.message import Message


class SocketData:
    def __init__(self) -> None:
        self.messages: list[Message] = list()
