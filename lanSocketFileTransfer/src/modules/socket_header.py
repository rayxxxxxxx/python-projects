import pickle


class SocketHeader:
    def __init__(self) -> None:
        self.headers = dict()

    def add(self, key, value):
        self.headers[key] = value

    def as_bytes(self):
        return pickle.dumps(self.headers)

    @classmethod
    def from_bytes(cls, data: bytes):
        return pickle.loads(data)
