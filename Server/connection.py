#!/usr/bin/python3

import os
import subprocess


class Connection:

    __RECEIVE_TIMEOUT = 300 # seconds
    __BUFFER_SIZE = 8192
    __CLIENT_IDLE_TIMEOUT = 300 # seconds

    __clientsocket = None
    __clientaddress = None
    __availableCommands = set(['ls', 'mkdir', 'touch', 'cat', 'mv', 'cp', 'rm', 'rmdir'])



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
            while self.__clientsocket:
                try:
                    # Read what the client said
                    receivedMessage = self.__clientsocket.recv(self.__BUFFER_SIZE).decode()

                    # Execute a command
                    response = self.__execute(receivedMessage)
                    self.__clientsocket.send(response)
                
                except TimeoutError as e:
                    print(str(e))
                    self.__clientsocket.close()
                    self.__clientsocket = None
                except Exception as e:
                    self.__clientsocket.send(str(e).encode())
        finally:
            self.__clientsocket.close()



    """
     Executes bash commands, returns byte string
    """
    def __execute(self, commandString):
        cmds = [x.lower() for x in commandString.strip().split()]

        if (cmds[0] not in self.__availableCommands): 
            return f"Command not recognized. Available commands: {self.__availableCommands}".encode()

        process = subprocess.Popen(cmds, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if (error):
            return error
        elif (output.decode() == ''):
            return '\n'.encode()
        else:
            return output