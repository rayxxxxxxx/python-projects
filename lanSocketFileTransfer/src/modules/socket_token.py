import enum


class SocketToken(enum.Enum):
    DISCONNECT = b"\r\0"
