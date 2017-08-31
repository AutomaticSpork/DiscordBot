import argparse
from .. import api
from .. import util

access = util.levels.all
args = util.BotArgs(description='Lists commands', prog='help')
args.add_argument('-v', dest='verbose', action='store_true')

async def run(args, user, channel, commands, environment):
    async def print_callback(m):
        await api.send_message('```' + m + '```', channel)
    if args.verbose:
        for _, command in commands.items():
            command.args.on_print = print_callback
            command.args.print_help()
            command.args.on_print = None
    else:
        await api.send_message('\n'.join(['**%s%s**: %s' % (environment['commandStart'], k, v.args.description) for k, v in commands.items()]), channel)