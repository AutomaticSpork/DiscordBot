from enum import Enum
import asyncio
import argparse
import json
from gettext import gettext as _, ngettext
from . import api

levels = Enum('Access', 'all owner none')

async def get_data(key):
    with open('data.json') as f:
        return json.loads(f.read())[key]

async def set_data(key, value):
    with open('data.json', 'r+') as f:
        data = json.loads(f.read())
        data[key] = value
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()

async def log(message):
    print(message)

class Task():
    def __init__(self, name, run):
        self.name = name
        self.run = run

class CommandContext():
    def __init__(self, command, channel):
        self.command = command
        self.channel = channel

    def __enter__(self):
        self.command.channel = self.channel

    def __exit__(self, type, value, td):
        self.command.channel = None


class Command(argparse.ArgumentParser):
    def __init__(self, name, description, access, run):
        super().__init__(prog=name, description=description)
        self.access = access
        self.run = run
        self.on_print = None
        self.is_error = False
        self.channel = None

    def print_usage(self, file=None):
        self.is_error = False
        super().print_usage(file)

    def print_help(self, file=None):
        self.is_error = False
        super().print_help(file)

    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _('%(prog)s error: %(message)s\n') % args)

    def exit(self, status=0, message=None):
        self.is_error = (status != 0)
        self._print_message(message)
        raise ValueError()

    def _print_message(self, message, file=None):
        if message and self.channel:
            asyncio.ensure_future(api.send_message('', self.channel, {
                'title': 'Error' if self.is_error else '',
                'color': 0xd50000 if self.is_error else 0x304ffe,
                'description': message
            }))