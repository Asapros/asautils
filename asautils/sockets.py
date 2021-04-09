import socket
from pickle import loads, dumps
from datetime import datetime
from threading import Thread
from asautils.logger import Logger

class Client:
    def __init__(self, host, port, headerlen):
        self.host = host
        self.port = port
        self.header = headerlen
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def send(self, data):
        datalen = len(data)
        header = str(datalen) + " "*(self.header-len(str(datalen)))
        self.socket.send(header.encode("utf-8")+data)
    def recv(self):
        msglen = int(self.socket.recv(self.header))
        msg = self.socket.recv(msglen)
        return msg
    def disconnect(self):
        self.send(dumps({"action":0}))
    def ping(self):
        timestamp = datetime.timestamp(datetime.now())
        self.send(dumps({"action":1, "timestamp":timestamp}))
        return loads(self.recv())["timestamp"] - timestamp
    def connect(self):
        self.socket.connect((self.host, self.port))

class Server:
    def __init__(self, host, port, headerlen):
        self.host = host
        self.port = port
        self.header = headerlen
        self.clients = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def send(self, data, conn):
        datalen = len(data)
        header = str(datalen) + " "*(self.header-len(str(datalen)))
        conn.send(header.encode("utf-8")+data)
        
    def recv(self, conn):
        msglen = int(conn.recv(self.header))
        msg = conn.recv(msglen)
        return msg

    def listen(self):
        self.socket.listen()
        while True: Thread(target=self.handle_client, args=self.socket.accept()).start()
        
    def handle_action(self, conn, addr, data):
        action = data["action"]
        if action == 0: # DISCONNECT
            return 0
        elif action == 1: # PING
            self.send(dumps({"timestamp":datetime.timestamp(datetime.now())}), conn)

    def on_client_connect(self, conn, addr): pass
    
    def handle_client(self, conn, addr):
        Logger.info("Handling new client: %s:%d" % addr)
        self.clients.add(conn)
        self.on_client_connect(conn, addr)
        while True:
            try: data = loads(self.recv(conn))
            except (ConnectionResetError, ValueError): break # Lost connection or disconnected due to error
            if "action" in data.keys():
                value = self.handle_action(conn,addr,data)
                if value == 0: break
        Logger.info("%s:%d disconnected" % addr)
        self.clients.remove(conn)
        conn.close()
