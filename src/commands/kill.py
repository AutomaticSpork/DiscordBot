import sys
import argparse
from .. import api
from .. import util

async def _run(args, user, channel, commands, environment):
    if args.sad_bot:
        await api.send_message('Killing :(', channel)
    else:
        await api.send_message('Killing', channel)
    sys.exit()

command = util.Command('kill', 'Kills the bot', util.levels.owner, _run)
command.add_argument('-s', '--sad-bot', dest='sad_bot', action='store_true', required=False)
