import sys
import os
import asyncio
import discord
import data
from discord.ext.commands.bot import Bot
from discord.ext import commands

settings = data.load_json('settings.json')
if not os.path.exists('data'):
    os.mkdir('data')

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

def load_bot(token, prefix):
    bot = FUBot(prefix, settings['owner_id'], pm_help=True)
    '''
    # Hacky way of dynamically loading extensions (?)
    Note: The directory should be changed to fit the current directory.
    Meaning, if ProjectFU is not a folder, and run.bat is in the same folder
    as "commands", then remove ProjectFU.
    '''
    for ext in os.listdir('commands'):
        if ext.endswith('.py'):
            bot.load_extension('commands.{}'.format(ext[:-3]))
    bot.run(token)
    
if 'prefix' not in settings:
    settings['prefix'] = 's-'
    data.save_json('settings.json', settings)
    print('The default prefix is "s-", you can set this in settings.json.')
if 'token' not in settings:
    print('You need a token in order to run the bot!')
    token = input('Input a valid token:')
    settings['token'] = token
    owner_id = input('Input your Discord id:')
    settings['owner_id'] = owner_id
    data.save_json('settings.json', settings)
    load_bot(token, settings['prefix'])
else:
    load_bot(settings['token'], settings['prefix'])