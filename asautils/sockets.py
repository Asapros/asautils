"""
a socket wrapper
"""

import socket
from pickle import loads, dumps
from datetime import datetime
from threading import Thread
from asautils.logger import Logger
from copy import copy

class Client:
    def __init__(self, host="127.0.0.1", port=4949, headerlen=16):
        self.host = host
        self.port = port
        self.header = headerlen
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def send(self, data):
        """Send the data. If your sending a dict, remember to pickle it first!
        """
        datalen = len(data)
        header = str(datalen) + " "*(self.header-len(str(datalen)))
        self.socket.send(header.encode("utf-8")+data)
        
    def recv(self):
        """Wait for the server to respond with data"""
        msglen = int(self.socket.recv(self.header))
        msg = self.socket.recv(msglen)
        return msg
    
    def send_data(self, data):
        """
Passing the data to server.on_data_recv
In most cases you should use this instead of normal send.
        """
        self.send(dumps({"action":2, "data":data}))
        
    def disconnect(self):
        """Sending to the server quick {"action":0} to tell it you want to abort connection."""
        self.send(dumps({"action":0}))
        
    def ping(self):
        """
Sending to the server current timestamp.
It will respond with it's timestamp so we can calculate how many time it took to send and then recieve the message
        """
        timestamp = datetime.timestamp(datetime.now())
        self.send(dumps({"action":1, "timestamp":timestamp}))
        return loads(self.recv())["timestamp"] - timestamp
    
    def connect(self):
        """
Connect to the host you passed in __init__
        """
        self.socket.connect((self.host, self.port))

class Server:
    def __init__(self, host="127.0.0.1", port=4949, headerlen=16):
        self.host = host
        self.port = port
        self.header = headerlen
        self.clients = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def send(self, data, conn):
        """Send the data to connected client"""
        datalen = len(data)
        header = str(datalen) + " "*(self.header-len(str(datalen)))
        conn.send(header.encode("utf-8")+data)
        
    def recv(self, conn):
        """Recieve data from client"""
        msglen = int(conn.recv(self.header))
        msg = conn.recv(msglen)
        return msg

    def listen(self):
        """Loop of the server, it will wait for clients and handle them forever."""
        self.socket.listen()
        threads = set()
        while True:
            for thread in copy(threads):
                if not thread.isAlive():
                    thread.join()
                    threads.remove(thread)
            thread = Thread(target=self.handle_client, args=self.socket.accept())
            thread.start()
            threads.add(thread)

    def on_data_recv(self, conn, addr, data):
        print("%s:%d sends: %s" % (*addr, data))
    
    def handle_action(self, conn, addr, data):
        """Handles clients request"""
        action = data["action"]
        if action == 0: # DISCONNECT
            conn.close()
        elif action == 1: # PING
            self.send(dumps({"timestamp":datetime.timestamp(datetime.now())}), conn)
        elif action == 2: # DATA
            self.on_data_recv(conn, addr, data["data"])

    def on_client_connect(self, conn, addr):
        """Called when client connected"""
        Logger.info("Handling new client: %s:%d" % addr)
        self.clients.add(conn)

    def on_client_disconnect(self, conn, addr):
        """Called when client disconnected"""
        Logger.info("%s:%d disconnected" % addr)
        self.clients.remove(conn)
        conn.close()
        
    def handle_client(self, conn, addr):
        """Loop of handling the client"""
        self.on_client_connect(conn, addr)
        while True:
            try: data = loads(self.recv(conn))
            except (ConnectionResetError, ValueError, OSError):
                break # Connection no longer exists, or for example wrong header is passed
            if "action" in data.keys():
                self.handle_action(conn,addr,data)
            else:
                self.send(dumps({"error":"No 'action' key in recieved data"}), conn)
        self.on_client_disconnect(conn, addr)
