"""
Socket wrapper
"""
# TODO add logging
import socket
from json import loads, dumps
from datetime import datetime
from threading import Thread
from asautils.extypes import List


class ClientError(Exception):
    """Errors caused serverside by client's mistake (Too less data etc.)"""
    pass

class UnknownPacket(ClientError):
    def __init__(self, packet_id):
        super().__init__("Packed with id %d is not supported by the server" % packet_id)

class TooLessData(ClientError):
    def __init__(self, required):
        super().__init__("Your request is missing %d argument(s): %s" % (len(required), List(required)))

class InvalidData(ClientError, ValueError):
    def __init__(self, argument):
        super().__init__("Data in '%s' is invalid!")

class Client:
    PACKET_IDS = {
        "disconnect":0,
        "ping":1
        }
    def __init__(self, host, port=4949, headerlen=16):
        self.host = host
        self.port = port
        self.header = headerlen
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def send(self, json):
        """Send the data"""
        data = dumps(json)
        datalen = len(data)
        header = datalen.to_bytes(self.header, "big")
        
        self.socket.send(header+data.encode("utf-8"))

    def send_packet(self, packet_id, data={}):
        self.send({"request":packet_id, **data})
        
    def recv(self):
        """Wait for the server to respond with data"""
        datalen = int.from_bytes(self.socket.recv(self.header), "big")
        data = self.socket.recv(datalen)
        json = loads(data)
        return json
    
    def disconnect(self):
        """Sending to the server disconnection packet"""
        self.send_packet(PACKET_IDS["disconnect"])
        self.socket.close()
        
    def ping(self):
        """
Sending to the server current timestamp.
It will respond with time it took for packet to get recieved
        """
        timestamp = datetime.timestamp(datetime.now())
        self.send_packet(PACKET_IDS["ping"], {"timestamp":timestamp})
        response = self.recv()

        return response["diff"]
    
    def connect(self):
        """
Connect to the host you passed in constructor
        """
        self.socket.connect((self.host, self.port))

class Server:
    def __init__(self, host="127.0.0.1", port=4949, headerlen=16):
        self.host = host
        self.port = port
        self.header = headerlen
        self.clients = set()
        self.request_handlers = {0:self._handle_disconnect, 1:self._handle_ping}
        self.error_handling = self._handle_error
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def _handle_error(self, conn, exception):
        exception_cause = exception.args[0] if exception.args else exception.__class__.__name__
        self.send_packet(False, 0, {"error":exception_cause}, conn)
        if isinstance(exception, ClientError):
            return
        raise exception

    def _handle_disconnect(self, conn, _):
        conn.close()

    def _handle_ping(self, conn, data):
        client_time = data.get("timestamp")
        if client_time is None:
            raise TooLessData({"timestamp"})
        if not isinstance(client_time, int):
            raise InvalidData("timestamp")
        
        self.send_packet(True, 0, {"diff":datetime.timestamp(datetime.now())-client_time}, conn)

    def request_handler(self, packet_id):
        def wrapper(func):
            self.request_handlers[packet_id] = func
            return func
        return wrapper

    def error_handler(self, func):
        self.error_handling = func
        return func
        
            
    
    def send(self, json, conn):
        """Send the data"""
        data = dumps(json)
        datalen = len(data)
        header = datalen.to_bytes(self.header, "big")

        conn.send(header+data.encode("utf-8"))

    def send_packet(self, success, packet_type, data, conn):
        self.send({"success":success, "type":packet_type, "data":data}, conn)
    
    def recv(self, conn):
        """Recieve data from client"""
        datalen = int.from_bytes(conn.recv(self.header), "big")
        data = conn.recv(datalen)
        json = loads(data)
        return json

    def listen(self):
        """Loop of the server, it will wait for clients and handle them forever."""
        self.socket.listen()
        while True:
            conn, _ = self.socket.accept()
            thread = Thread(target=self.handle_client, args=(conn,))
            thread.start()
    
    def handle_request(self, conn, data):
        """Handles clients request"""
        action = data.get("request")
        function = self.request_handlers.get(action)
        if function is None:
            raise UnknownPacket(action)
        function(conn, data)

        
    def handle_client(self, conn):
        """Loop of handling the client"""
        conn_ip, conn_port = conn.getsockname()

        self.clients.add(conn)
        while True:
            try: data = self.recv(conn)
            except (Exception):
                break
            try:
                self.handle_request(conn,data)
            except Exception as exception:
                self.error_handling(conn, exception)
        self.clients.remove(conn)
        conn.close()
