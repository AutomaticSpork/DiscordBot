import argparse
from .. import api
from .. import util

access = util.levels.all
args = util.BotArgs(description='Echoes a message', prog='echo')
args.add_argument('text', type=str)

async def run(args, user, channel, commands, environment):
    await api.send_message(args.text, channel)