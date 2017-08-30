import json
import argparse
from .. import api
from .. import util

access = util.levels.all
args = util.BotArgs(description='XKCD!', prog='xkcd')
args.add_argument('searchterm', type=str)

async def run(args, user, channel, commands, environment):
    url = ''
    if args.searchterm:
        num = False
        try:
            int(args.searchterm)
            num = True
        except: pass
        if num:
            url = args.searchterm
        else:
            await api.send_message('Not implemented yet :(', channel)
            return
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