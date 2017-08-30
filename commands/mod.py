import checks
import discord
from . import basecog
from discord.ext import commands

class Mod(basecog.BaseCog):
    '''
    Server moderation commands.
    '''

    @commands.command(pass_context=True)
    @checks.is_mod()
    async def kick(self, ctx, user: discord.Member):
        await self.bot.kick(user)

def setup(bot):
    bot.add_cog(Mod(bot))