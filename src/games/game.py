from src.games.game_type import GameType
from src.commands.telnet_command import TelnetCommand
from src.commands.console_command import ConsoleCommand


class Game:
    def __init__(self, info):
        self.info = info

    def name(self):
        return self.info["name"]

    def kill_empty(self):
        return self.info["kill_empty"]

    def get_start_command(self):
        return ConsoleCommand(self.info["commands"]["start"]["command"])

    def get_stop_command(self):
        # should be more or less the same as players
        pass

    def get_update_command(self):
        # skip for first cut
        pass

    def get_connect_command(self):
        # might not need this
        # might want to use this to prime a socket
        pass

    def get_players_command(self):
        try:
            game_type = GameType[self.info["type"]]
        except KeyError:
            raise Exception("GameType was not valid")

        command = {
            GameType.telnet: self.__make_telnet_command("players"),
        }[game_type]

        return command

    def get_version_command(self):
        # skip for first cut
        pass

    def get_delay_command(self):
        # Server closing in X minutes message thing
        # should be more or less the same as players
        pass

    def __make_telnet_command(self, command_type):
        return TelnetCommand(
            self.info["port"],
            self.info["commands"][command_type]["command"],
            self.info["password"],
            self.info["commands"][command_type]["regex"],
        )
