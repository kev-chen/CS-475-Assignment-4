#!/usr/bin/env python3

from server import Server
from config import Config

s = Server(Config.setting('serverPort'))