import asyncio


class MonitorGames:
    def __init__(self, logger, games):
        """
        Start the event loop which will actually monitor games for their status and perform actions
        The Discord bot will run on the same event loop
        :param logger:
            A logger object for logging (duh).  It should already be configured to log wherever you want
        :param games:
            A list of game game which we are supposed to check on the status of
        :return:
            An event loop which can be used to run other functions on the same loop
        """
        self.logger = logger
        self.games = games
        loop = asyncio.get_event_loop()
        self.loop = loop
        self.loop.call_later(1, self.monitor_loop)

    def monitor_loop(self):
        """
        Monitor games
        Checks for two major things:
            Servers with <1 players on them (some of these will be killed)
            Duplicate instances of servers running (which generally means something went wrong)
        :return:
        """
        try:
            self.logger.info("Beginning to check game status")
            for game in self.games:
                self.logger.info("Checking {}...".format(game))
                self.check_player_count(game)
                self.find_dupe_servers(game)
            self.loop.call_later(90, self.monitor_loop)
        except Exception as e:
            self.logger.error("Encountered error while attempting to check game status: {}".format(e))
            self.loop.stop()

    def find_dupe_servers(self, game):
        """
        Determine if there is more than one server for the same game running
        This can happen if we fail starting or stopping a game.
        Not entirely sure how we'll do this - probably connect to the management interface, shut it down gracefully,
            then kill remaining processes with the same name.  This avoids doing an abrupt shutdown to the server
            actually servicing players
        :param game:
        :return:
        """
        pass

    def check_player_count(self, game):
        """
        Determine if there are any players on the server and kill it if there are not
            (and we wish to close servers with no players)
        :param game:
            The name of the game you wish to check the status of
        :return:
        """
        if not self.games[game].get_players_command().execute():
            # TODO: implement check if we actually care about there being no players on this server
            # The game is running and has no players
            self.logger.info("{} has no players! Stopping".format(game))
            self.games[game].get_stop_command().execute()
