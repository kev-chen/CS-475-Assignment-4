#!/usr/bin/env python3

import os
import subprocess
from config import Config


class Connection:

    __RECEIVE_TIMEOUT = Config.setting('clientTimeout')
    __BUFFER_SIZE = Config.setting('maxBufferSize')

    __clientsocket = None
    __clientaddress = None
    __availableCommands = set(['ls', 'mkdir', 'touch', 'cat', 'mv', 'cp', 'rm', 'rmdir', 'quit', 'pwd'])



    """
     @param client = (clientsocket, clientaddress) as returned from a socket.accept()
    """
    def __init__(self, client, privatekey):
        self.__clientsocket = client[0]
        self.__clientaddress = client[1]

        # Set a timeout to avoid hanging on reading from client Timeout errors 
        # on reading from socket are handled by handleRequests
        self.__clientsocket.settimeout(self.__RECEIVE_TIMEOUT)



    """
     Drives the socket listening for messages from the client and acts on them
    """
    def listen(self):
        try:
            while True:
                # Read what the client said
                receivedMessage = self.__clientsocket.recv(self.__BUFFER_SIZE).decode()

                # Execute a command
                response = self.__execute(receivedMessage)
                self.__clientsocket.send(response)

                if (response == b'Goodbye'):
                    break
                    
        except Exception as e:
            self.__clientsocket.send(str(e).encode())

        finally:
            if (self.__clientsocket != None):
                self.__clientsocket.close()
                self.__clientsocket = None



    """
     Executes bash commands, returns byte string
    """
    def __execute(self, commandString):

        cmds = [x.lower() for x in commandString.strip().split()]

        if (cmds[0] not in self.__availableCommands): 
            return f"Command not recognized. Available commands: {self.__availableCommands}".encode()
        
        if (cmds[0] == 'quit'):
            return 'Goodbye'.encode()

        process = subprocess.Popen(cmds, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if (error):
            return error
        elif (output.decode() == ''):
            return '\n'.encode()
        else:
            return output