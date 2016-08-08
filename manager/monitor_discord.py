import discord
import asyncio

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as', client.user.name)


@client.event
async def on_message(message):
    """
    The bot has received a message
    :param message:
        Message object passed by the discord client
    :return:
        N/A
    """
    # TODO: Read this from the config object
    channels = [
        'testeroni'
    ]
    roles = [
        'member',
    ]
    commands = [
        '!help',
        '!start',
        '!stop'
    ]

    full_local_user = str(client.user.name) + '#' + str(client.user.discriminator)

    # Do they have the appropriate roles?
    has_role = False
    for role in message.author.roles:
        if str(role) in roles:
            has_role = True
            break

    if str(message.author) != full_local_user and str(message.channel) in channels and has_role:
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
    # Remove leading space
    if game and game[0] == ' ':
        game = game[1:]
    # TODO: Read from config object
    # Global admins can do anything to anything
    global_admins = [
        108005836579696640,  # Tim
    ]

    # Game admins can only change their own games
    game_admins = {
        'tf2': [
            108337116919910400,  # Jeremy
        ],
        'empyrion': [],
    }

    if not game and command != '!help':
        await client.send_message(channel, 'You must include a game.')
    elif command == '!help':
        await client.send_message(channel, 'Available commands: !start, !stop, !status.')
    elif command == '!start':
        if game in game_admins.keys():
            # TODO: Actually start the game
            await asyncio.sleep(5)
            await client.send_message(channel, 'Server for ' + game + ' started!')
        else:
            await client.send_message(channel, game + ' not supported!')
    elif command == '!stop':
        if user not in global_admins and user not in game_admins[game]:
            await client.send_message(channel, 'You do not have permission to stop this game.')
        elif game in game_admins.keys():
            # TODO: Actually stop the game
            await asyncio.sleep(5)
            await client.send_message(channel, 'Server for ' + game + ' stopped!')
        else:
            await client.send_message(channel, game + ' not supported!')
    elif command == '!status':
        if game in game_admins.keys():
            # TODO: Actually get the status of the game
            await asyncio.sleep(5)
            await client.send_message(channel, game + ' has two players!')
        else:
            await client.send_message(channel, game + ' not supported!')
    else:
        await client.send_message(channel, 'Unknown command.')

# TODO: move to config file. When Kevin is done with that part
client.run('KEY_FROM_CONFIG_FILE')
