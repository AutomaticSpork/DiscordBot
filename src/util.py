from enum import Enum
import asyncio
import argparse

levels = Enum('Access', 'all, owner')

async def log(message):
    print(message)

class BotArgs(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        if message:
            if self.on_print:
                asyncio.ensure_future(self.on_print(message))