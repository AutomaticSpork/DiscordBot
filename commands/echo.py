access = 'all'
args = [ 'text+' ]
text = 'Echoes a message'

async def run(args, user, commands, environment):
    #print(' '.join(args['text']))
    print(args['text'])