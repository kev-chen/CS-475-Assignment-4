#!/usr/bin/python3

import os
import socket
import threading
import json
import uuid
from log import Log
from Crypto.PublicKey import RSA

class Client:

    def __init__(self, portNumber):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = portNumber
        self.clientName = 'test_client_name'
        self.__start()



    """
     Sends the initial authentication request to the server
     TODO: Remove the finally block and add on-authenticated behavior
    """
    def __start(self):
        try:
            self.socket.connect( (socket.gethostname(), self.port) )
            message = self.encrypt(self.__getServerPublicKey(), self.clientName)

            self.socket.send(message)
            response = self.decrypt(self.__getPrivateKey(), self.socket.recv(8192)).decode()

            # Response was correct
            if (self.clientName == response[:response.find(',')]):
                print(f"{response[:response.find(',')]}, {response[response.find(',')+1:]}")
            else:
                print("AUTHENTICATION FAILED")
        except Exception as e:
            Log(str(e))
        finally:
            self.socket.close()



    """
     Reads and returns the client's public key from the store
    """
    def __getServerPublicKey(self,):
        with open('server_public_key.pem', 'rb') as file:
            return RSA.importKey(file.read())

    

    """
     Reads and returns the client's private key
    """
    def __getPrivateKey(self):
        with open('client_private_key.pem', 'rb') as file:
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