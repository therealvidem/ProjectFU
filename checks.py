from discord.ext import commands
from discord.utils import get

owner_id = '138838298742226944'

'''
These are several functions that are only here just so
is_admin can also check is_owner, and so is_mod can also
use is_admin.
'''

def __is_owner(ctx):
    return ctx.message.author.id == owner_id

def __is_admin(ctx):
    author = ctx.message.author
    return get(author.roles, name='Discord Tsar') or get(author.roles, name='Senior Staff') or __is_owner(ctx)

def __is_mod(ctx):
    author = ctx.message.author
    return get(author.roles, name='SB Community Moderator') or __is_admin(ctx)

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