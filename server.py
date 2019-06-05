#!/usr/bin/python3

import os
import socket
import threading
import json
import uuid
from log import Log

class Server:

    def __init__(self, portNumber):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = portNumber
        self.lock = threading.Lock()
        self.__start()



    """
     Starts listening on a port and controls handling incoming requests
    """
    def __start(self):
        try:
            self.serverSocket.bind((socket.gethostname(), self.port))
            self.serverSocket.listen(5)
            Log(f"Started listening on port {self.port}...")
        except Exception as e:
            Log(str(e))
            quit()

        try:
            while True:
                (clientsocket, clientaddress) = self.serverSocket.accept()
                threading.Thread(target = self.handleAuthRequest(clientsocket, clientaddress)).start()
        except Exception as e:
            Log(str(e))

    

    """
     TODO: Iron out authentication logic
    """
    def handleAuthRequest(self, clientsocket, clientaddress):
        try:
            clientsocket.settimeout(10)
            hostname = socket.gethostbyaddr(clientaddress[0])[0] # => (hostname, alias-list, IP)
            Log(f"Handling request from {hostname}.")

            # 1. Client sends E_s(N_c)
            clientname = self.decrypt('', clientsocket.recv(8192).decode())
            clientPublicKey = self.__getClientPublicKey(clientname)
            sessionKey = self.generateSessionKey()
            response = self.encrypt(clientPublicKey, f"{clientname}, {sessionKey}")
            Log(response)
            clientsocket.send(response.encode())

        except Exception as e:
            Log(str(e))
            clientsocket.send(str(e).encode())

        finally:
            clientsocket.close()



    """
     Reads and returns the client's public key from the store
    """
    def __getClientPublicKey(self, client):
        try:
            self.lock.acquire()
            with open('clients.json', 'r') as file:
                data = json.load(file)
                return data[client]

        finally:
            self.lock.release()



    """
     TODO: Actually encrypt the data
    """
    def encrypt(self, encryptionKey, data):
        return data


    
    """
     TODO: Actually decrypt the data
    """
    def decrypt(self, decryptionKey, data):
        return data

    

    """
     Generates random session key
    """
    def generateSessionKey(self):
        return str(uuid.uuid1())
    