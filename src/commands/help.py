import argparse
from .. import api
from .. import util

async def _run(args, user, channel, commands, environment):
    async def print_callback(m):
        await api.send_message('```' + m + '```', channel)
    if args.verbose:
        for _, command in commands.items():
            command.on_print = print_callback
            command.print_help()
            command.on_print = None
    else:
        await api.send_message('\n'.join(['**%s%s**: %s' % (environment['commandStart'], k, v.description) for k, v in commands.items()]), channel)

command = util.Command('help', 'Lists commands', util.levels.all, _run)
command.add_argument('-v', dest='verbose', action='store_true')
