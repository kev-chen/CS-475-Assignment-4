from client import Client
import socket

c = Client(3002)

c.authenticate(socket.gethostname(), 3002)