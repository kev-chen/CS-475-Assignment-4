#!/usr/bin/env python3

import subprocess
from config import Config


class Connection:

    __RECEIVE_TIMEOUT = Config.setting('clientTimeout')
    __BUFFER_SIZE = Config.setting('maxBufferSize')
    __AVAILABLE_COMMANDS = set(['ls', 'quit', 'pwd'])


    """
     @param client = (clientsocket, clientaddress) as returned from a socket.accept()
    """
    def __init__(self, client, sessionKey):
        self.__clientsocket = client[0]
        self.__clientaddress = client[1]
        self.__sessionKey = sessionKey

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
        receivedSessionKey = commandString[:commandString.find(':')]
        if (receivedSessionKey != self.__sessionKey):
            raise Exception('Invalid session key. Closing connection.')

        cmds = [x.lower() for x in commandString[commandString.find(':')+1:].strip().split()]

        if (cmds[0] not in self.__AVAILABLE_COMMANDS): 
            return f"Command not recognized. Available commands: {self.__AVAILABLE_COMMANDS}".encode()
        
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