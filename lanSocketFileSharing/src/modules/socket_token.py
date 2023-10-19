import enum


class SokenToken(enum.Enum):
    DISCONNECT = b'<DISCONNECT>'
    BEGIN_OF_STREAM = b'<BOS>'
    END_OF_STREAM = b'<EOS>'
    BEGIN_OF_FILE = b'<BOF>'
    END_OF_FILE = b'<EOF>'
