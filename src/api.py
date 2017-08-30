import asyncio
import requests
import json

async def api_call(url, method, args, environment):
    loop = asyncio.get_event_loop()
    headers = None
    if environment:
        headers = {'Authorization': 'Bot ' + environment['token']}
    response = await loop.run_in_executor(None, lambda: requests.request(method, 'http://discordapp.com/api/' + url, data=args, headers=headers))
    return json.loads(response.text)

async def delete_message(id, channel, environment):
    pass

async def send_message(content, channel, environment):
    loop = asyncio.get_event_loop()
    print(await api_call('users/@me/channels', 'post', {'recipient_id': 141673287578157056}, environment))
    return await api_call('channels/' + channel + '/messages', 'post', {
        'content': 'This is a test'
    }, environment)