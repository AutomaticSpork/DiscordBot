from enum import Enum
import asyncio
import argparse
import json
from . import api

levels = Enum('Access', 'all owner')

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
        self.command.set_callback(self.channel)

    def __exit__(self, type, value, td):
        self.command.clear_callback()


class Command(argparse.ArgumentParser):
    def __init__(self, name, description, access, run):
        super().__init__(prog=name, description=description)
        self.access = access
        self.run = run
        self.on_print = None

    def _print_message(self, message, file=None):
        if message:
            if self.on_print:
                asyncio.ensure_future(self.on_print(message))

    def set_callback(self, channel):
        async def print_callback(m):
            await api.send_message('```' + m + '```', channel)
        self.on_print = print_callback

    def clear_callback(self):
        self.on_print = None