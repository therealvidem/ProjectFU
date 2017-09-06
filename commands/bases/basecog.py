import discord

class BaseCog:
    '''
    The base for all cogs; contains a bot property.
    '''
    def __init__(self, bot, cogname):
        self.bot = bot
        self.cogname = cogname if cogname else self.__class__.__name__
        self.prefix = bot.command_prefix

    async def send_help(self, ctx):
        command = ctx.invoked_subcommand or ctx.command
        pages = self.bot.formatter.format_help_for(ctx, command)
        for page in pages:
            await self.bot.send_message(ctx.message.channel, page)