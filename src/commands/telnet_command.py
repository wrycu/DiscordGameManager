import re
import socket
import time

from src.commands.command import Command


class TelnetCommand(Command):
    """
    An object encapsulating the socket communication when interacting with a game server that uses Telnet
    for remote management.
    """
    def __init__(self, ip_addr, port, command, password=None, regex=None):
        """
        Initializes the object
        :param port:
            The port to open with telnet
        :param command:
            The command to run once connected
        :param password:
            Optional password that server management uses
        :param regex:
            Optional regex to parse result of command. If there is no match (unexpected output) and Exception
            will be raised
        :return:

        """

        self.ip_addr = ip_addr
        self.port = port
        self.password = password
        self.command = command
        self.regex = regex
        self.soc = None

    def execute(self):
        self.prime_socket()

        self.soc.connect((self.ip_addr, self.port))

        # Wait for connected message
        self.read_socket()

        if self.password:
            # Send password
            self.write_socket(self.password)

            # Wait for server greeting
            self.read_socket()

        # Send command
        self.write_socket(self.command)

        result_data = self.read_socket()
        result = {
            'result': {
                'text': result_data,
                'matched': True,
            },
            'error': {
                'errored': False,
            },
        }
        self.soc.close()
        if self.regex:
            matches = re.search(self.regex, result_data)
            if matches:
                result['result']['match'] = matches.group(1)
            else:
                result['result']['matched'] = False
                result['error']['errored'] = True
                result['error']['message'] = 'Command result did not match regex'

        return result

    def prime_socket(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
