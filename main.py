#!/usr/bin/env python3
import asyncio
import aiohttp
import websockets
import json
import requests

async def api_call(url, args):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, 'http://discordapp.com/api/' + url)
    return json.loads(response.text)

async def handle_gateway(url):
    global environment
    seq = 0 # TODO: Threads may break?
    async def websocket_send(websocket, op, payload):
        await websocket.send(json.dumps({
            'op': op,
            'd': payload
        }))
    async def receive(websocket):
        while True:
            print(await websocket.recv())
    async def send(websocket, timeout):
        while True:
            await websocket_send(websocket, 1, seq)
            await asyncio.sleep(timeout / 1000)
    async with websockets.connect(url) as websocket:
        await websocket_send(websocket, 2, {
            'token': environment['token'],
            'properties': {
                '$os': 'Linux',
                '$browser': 'DiscordBot',
                '$device': 'DiscordBot'
            },
            'compress': False,
            'large_threshold': 250,
            'shard': [1, 10],
            'presence': {
                'game': {
                    'name': 'Bitcoin Mining',
                    'type': 0
                },
                'status': 'online'
            }
        })
        hello = json.loads(await websocket.recv())['d']
        environment['botId'] = hello['user']['id']
        done, pending = await asyncio.wait([asyncio.ensure_future(receive(websocket)), asyncio.ensure_future(send(websocket, hello['heartbeat_interval']))], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

async def main():
    gateway = await api_call('gateway', None)
    await handle_gateway(gateway['url'])

with open('secret.json') as secret:
    environment = json.loads(secret.read())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()