import sys
import socket


ENCODING = 'ASCII'
HEADER_SIZE = 4
MAX_CHUNK_SIZE = 16


def wrap(text: str) -> bytes:
    text_bytes = bytes(text, ENCODING)
    header_bytes = len(text).to_bytes(HEADER_SIZE, sys.byteorder, signed=False)
    return header_bytes+text_bytes


def chunkify(packet: bytes) -> list[bytes]:
    begin = 0
    chunks = []
    packet_len = len(packet)

    while begin < packet_len:
        end = min(begin+MAX_CHUNK_SIZE, packet_len)
        chunks.append(packet[begin:end])
        begin = end

    return chunks


def send_data(sock: socket.socket, text: str) -> None:
    for chunk in chunkify(wrap(text)):
        sock.sendall(chunk)


def recv_data(sock: socket.socket) -> bytes:
    data = bytearray()
    header = sock.recv(HEADER_SIZE)

    if not header:
        return data

    bytes_left = int.from_bytes(header, sys.byteorder, signed=False)

    while bytes_left > 0:
        chunk = sock.recv(MAX_CHUNK_SIZE)
        data.extend(chunk)
        bytes_left -= len(chunk)

    return data
