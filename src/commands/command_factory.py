from src.commands.console import ConsoleCommand
from src.commands.telnet import TelnetCommand


class CommandFactory:
    @staticmethod
    def create(properties, command):
        """
        Factory method to create a game command from the config.
        :param properties:
            dict config properties for the game
        :param command:
            object command that needs to be created
        :return:
            Command A command for the game
        """
        if command['type'] == 'console':
            return ConsoleCommand(properties['install_dir'], command['text'])
        elif command['type'] == 'telnet':
            return TelnetCommand(properties['ip_addr'], properties['port'], command['text'], command['regex'])
        elif command['type'] == 'rcon':
            return None
        else:
            return None
