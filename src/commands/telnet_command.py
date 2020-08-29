import re

from src.commands.command import Command


class TelnetCommand(Command):
    """
    An object encapsulating the socket communication when interacting with a game server that uses Telnet
    for remote management.
    """
    def __init__(self, port, command, password=None, regex=None):
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
            Result of the command being executed
        """
        super(TelnetCommand, self).__init__()
        self.port = port
        self.password = password
        self.command = command
        self.regex = regex

    def execute(self):
        self.soc.connect(("localhost", self.port))

        # Wait for connected message
        self.read_socket()

        if self.password:
            # Send password
            self.write_socket(self.password)

            # Wait for server greeting
            self.read_socket()

        # Send command
        self.write_socket(self.command)

        result = self.read_socket()
        self.soc.close()
        if not self.regex:
            return result

        matches = re.search(self.regex, result)
        if matches:
            return matches.group(1)
        else:
            raise Exception("Command result did not match regex")
