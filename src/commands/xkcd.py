import re
import json
import random
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
            term = ' '.join(args.searchterm)
            query = 'https://www.googleapis.com/customsearch/v1?q=%s&key=%s&cx=%s' % (urllib.parse.quote('xkcd ' + term), urllib.parse.quote(environment["googleKey"]), urllib.parse.quote(environment["googleCustom"]))
            response = json.loads(await api.web_call('get', query))
            if 'items' not in response:
                await api.send_message('**No results**', channel)
                return
            items = response['items']
            pattern = re.compile('^http(s)?:\/\/xkcd\.com')
            matched = [x['link'] for x in items if pattern.match(x['link'])]
            if len(matched) == 0:
                await api.send_message('**No matching comics**', channel)
                return
            else:
                url = pattern.sub('', matched[0])
        elif args.number:
            if args.number > 0:
              url = str(args.number)
            else:
              response = json.loads(await api.web_call('get', 'http://xkcd.com/info.0.json'))
              url = str(int(response['num']) + args.number)
              print(url)
        elif args.random:
            response = json.loads(await api.web_call('get', 'http://xkcd.com/info.0.json'))
            max = response['num']
            url = str(random.randrange(1, max))
        else:
            url = ''
        response = json.loads(await api.web_call('get', 'http://xkcd.com/' + url + '/info.0.json'))
        await api.send_message('', channel, {
            'title': response['title'] + ' #' + str(response['num']),
            'url': 'http://xkcd.com/' + url,
            'image': {
                'url': response['img']
            },
            'footer': {
                'text': response['alt']
            }
        })

command = util.Command('xkcd', 'XKCD!', util.levels.all, _run)
command.add_argument('searchterm', metavar='TERM', nargs='*', help='access comic by keyword', type=str)
group = command.add_mutually_exclusive_group()
group.add_argument('--add-channel', help='subscribe channel to automatic XKCD', action='store_true')
group.add_argument('--remove-channel', help='unsubscribe channel from automatic XKCD', action='store_true')
group.add_argument('-n', '--number', metavar='number', dest='number', help='access comic by number', type=int, required=False)
group.add_argument('-r', '--random', dest='random', help='display a random comic', action='store_true', required=False)
