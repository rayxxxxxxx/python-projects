from src import ENCODING, HEADER_SIZE


def add_header(data: bytes) -> bytes:
    dsize = len(data)
    ndigits = len(str(dsize))
    header = str(dsize)+' '*(HEADER_SIZE-ndigits)
    return header.encode(ENCODING)+data


def remove_header(data: bytes) -> bytes:
    ...


def chunkify(data: bytes) -> list[bytes]:
    ...
