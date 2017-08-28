from enum import Enum

levels = Enum('Access', 'all, owner')

async def log(message):
    print(message)
