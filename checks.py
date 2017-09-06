import data
import discord
from discord.ext import commands
from discord.utils import get

settings = data.load_json('settings.json')

'''
These are several functions that are only here just so
is_admin can also check is_owner, and so is_mod can also
use is_admin.
'''

def __is_owner(ctx):
    return ctx.message.author.id == settings['owner_id']

def __is_admin(ctx):
    author = ctx.message.author
    if isinstance(author, discord.Member):
        return get(author.roles, name='Discord Tsar') or get(author.roles, name='Senior Staff') or __is_owner(ctx)
    else:
        return __is_owner(ctx)

def __is_mod(ctx):
    author = ctx.message.author
    if isinstance(author, discord.Member):
        return get(author.roles, name='SB Community Moderator') or __is_admin(ctx)
    else:
        return __is_owner(ctx)

'''
Below are several decorators that can be accessed anywhere so as long
as checks is imported
'''

def is_owner():
    return commands.check(__is_owner)

def is_admin():
    return commands.check(__is_admin)

def is_mod():
    return commands.check(__is_mod)