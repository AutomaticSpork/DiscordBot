import argparse
from .. import api
from .. import util

access = util.levels.all
args = util.BotArgs(description='Lists commands', prog='help')
args.add_argument('cats', type=str)

async def run(args, user, channel, commands, environment):
    await api.send_message('\n'.join(['**%s%s**: %s' % (environment['commandStart'], k, v.args.description) for k, v in commands.items()]), channel)