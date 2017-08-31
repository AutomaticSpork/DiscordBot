import re
import json
import argparse
import urllib.parse
from .. import api
from .. import util

async def _run(args, user, channel, commands, environment):
    url = ''
    if args.add_channel:
        channels = await util.get_data('xkcdChannels')
        if channel in channels:
            await api.send_message('Already subscribed!', channel)
        else:
            channels.append(channel)
            await util.set_data('xkcdChannels', channels)
            await api.send_message('Subscribing channel!', channel)
    elif args.remove_channel:
        channels = await util.get_data('xkcdChannels')
        if channel in channels:
            channels.remove(channel)
            await util.set_data('xkcdChannels', channels)
            await api.send_message('Unsubscribing channel!', channel)
        else:
            await api.send_message('Not subscribed', channel)
    else:
        if args.searchterm:
            query = 'https://www.googleapis.com/customsearch/v1?q=%s&key=%s&cx=%s' % (urllib.parse.quote('xkcd ' + args.searchterm), urllib.parse.quote(environment["googleKey"]), urllib.parse.quote(environment["googleCustom"]))
            items = json.loads(await api.web_call('get', query))['items']
            pattern = re.compile('^http(s)?:\/\/xkcd\.com')
            matched = [x['link'] for x in items if pattern.match(x['link'])]
            if len(matched) == 0:
                await api.send_message('**No matching comics**')
                return
            else:
                url = pattern.sub('', matched[0])
        elif args.number:
            url = str(args.number)
        else:
            url = ''
        response = json.loads(await api.web_call('get', 'http://xkcd.com/' + url + '/info.0.json'))
        await api.send_message('', channel, {
            'title': response['title'] + ' #' + str(response['num']),
            'image': {
                'url': response['img']
            },
            'footer': {
                'text': response['alt']
            }
        })

command = util.Command('xkcd', 'XKCD!', util.levels.all, _run)
group = command.add_mutually_exclusive_group()
group.add_argument('--add-channel', action='store_true')
group.add_argument('--remove-channel', action='store_true')
group.add_argument('-s', metavar='searchterm', dest='searchterm', type=str, required=False)
group.add_argument('-n', metavar='number', dest='number', type=int, required=False)