import asyncio
import checks
import discord
import sys
import traceback
from . import basecog
from discord.ext import commands

class Common(basecog.BaseCog):
    '''
    Common events and commands.
    '''

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def shutdown(self, ctx):
        await self.bot.say('Shutting down...')
        await self.bot.logout()

    async def on_ready(self):
        print('Logging in to {} guild(s)...'.format(len(self.bot.servers)))

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.send_help(ctx)
        else:
            if hasattr(ctx.command, "on_error"):
                return
            print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await self.bot.say('An error occured while trying to do that command.')

def setup(bot):
    bot.add_cog(Common(bot))