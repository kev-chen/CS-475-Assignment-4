#!/usr/bin/python3

import os
import socket
import threading
import json
import uuid
from Crypto.PublicKey import RSA

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
            print(f"Started listening on port {self.port}...")
        except Exception as e:
            print(str(e))
            quit()

        try:
            while True:
                (clientsocket, clientaddress) = self.serverSocket.accept()
                threading.Thread(target = self.handleAuthRequest(clientsocket, clientaddress)).start()
        except Exception as e:
            print(str(e))

    

    """
     TODO: Add on-authentication behavior
    """
    def handleAuthRequest(self, clientsocket, clientaddress):
        try:
            clientsocket.settimeout(10)
            hostname = socket.gethostbyaddr(clientaddress[0])[0] # => (hostname, alias-list, IP)
            print(f"Handling request from {hostname}.")

            # 1. Client sends E_s(N_c)
            clientname = self.decrypt(self.__getPrivateKey(), clientsocket.recv(8192)).decode()
            sessionKey = self.generateSessionKey()
            response = self.encrypt(self.__getClientPublicKey(clientname), f"{clientname},{sessionKey}")
            clientsocket.send(response)

        except Exception as e:
            print(str(e))
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
                pemFileName = data[client]
                with open(pemFileName, 'rb') as pemFile:
                    return RSA.importKey(pemFile.read())

        finally:
            self.lock.release()



    """
     Reads and returns the server's private key
    """
    def __getPrivateKey(self):
        with open('server_private_key.pem', 'rb') as file:
            return RSA.importKey(file.read())



    """
     Encrypts data given an RSA public key
    """
    def encrypt(self, encryptionKey, data):
        return encryptionKey.encrypt(data.encode(), 32)[0]


    
    """
     Decrypts data given an RSA private key
    """
    def decrypt(self, decryptionKey, data):
        return decryptionKey.decrypt(data)

    

    """
     Generates random session key
    """
    def generateSessionKey(self):
        return str(uuid.uuid1())
    