from manager.objects.command import Command
import re


class TelnetCommand(Command):
    def __init__(self, port, command, password=None, regex=None):
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
        if not self.regex:
            return result

        matches = re.search(self.regex, result)
        if matches:
            return matches.group(1)
        else:
            raise Exception("Command result did not match regex")
