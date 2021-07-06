"""
A thin wrapper for socket
L3P - Length prefixed packet protocol
LPP or L2P - Length prefixed packet

LPP structure:
    unsigned LEB128 encoded incoming packet length + packet content

"""
from socket import socket, AF_INET, SOCK_STREAM
from leb128 import u as unsigned_leb128
from json import dumps

class L3Psocket(socket):
    """
Socket for sending LPPs
Currently you can only use TCP, maybe UDP will added
'send' method can convert any type to bytes itself, there's no need of json-serializing dictionaries or encoding strings
    """
    read = socket.recv # leb128 decoder uses "read" method to... READ bytes
    def recv(self) -> bytes:
        """
Recieve a single packet
        """
        try:
            packet_length, _ = unsigned_leb128.decode_reader(self)
        except TypeError:
            return b""
        data = socket.recv(self, packet_length)
        return data
    def send(self, data: object) -> int:
        """
Send a packet
If the data is not bytes-like it gets valided:
    If object is or can be converted to dict, it gets json-serialized and utf-8 encoded
    Else it's string representation gets utf-8 encoded
Example validations:
    "Hello world" -> b"Hello world"
    {'hello': 'world', 'sample': 123} -> b{"hello":"world","sample":123}
        """
        def validate_data(data: object) -> bytes:
            if isinstance(data, (bytes, bytearray, memoryview)):
                return data
            if hasattr(data, "__dict__"):
                data = data.__dict__
            if isinstance(data, dict):
                return dumps(data, separators=(",", ":")).encode("utf-8")
            return str(data).encode("utf-8")

        data = validate_data(data)
        length = unsigned_leb128.encode(len(data))
        payload = length + data
        byte_count = socket.send(self, payload)
        return byte_count
