import argparse
from .. import api
from .. import util

async def _run(args, user, channel, commands, environment):
    await api.send_message(' '.join(args.text), channel)

command = util.Command('echo', 'Echoes a message', util.levels.all, _run)
command.add_argument('text', metavar='TEXT', nargs='+', type=str)
