import discord

class BaseCog:
    '''
    The base for all cogs; contains a bot property.
    '''
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.command_prefix

    async def send_help(self, ctx):
        command = ctx.invoked_subcommand or ctx.command
        pages = self.bot.formatter.format_help_for(ctx, command)
        for page in pages:
            await self.bot.send_message(ctx.message.channel, page)