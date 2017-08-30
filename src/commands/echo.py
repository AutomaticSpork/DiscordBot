from .. import api
from ..util import levels

access = levels.all
args = [ 'text+' ]
text = 'Echoes a message'

async def run(args, user, channel, commands, environment):
    #print(' '.join(args['text']))
    await api.send_message(args['text'], channel, environment)