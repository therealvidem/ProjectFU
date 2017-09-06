import discord
import checks
import json
import data
import asyncio
import discord.embeds as embeds
from .bases import DataCog
from discord.ext import commands

class FeatureUpdater(DataCog):
    '''
    Updates the featured builders for Sandbox.
    '''

    def __init__(self, bot, cogname):
        super().__init__(bot, cogname)
        if 'features' not in self.settings:
            self.settings['features'] = {}
        self.features = self.settings['features']
        self.channel = None
        self.num_text = {
            1: '1st',
            2: '2nd',
            3: '3rd'
        }

    async def set_prop(self, ctx, num: int, prop, content):
        if num and num not in self.features:
            if num not in range(1, 4):
                await self.bot.say('The num of the feature must be 1, 2, or 3.')
                return
            self.features[num] = {
                'userId': 0,
                'image': '',
                'blurb': ''
            }
        self.features[num][prop] = content
        await self.save_settings()
        await self.bot.say('Successfully set the {} of the {} featured builder.'.format(prop, self.num_text[num]))

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_admin()
    async def fu(self, ctx):
        await self.send_help(ctx)

    @fu.command(pass_context=True, name='setchannel')
    @checks.is_admin()
    async def fu_setchannel(self, ctx, id: int):
        if not self.bot.get_channel(str(id)):
            await self.bot.say('That\'s not a valid channel id.')
        self.channel = self.bot.get_channel(str(id))
        await self.bot.say('Successfully set the channel id to {}.'.format(id))

    @fu.command(pass_context=True, name='new')
    @checks.is_admin()
    async def fu_new(self, ctx):
        self.features = {}
        await self.save_settings()
        await self.bot.say('Successfully reset the featured list.')

    @fu.command(pass_context=True, name='display')
    @checks.is_admin()
    async def fu_display(self, ctx):
        await self.bot.say(json.dumps(self.features, separators=(',', ':')))

    '''
    I *could* remove the repetition for these three commands (i.e. compact it into one command that takes the property,)
    but I think I'll keep it this way just to make it easier to use.
    '''

    @fu.command(pass_context=True, name='userId')
    @checks.is_admin()
    async def fu_userId(self, ctx, num: int, userId: int):
        await self.set_prop(ctx, num, 'userId', userId)

    # Note: This must some form of a ROBLOX asset id.
    @fu.command(pass_context=True, name='image')
    @checks.is_admin()
    async def fu_image(self, ctx, num: int, image):
        await self.set_prop(ctx, num, 'image', image)

    @fu.command(pass_context=True, name='blurb')
    @checks.is_admin()
    async def fu_blurb(self, ctx, num: int, blurb):
        await self.set_prop(ctx, num, 'blurb', blurb)
        
    @fu.command(pass_context=True, name='confirm')
    @checks.is_admin()
    async def fu_confirm(self, ctx):
        if len(self.features) < 3:
            await self.bot.say('There aren\'t enough features (3 needed.)')
            return
        if not self.channel:
            await self.bot.say('You have to set the channel using "{}fu setchannel <id>"'.format(self.prefix))
            return
        for i in range(len(self.features), 0):
            await self.bot.send_message(self.channel, json.dumps(self.features[i], separators=(',', ':')))
            await asyncio.sleep(0.2)

def setup(bot):
    bot.add_cog(FeatureUpdater(bot, 'featureupdater'))

