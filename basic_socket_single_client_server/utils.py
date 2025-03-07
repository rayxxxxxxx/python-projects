ENCODING = 'ASCII'
HEADER_SIZE = 2
MAX_CHUNK_SIZE = 16


def make_packet(text):
    text_bytes = bytes(text, ENCODING)
    header_bytes = len(text).to_bytes(HEADER_SIZE, 'big')
    return header_bytes+text_bytes


def chunkify(packet):
    chunks = []
    begin = 0

    while begin < len(packet):
        end = min(begin+MAX_CHUNK_SIZE, len(packet))
        chunks.append(packet[begin:end])
        begin = end

    return chunks


def send_data(sock, text):
    for chunk in chunkify(make_packet(text)):
        sock.sendall(chunk)


def recv_data(sock):
    data = bytearray()
    header = sock.recv(HEADER_SIZE)

    if header == b'':
        return data

    size = int.from_bytes(header, 'big')

    while size > 0:
        chunk = sock.recv(MAX_CHUNK_SIZE)
        data.extend(chunk)
        size -= len(chunk)

    return data
