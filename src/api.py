import asyncio
import aiohttp
import json

token = ''

async def on_init(t):
    global token
    token = t

async def api_call(method, url, args=None):
    loop = asyncio.get_event_loop()
    headers = {
        'Authorization': 'Bot ' + token,
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.request(method, 'https://discordapp.com/api/' + url, data=json.dumps(args), headers=headers) as response:
            return json.loads(await response.text())

async def delete_message(id, channel):
    pass

async def send_message(content, channel):
    return await api_call('post', 'channels/' + channel + '/messages', {
        'content': content
    })