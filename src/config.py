import logging
import os
from json import load

import discord
from jsonschema import validate

from src.config_schema import config_schema
from src.games.game import Game
from src.loops.monitor_discord import DiscordBot
from src.loops.monitor_games import MonitorGames


class Config:
    def __init__(self, config_file=os.path.join(os.path.pardir, 'conf', 'config.json')):
        self._configure_logger()
        with open(config_file) as data_file:
            data = load(data_file)
        data_file.close()
        validate(data, config_schema)
        self.discord_user = data['discord']['username']
        self.discord_token = data['discord']['oauth_token']
        self.channels = data['discord']['channels']
        self.admins = {
            'global': data['discord']['global_admins'],
        }
        self.games = {}
        for attrs in data['games']:
            self.admins[attrs['name']] = attrs['admins']
            if attrs['name'] not in self.games:
                self.games[attrs['name']] = Game(attrs)
        self.required_roles = data['discord']['required_roles']
        monitor = MonitorGames(self.logger, self.games)
        self.discord_client = discord.Client(loop=monitor.loop)
        bot = DiscordBot(self.logger, self.channels, self.admins, self.required_roles, self.games)
        bot.register_events(self.discord_client)
        self.discord_client.run(self.discord_token)

    def _configure_logger(self):
        """
        Creates and configures a logger to log to "game_manager.log"
        :return:
        """
        self.logger = logging.getLogger('DiscordGameManager')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('game_manager.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
