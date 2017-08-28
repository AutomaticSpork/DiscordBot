import asyncio
import requests
import json

async def api_call(url, args):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, 'http://discordapp.com/api/' + url)
    return json.loads(response.text)

async def delete_message():
    pass

async def send_message(text, channel):
    print(text)