import asyncio


class DiscordBot:
    """
    Create an object which allows you to register events on it for interacting with Discord while still having
        features such as logging and shared information available to the object
    """
    def __init__(self, logger, channels, admins, required_roles, games):
        """
        Initialize the object
        :param logger:
            A logger object for logging (duh).  It should already be configured to log wherever you want
        :param channels:
            A list of channels in which to listen for messages
        :param admins:
            A dict of people allowed to execute the more privileged commands.
            Note that "global" admins are allowed to do anything
            Additionally, "global" is always present (though it may be empty) while any other grouping is dependent
                on the game being loaded
            {
                'global':
                    [ ],
                'tf2':
                    [ ],
            }
        :param required_roles:
            A list of roles required for the bot to respond to users.  Useful for making it so non-registered
                users cannot do silly things
        :param games:
            A list of games. Basically a straight read from the config file at the moment, though this is expected
                to evolve into a list of "game" objects which can have commands executed on them
        """
        self.logger = logger
        self.channels = channels
        self.admins = admins
        self.roles = required_roles
        self.games = games

    def register_events(self, client):
        """
        The Discord library runs async, so we need to register functions to be called on events.
        :param client:
            An already configured and logged in Discord client
        :return:
        """
        @client.event
        async def on_ready():
            """
            We have successfully logged in (and are online)
            :return:
            """
            self.logger.warn("Logged in")
            print('Logged in as', client.user.name)

        @client.event
        async def on_message(message):
            """
            Parse messages for commands and pass the handling off
            :param message:
                Message object passed by the discord client
            :return:
                N/A
            """
            commands = [
                '!help',
                '!start',
                '!stop',
                '!status',
            ]

            full_local_user = str(client.user.name) + '#' + str(client.user.discriminator)

            # Do they have the appropriate roles?
            has_role = False
            for role in message.author.roles:
                if str(role) in self.roles:
                    has_role = True
                    break

            if has_role and str(message.author) != full_local_user and str(message.channel) in self.channels:
                for command in commands:
                    if str(message.content).startswith(command):
                        await client.send_typing(message.channel)
                        await handle_command(
                            command,
                            int(message.author.id),
                            str(message.content).replace(command, ''),
                            message.channel
                        )

        async def handle_command(command, user, game, channel):
            """
            Parse a chat command and invoke the appropriate function for it.
            :param command:
                String. Name of the command being executed.
            :param user:
                Integer. ID of the user executing a command.
            :param game:
                String. Name of the game being impacted (can be an empty string for certain commands)
            :param channel:
                Discord channel object. Used to send messages to.
            :return:
            """
            # Remove leading space if it exists
            if game and game[0] == ' ':
                game = game[1:]

            if not game and command != '!help':
                await client.send_message(channel, 'You must include a game.')
            elif command == '!help':
                await client.send_message(channel, 'Available commands: !start, !stop, !status.')
            elif command == '!start':
                if game in self.games:
                    self.games[game].get_start_command().execute()
                    await asyncio.sleep(5)
                    await client.send_message(channel, 'Server for ' + game + ' started!')
                else:
                    await client.send_message(channel, game + ' not supported!')
            elif command == '!stop':
                if user not in self.admins['global'] and user not in self.admins[game]:
                    await client.send_message(channel, 'You do not have permission to stop this game.')
                elif game in self.games:
                    # TODO: Actually stop the game
                    await asyncio.sleep(5)
                    await client.send_message(channel, 'Server for ' + game + ' stopped!')
                else:
                    await client.send_message(channel, game + ' not supported!')
            elif command == '!status':
                if game in self.games:
                    num_players = self.games[game].get_players_command().execute()
                    await asyncio.sleep(5)
                    await client.send_message(channel, game + ' has ' + num_players + ' players!')
                else:
                    await client.send_message(channel, game + ' not supported!')
            else:
                await client.send_message(channel, 'Unknown command.')
