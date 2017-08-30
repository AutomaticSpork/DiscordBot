import asyncio
import aiohttp
import json

token = ''

async def on_init(t):
    global token
    token = t

async def web_call(method, url, args=None, headers=None):
    if args == None:
        args = ''
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, data=args, headers=headers) as response:
            return await response.text()

async def api_call(method, url, args=None):
    headers = {
        'Authorization': 'Bot ' + token,
        'Content-Type': 'application/json'
    }
    return json.loads(await web_call(method, 'https://discordapp.com/api/' + url, json.dumps(args), headers))

async def delete_message(id, channel):
    pass

async def send_message(content, channel, embed=None):
    return await api_call('post', 'channels/' + channel + '/messages', {
        'content': content,
        'embed': embed
    })