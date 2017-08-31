import asyncio
import importlib
import shlex
import json
import glob
from os import path
from . import util
from . import api

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
    command_dict = await import_dir('commands')
    commands = { v.command.prog: v.command for _, v in command_dict.items() }
    tasks = await import_dir('tasks')
    await api.on_init(environment['token'])

async def on_connect():
    await util.log('Connected!')

async def on_message(message):
    if message['content'].startswith(environment['commandStart']):
        commandstr = message['content'][len(environment['commandStart']):]
        for name, command in commands.items():
            if commandstr.startswith(name) and await check_access(command, message['user']):
                async def print_callback(m):
                    await api.send_message('```' + m + '```', message['channel'])
                parsedargs = shlex.split(commandstr[len(name) + 1:])
                command.on_print = print_callback
                try:
                    args = command.parse_args(parsedargs)
                except:
                    # Printing is handled by the callback
                    command.on_print = None
                    return
                await command.run(args, message['user'], message['channel'], commands, environment)
                command.on_print = None
                break