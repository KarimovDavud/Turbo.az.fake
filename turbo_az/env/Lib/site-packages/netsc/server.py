import socket
from .netsc import NetworkScript

class Server(NetworkScript):
    sock_family = socket.AF_INET
    sock_type = socket.SOCK_STREAM
    sock_proto = 0
    bind_addr = ('', 0)
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.sock = socket.socket(self.sock_family, self.sock_type, self.sock_proto)
        self.sock.bind(self.bind_addr)
    def accept(self):
        self.sock.listen()
        sock, addr = self.sock.accept()
        self.sock = sock
        return addr

__all__ = ['Server']