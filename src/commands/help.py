from .. import api
from ..util import levels

access = levels.all
args = [ 'command?' ]
text = 'Displays help'

async def run(args, user, channel, commands, environment):
    used = commands
    if args['command']:
        used = { k: v for k, v in commands.items() if args['command'] in k } 
    await api.send_message('```%s```' % ('\n\n'.join(['**%s%s** %s\n%s' % (environment['commandStart'], k, ' '.join(v.args), v.text) for k, v in used.items()])), channel, environment)