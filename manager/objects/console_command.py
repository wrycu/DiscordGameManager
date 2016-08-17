from manager.objects.command import Command
import subprocess
import os


class ConsoleCommand(Command):
    def __init__(self, command):
        self.command = command

    def execute(self):
        proc = subprocess.Popen(self.command, preexec_fn=os.setsid)
        return proc.pid
