import socket
from .netsc import NetworkScript

class Client(NetworkScript):
    sock_family = socket.AF_INET
    sock_type = socket.SOCK_STREAM
    sock_proto = 0
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.sock = socket.socket(self.sock_family, self.sock_type, self.sock_proto)
    def connect(self, addr):
        self.sock.connect(addr)

__all__ = ['Client']