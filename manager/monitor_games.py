import asyncio


def monitor_games(loop):
    """
    Monitor games
    :param loop:
    :return:
    """
    # TODO:
    #  1. Actually monitor games
    #  2. Configure an actual try / except block which logs failures (possibly even sending them to Discord)
    try:
        print("hello")
        loop.call_later(60, monitor_games, loop)
    except Exception:
        loop.stop()


def create_game_loop():
    """
    Start the event loop which will actually monitor games for their status and perform actions
    The Discord bot will run on the same event loop
    :return:
        An event loop which can be used to run other functions on the same loop
    """
    loop = asyncio.get_event_loop()
    loop.call_later(60, monitor_games, loop)
    return loop
