import paramiko

from .connection import Connection


# Representation of an ssh connection to a cluster
class SSHConnection(Connection):
    def __init__(self, cluster):
        self._cluster = cluster

    def execute(self, command):
        raise NotImplementedError("Implemented by subclass")

    def __enter__(self):
        raise NotImplementedError("Implemented by subclass")

    def __exit__(self):
        raise NotImplementedError("Implemented by subclass")