from src.commands.command_factory import CommandFactory


class Game:
    def __init__(self, info):
        self.info = info
        self.commands = {}

    def name(self):
        return self.info["name"]

    def kill_empty(self):
        return self.info["kill_empty"]

    def get_start_command(self):
        return self.__get_command('start')

    def get_stop_command(self):
        return self.__get_command('stop')

    def get_update_command(self):
        # skip for first cut
        pass

    def get_connect_command(self):
        # might not need this
        # might want to use this to prime a socket
        pass

    def get_players_command(self):
        return self.__get_command('players')

    def get_version_command(self):
        # skip for first cut
        pass

    def get_delay_command(self):
        # Server closing in X minutes message thing
        # should be more or less the same as players
        pass

    def __get_command(self, command_type):
        """
        Fetches the requested command from the cache if it exists, otherwise creates it
        :param command_type:
            The type of the command to get
        :return:
            An instance of the command
        """
        if self.commands[command_type]:
            return self.commands[command_type]

        command = CommandFactory.create(self.info['properties'], self.info['commands'][command_type])
        self.commands[command_type] = command

        return command
