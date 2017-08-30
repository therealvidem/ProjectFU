import sys
import os
import asyncio
import discord
import checks
from discord.ext.commands.bot import Bot
from discord.ext import commands
from discord.utils import get

global_prefix = 's-'

class FUBot(Bot):
    '''
    A class that extends Bot for the sole
    purpose of adding other methods and properties, such as
    owner_id.

    **other is simply just the optional arguments of the Bot class
    (e.g. pm_help=False).
    '''
    def __init__(self, prefix, owner_id, **other):
        super().__init__(prefix, **other)
        self.owner_id = owner_id

'''
sys.argv is just a way to get the token from the
execution of this python file. A cmd line to run this
bot would look something like this:

python bot.py [token]
'''

# Making sure we're in the file's relative directory.
os.chdir(sys.path[0])

try:
    bot = FUBot(global_prefix, checks.owner_id, pm_help=True)
    # Hacky way of dynamically loading extensions (?)
    for ext in os.listdir('commands'):
        if ext != 'basecog.py' and ext.endswith('.py'):
            bot.load_extension('commands.{}'.format(ext[:-3]))
    bot.run(sys.argv[1])
except IndexError:
    print('Couldn\'t find token; do "python bot.py [token]"')