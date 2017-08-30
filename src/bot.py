import asyncio
import importlib
from os import path
import json
import glob
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

def arg_string(arg):
    return arg[:-1] if (arg.endswith('?') or arg.endswith('+')) else arg

async def on_init():
    global commands, tasks, environment
    with open('secret.json') as secret:
        environment = json.loads(secret.read())
    commands = await import_dir('commands')
    tasks = await import_dir('tasks')
    await api.on_init(environment['token'])

async def on_connect():
    await util.log('Connected!')

async def on_message(message):
    if message['content'].startswith(environment['commandStart']):
        commandstr = message['content'][len(environment['commandStart']):]
        for name, command in commands.items():
            if commandstr.startswith(name) and await check_access(command, message['user']):
                async def arg_print(m):
                    await api.send_message('```' + m + '```', message['channel'])
                commandstr = commandstr[len(name) + 1:].split(' ')
                command.args.on_print = arg_print
                try:
                    args = command.args.parse_args(commandstr)
                except:
                    # await api.send_message('**Invalid args for command ' + name + '**', message['channel'])
                    return
                await command.run(args, message['user'], message['channel'], commands, environment)
                break