from client import Client
from config import Config
import socket

c = Client()

if ( c.authenticate(Config.setting('serverName'), Config.setting('serverPort')) ):
    try:
        while True:
            resp = c.readCommand()
            if (resp != '\n'):
                print(resp)
            if (resp == 'Goodbye'):
                quit()
    finally:
        c.quit()