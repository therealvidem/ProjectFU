from datetime import datetime
from discord.errors import HTTPException
import discord
import checks
import discord.embeds as embeds
from . import basecog
from discord.ext import commands

class Embed(basecog.BaseCog):
    '''
    Emote builder.
    '''

    def __init__(self, bot):
        super().__init__(bot)
        self.user_embeds = {}
        self.success_message = 'Successfully set the {} to {}'
    
    async def check_embed(self, ctx):
        member = ctx.message.author
        if member.id not in self.user_embeds:
            await self.bot.say('You must first initialize a new embed using "{}buildembed new"'.format(self.prefix))
            return False
        return True

    async def check_value(self, ctx, property, value, message=None):
        if not message:
            message = self.success_message
        embed = self.user_embeds[ctx.message.author.id]
        if not value and embed.get(property, None):
            del embed[property]
            await self.bot.say(message.format(property, 'nothing'))
            return False
        return True

    async def check_fields(self, ctx):
        embed = self.user_embeds[ctx.message.author.id]
        if 'fields' not in embed:
            embed['fields'] = []

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_admin()
    async def buildembed(self, ctx):
        await self.send_help(ctx)

    @buildembed.command(pass_context=True, name='display')
    async def buildembed_display(self, ctx):
        if not await self.check_embed(ctx):
            return
        member = ctx.message.author
        embed_data = self.user_embeds[member.id]
        embed = embeds.Embed.from_data(embed_data)
        try:
            await self.bot.say(embed=embed)
        except HTTPException:
            await self.bot.say(embed=embeds.Embed(title=''))
        except:
            await self.bot.say('Something went wrong while trying to send the embed.')

    @buildembed.command(pass_context=True, name='new')
    async def buildembed_new(self, ctx):
        member = ctx.message.author
        self.user_embeds[member.id] = {
            'title': 'New Embed'
        }
        await self.bot.say('Initialized a new embed. You may start configuring its properties using "{}buildembed modify"'.format(self.prefix))

    @buildembed.group(pass_context=True, name='modify', invoke_without_command=True)
    async def buildembed_modify(self, ctx):
        await self.send_help(ctx)

    @buildembed_modify.command(pass_context=True, name='title')
    async def buildembed_modify_title(self, ctx, *, value=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'title', value):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['title'] = value
        await self.bot.say(self.success_message.format('title', value))

    @buildembed_modify.command(pass_context=True, name='author')
    async def buildembed_modify_author(self, ctx, name=None, url=None, icon_url=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'author', name):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['author'] = {
            'name': name
        }
        if url:
            embed['author']['url'] = url
        if icon_url:
            embed['author']['icon_url'] = icon_url
        await self.bot.say(self.success_message.format('author', name))

    @buildembed_modify.command(pass_context=True, name='description')
    async def buildembed_modify_description(self, ctx, *, value=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'description', value):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['description'] = value
        await self.bot.say(self.success_message.format('description', value))

    @buildembed_modify.command(pass_context=True, name='url')
    async def buildembed_modify_url(self, ctx, value=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'url', value):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['url'] = value
        await self.bot.say(self.success_message.format('url', value))

    @buildembed_modify.command(pass_context=True, name='colour')
    async def buildembed_modify_colour(self, ctx, value: int=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'colour', value):
            return
        embed = self.user_embeds[ctx.message.author.id]
        if value:
            try:
                value = int(value, 16)
            except:
                await self.bot.say('Value must be a hexadecimal colour.')
                return
        embed['colour'] = value
        await self.bot.say(self.success_message.format('colour', value))

    @buildembed_modify.command(pass_context=True, name='timestamp')
    async def buildembed_modify_timestamp(self, ctx, year: int=None, month: int=None, day: int=None, hour: int=None, minute: int=None, second: int=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'timestamp', day, 'Successfully set the {} to {}.\nNote: You have to pass in the year, month, and day at the very least.'):
            return
        embed = self.user_embeds[ctx.message.author.id]
        kwargs = {}
        if hour:
            kwargs['hour'] = hour
        if minute:
            kwargs['minute'] = minute
        if second:
            kwargs['second'] = second
        try:
            dt = datetime(year, month, day, **kwargs)
        except ValueError:
            await self.bot.say('That date is not valid.')
            return
        embed['timestamp'] = dt.isoformat()
        await self.bot.say(self.success_message.format('timestamp', dt))

    @buildembed_modify.command(pass_context=True, name='footer')
    async def buildembed_modify_footer(self, ctx, text=None, icon_url=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'footer', text):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['footer'] = {
            'text': text    
        }
        if icon_url:
            embed['footer']['icon_url'] = icon_url
        await self.bot.say('Successfully set the footer')

    @buildembed_modify.command(pass_context=True, name='thumbnail')
    async def buildembed_modify_thumbnail(self, ctx, url=None):
        if not await self.check_embed(ctx) or not await self.check_value(ctx, 'thumbnail', url):
            return
        embed = self.user_embeds[ctx.message.author.id]
        embed['thumbnail'] = {
            'url': url    
        }
        await self.bot.say(self.success_message.format('thumbnail', url))

    @buildembed.command(pass_context=True, name='addfield')
    async def buildembed_addfield(self, ctx, name, *, value):
        if not await self.check_embed(ctx):
            return
        await self.check_field(ctx)
        embed = self.user_embeds[ctx.message.author.id]
        embed['fields'].insert(0, {
            'name': name,
            'value': value,
            'inline': True
        })
        await self.bot.say('Successfully added field')

    @buildembed.command(pass_context=True, name='addfieldnotinline')
    async def buildembed_addfieldnotinline(self, ctx, name, *, value):
        if not await self.check_embed(ctx):
            return
        await self.check_field(ctx)
        embed = self.user_embeds[ctx.message.author.id]
        embed['fields'].insert(0, {
            'name': name,
            'value': value,
            'inline': False
        })
        await self.bot.say('Successfully added non-inline field')

    @buildembed.command(pass_context=True, name='removefield')
    async def buildembed_removefield(self, ctx, index: int):
        if not await self.check_embed(ctx):
            return
        await self.check_field(ctx)
        embed = self.user_embeds[ctx.message.author.id]
        try:
            del embed['fields'][index]
        except IndexError:
            await self.bot.say('That index doesn\'t exist.')
            return
        await self.bot.say('Successfully removed field')

    @buildembed.command(pass_context=True, name='setfield')
    async def buildembed_setfield(self, ctx, index: int, name, value):
        if not await self.check_embed(ctx):
            return
        await self.check_field(ctx)
        embed = self.user_embeds[ctx.message.author.id]
        try:
            field = embed['fields']['index']
        except:
            await self.bot.say('That index doesn\'t exist.')
            return
        field['name'] = name
        field['value'] = value
        field['inline'] = True
        await self.bot.say('Successfully set field')

    @buildembed.command(pass_context=True, name='setfieldnotinline')
    async def buildembed_setfieldnotinline(self, ctx, index: int, name, value):
        if not await self.check_embed(ctx):
            return
        await self.check_field(ctx)
        embed = self.user_embeds[ctx.message.author.id]
        try:
            field = embed['fields']['index']
        except:
            await self.bot.say('That index doesn\'t exist.')
            return
        field['name'] = name
        field['value'] = value
        field['inline'] = False
        await self.bot.say('Successfully set non-inline field')

def setup(bot):
    bot.add_cog(Embed(bot))