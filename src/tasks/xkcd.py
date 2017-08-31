import asyncio
import json
from .. import api
from .. import util

async def _run(commands, environment):
    latest = await util.get_data('xkcdLatest')
    channels = await util.get_data('xkcdChannels')
    response = json.loads(await api.web_call('get', 'http://xkcd.com/info.0.json'))
    if response['num'] > latest:
        for channel in channels:
            print('Running for ' + channel)
            with util.CommandContext(commands['xkcd'], channel):
                args = commands['xkcd'].parse_args([])
                await commands['xkcd'].run(args, '0', channel, commands, environment)
        await util.set_data('xkcdLatest', response['num'])


task = util.Task('xkcd', _run)