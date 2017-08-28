access = 'all'
args = [ 'command?' ]
text = 'Displays help'

async def run(args, user, commands, environment):
    used = commands
    if args['command']:
        used = { k: v for k, v in commands.items() if k.contains(args['command']) } 
    print(['%s%s %s\n%s' % (environment['commandStart'], k, ' '.join(v.args), v.text) for k, v in used.items()])