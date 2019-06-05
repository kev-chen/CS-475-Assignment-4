#!/usr/bin/python3

import os
import socket
import threading
import json
import uuid
from log import Log

class Client:

    def __init__(self, portNumber):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = portNumber
        self.clientName = socket.gethostname()
        self.__start()



    """
     Sends the initial authentication request to the server
     TODO: Remove the finally block and add on-authenticated behavior
     TODO: Handle the keys, unrecognized response from server
    """
    def __start(self):
        try:
            self.socket.connect( (socket.gethostname(), self.port) )
            encryptedMessage = self.encrypt('', self.clientName)
            self.socket.send(encryptedMessage.encode())
            encryptedResponse = self.socket.recv(8192).decode()
            print(encryptedResponse)
        finally:
            self.socket.close()



    """
     Reads and returns the client's public key from the store
    """
    def __getServerPublicKey(self, key):
        with open('serverKey.json', 'r') as file:
            data = json.load(file)
            return data[key]

    

    """
     Reads and returns this client's private key
    """
    def __getPrivateKey(self):
        with open('privatekey.json', 'r') as file:
            data = json.load(file)
            return data[key]



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