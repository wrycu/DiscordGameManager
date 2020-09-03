from src.commands.command import Command
import subprocess
import os


class ConsoleCommand(Command):
    def __init__(self, game_dir, command):
        self.game_dir = game_dir
        self.command = command

    def execute(self):
        try:
            proc = subprocess.Popen(self.game_dir + self.command, preexec_fn=os.setsid)
            return {
                'result': {
                    'pid': proc.pid,
                },
                'error': {
                    'errored': False,
                },
            }
        except Exception as e:
            return {
                'result': {},
                'error': {
                    'message': str(e),
                    'type': str(type(e)),
                    'errored': True,
                },
            }
