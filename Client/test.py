from client import Client
from config import Config
import socket

c = Client()

if ( c.authenticate(Config.setting('serverName'), Config.setting('serverPort')) ):
    while True:
        print(c.readCommand(Config.setting('serverName')))