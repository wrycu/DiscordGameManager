import abc
import socket
import time


class Command:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @abc.abstractmethod
    def execute(self):
        pass

    def write_socket(self, data):
        self.soc.send((data + "\n").encode("utf-8"))

    def read_socket(self):
        # We are receiving data from localhost so it shouldn't take long
        timeout = 0.1
        buffer_size = 2048

        self.soc.setblocking(0)
        data = []
        begin = time.time()
        while 1:
            # If we have data then break after the timeout
            if data and time.time() - begin > timeout:
                break
            # If we have no data then wait a bit longer
            if time.time() - begin > timeout * 5:
                raise Exception("Request timed out")

            try:
                chunk = self.soc.recv(buffer_size)
                if chunk:
                    begin = time.time()
                    data.append(chunk)
                else:
                    time.sleep(0.1)
            except BlockingIOError:
                # If attempting to read from an empty receive buffer this
                # exception will be thrown. We don't care about it.
                pass
        self.soc.setblocking(1)
        return ''.join(str(x) for x in data)