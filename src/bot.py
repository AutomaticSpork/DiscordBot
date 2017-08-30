import asyncio
import importlib
from os import path
import json
import glob
from . import util

commands = []
tasks = []

async def set_environment(key, value):
    global environment
    environment[key] = value

async def import_dir(dir):
    files = glob.glob('%s/%s/*.py' % (path.dirname(__file__), dir))
    items = [path.basename(f)[:-3] for f in files if path.isfile(f) and not f.endswith('__init__.py')]
    return { x: importlib.import_module('.' + dir + '.' + x, __name__[:__name__.rfind('.')]) for x in items }

async def task_loop():
    pass

async def check_access(command, user):
    return True

async def on_init():
    global commands, tasks, environment
    with open('secret.json') as secret:
        environment = json.loads(secret.read())
    commands = await import_dir('commands')
    tasks = await import_dir('tasks')

async def on_connect():
    await util.log('Connected!')

async def on_message(message):
    if message['content'].startswith(environment['commandStart']):
        commandstr = message['content'][len(environment['commandStart']):]
        for name, command in commands.items():
            if commandstr.startswith(name) and await check_access(command, message['user']):
                parsedargs = commandstr[len(name) + 1:].split(' ')
                if len(parsedargs) < len(command.args):
                    await send_message('Invalid args for command %s, expected: %s' % (name, command.args), message['channel'], environment)
                    return
                args = { (x[:-1] if (x.endswith('?') or x.endswith('+')) else x): parsedargs[i] for i, x in enumerate(command.args) }
                await command.run(args, message['user'], message['channel'], commands, environment)
                break