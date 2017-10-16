import asyncio
import aioconsole
import checks
import discord
import sys
import traceback
import math
from .bases import BaseCog
from discord.ext import commands

class Common(BaseCog):
    '''
    Common events and commands.
    '''

    async def on_ready(self):
        print('Logging in to {} guild(s)...'.format(len(self.bot.servers)))

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await self.send_help(ctx)
        elif isinstance(error, commands.CheckFailure):
            await self.bot.send_message(ctx.message.channel, 'You\'re not allowed to use that command.')
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = math.floor(error.retry_after)
            article = 'second' if seconds == 1 else 'seconds'
            await self.bot.send_message(ctx.message.channel, 'You must wait {} {}.'.format(seconds, article))
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            if hasattr(ctx.command, "on_error"):
                return
            print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await self.bot.send_message(ctx.message.channel, 'An error occured while trying to do that command.')

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def shutdown(self, ctx):
        await self.bot.say('Shutting down...')
        await self.bot.logout()

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_admin()
    async def setbot(self, ctx):
        await self.send_help(ctx)

    @setbot.command(pass_context=True, name='name')
    @checks.is_admin()
    async def bot_name(self, ctx, *, name):
        await self.bot.edit_profile(username=name)
        await self.bot.say('Successfully set name.')

def setup(bot):
    bot.add_cog(Common(bot, 'common'))