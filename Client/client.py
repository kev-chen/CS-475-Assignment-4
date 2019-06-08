#!/usr/bin/env python3

import os
import socket
import threading
import json
import uuid
from Crypto.PublicKey import RSA
from config import Config

class Client:

    __BUFFER_SIZE = Config.setting('maxBufferSize')

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientName = Config.setting('clientName')
        self.__serverName = None
        self.__authenticated = False



    """
     Sends the initial authentication request to the server
    """
    def authenticate(self, serverHost, port):
        try:
            self.socket.connect( (serverHost, port) )
            self.__serverName = serverHost
            # Send the client name encrypted with the server's public key
            message = self.encrypt(self.__getServerPublicKey(), self.clientName)
            self.socket.send(message)

            # Get the response from the server, which is encyrpted with client's public key
            response = self.decrypt(self.__getPrivateKey(), self.socket.recv(self.__BUFFER_SIZE)).decode()

            returnedClientName = response[:response.find(',')]
            returnedSessionKey = response[response.find(',')+1:]

            # Response was correct
            if (self.clientName == returnedClientName):
                print(f"Successfully authorized. Server response: {response}")
                self.__authenticated = True
                return True
            else:
                raise Exception("Authentication Failed")

        except Exception as e:
            print("Authentication Failed")
            return False



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


    
    """
     Send commands to the server
    """
    def readCommand(self):
        command = input(f'{self.__serverName}> ')
        if (self.__authenticated):
            command = command.encode()
            self.socket.send(command)
            return self.socket.recv(self.__BUFFER_SIZE).decode()
        else:
            return 'Not connected'


    
    """
     Quits the client and cleans up connections
    """
    def quit(self):
        self.__authenticated = False
        if (self.socket != None):
            self.socket.close()
            self.socket = None