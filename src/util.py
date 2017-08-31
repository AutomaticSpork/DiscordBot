from enum import Enum
import asyncio
import argparse

levels = Enum('Access', 'all, owner')

async def log(message):
    print(message)

class Task():
    pass

class Command(argparse.ArgumentParser):
    def __init__(self, name, description, access, run):
        super().__init__(prog=name, description=description)
        self.access = access
        self.run = run

    def _print_message(self, message, file=None):
        if message:
            if self.on_print:
                asyncio.ensure_future(self.on_print(message))