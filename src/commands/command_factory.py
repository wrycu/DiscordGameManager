from src.commands.console_command import ConsoleCommand


class CommandFactory:
    @staticmethod
    def create(properties, commands):
        """
        Factory method to create game commands from the config.
        :param properties:
            dict config properties for the game
        :param commands:
            list commands that need to be created
        :return:
            Command[] List of commands for the game
        """
        result = []
        for command in commands:
            if command['type'] == 'console':
                result.append(ConsoleCommand(properties['install_dir'], command['text']))
            elif command['type'] == 'telnet':
                pass
            elif command['type'] == 'rcon':
                pass
            else:
                pass
        return result
