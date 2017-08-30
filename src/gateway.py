import asyncio
import websockets
import json
from . import bot
from . import api

seq = 0 # TODO: Threads may break?

async def websocket_receive_loop(websocket):
    global seq
    while True:
        data = json.loads(await websocket.recv())
        if data['op'] == 0 and data['t'] == 'MESSAGE_CREATE':
            loop = asyncio.get_event_loop()
            loop.create_task(bot.on_message({
                'user': data['d']['author']['id'],
                'channel': data['d']['channel_id'],
                'content': data['d']['content'],
                'embeds': data['d']['embeds'],
                'timestamp': data['d']['timestamp']
            }))
        if data['op'] == 1 and data['t'] == 'READY':
            bot.set_environment('botId', data['d']['user']['id'])
        if data['s']:
            seq = data['s']

async def websocket_send_loop(websocket, timeout):
    global seq
    while True:
        await websocket_send(websocket, 1, seq)
        await asyncio.sleep(timeout / 1000)

async def websocket_send(websocket, op, payload):
    await websocket.send(json.dumps({
        'op': op,
        'd': payload
    }))

async def run():
    await bot.on_init()
    gateway = await api.api_call('get', 'gateway')
    async with websockets.connect(gateway['url'] + '/?v=6&encoding=json') as websocket:
        hello = json.loads(await websocket.recv())
        assert hello['op'] == 10
        await websocket_send(websocket, 2, {
            'token': bot.environment['token'],
            'properties': {
                '$os': 'Linux',
                '$browser': 'DiscordBot',
                '$device': 'DiscordBot'
            },
            'compress': False,
            'large_threshold': 250,
            'presence': {
                'game': {
                    'name': 'Bitcoin Mining',
                    'type': 0
                }
            }
        })
        await bot.on_connect()
        done, pending = await asyncio.wait([asyncio.ensure_future(websocket_receive_loop(websocket)), asyncio.ensure_future(websocket_send_loop(websocket, hello['d']['heartbeat_interval']))], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
