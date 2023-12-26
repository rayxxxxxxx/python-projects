from modules import ENCODING
from utils.data_utils import add_header


class Message:
    def __init__(self, data: bytes = None) -> None:
        self.data: list[bytes] = list()
        if data:
            self.data.append(data)

    def addbytes(self, data: bytes) -> None:
        self.data.append(data)

    def addstr(self, data: str) -> None:
        self.data.append(data.encode(ENCODING))

    def addmeta(self, data: str) -> None:
        self.data.insert(0, data.encode(ENCODING))

    def prepare(self) -> bytes:
        return add_header(b" ".join(self.data))
