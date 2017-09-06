import checks
import discord
from .bases import BaseCog
from discord.ext import commands

class Mod(BaseCog):
    '''
    Server moderation commands.
    '''

    @commands.command(pass_context=True)
    @checks.is_mod()
    async def kick(self, ctx, user: discord.Member):
        await self.bot.kick(user)

def setup(bot):
    bot.add_cog(Mod(bot, 'mod'))