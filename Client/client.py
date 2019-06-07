#!/usr/bin/python3

import os
import socket
import threading
import json
import uuid
from Crypto.PublicKey import RSA
from config import Config

class Client:

    def __init__(self, portNumber):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientName = Config.setting('clientName')



    """
     Sends the initial authentication request to the server
     TODO: Remove the finally block and add on-authenticated behavior
    """
    def authenticate(self, serverHost, port):
        try:
            self.socket.connect( (serverHost, port) )

            # Send the client name encrypted with the server's public key
            message = self.encrypt(self.__getServerPublicKey(), self.clientName)
            self.socket.send(message)

            # Get the response from the server, which is encyrpted with client's public key
            response = self.decrypt(self.__getPrivateKey(), self.socket.recv(8192)).decode()

            returnedClientName = response[:response.find(',')]
            returnedSessionKey = response[response.find(',')+1:]

            # Response was correct
            if (self.clientName == returnedClientName):
                print(f"{returnedClientName}, {returnedSessionKey}")
            else:
                raise Exception("AUTHENTICATION FAILED")
        except Exception as e:
            print(str(e))
        finally:
            self.socket.close()



    """
     Reads and returns the client's public key from the store
    """
    def __getServerPublicKey(self):
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