# Abstract representation of a connection to a cluster
class Connection(object):
    def execute(self, command):
        raise NotImplementedError("Implemented by subclass")

    def __enter__(self):
        raise NotImplementedError("Implemented by subclass")

    def __exit__(self, type, value, traceback):
        raise NotImplementedError("Implemented by subclass")