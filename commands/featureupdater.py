import discord
import checks
import json
import data
import asyncio
import urllib.parse
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
        if 'channel' not in self.settings:
            self.settings['channel'] = ''
        self.num_text = {
            1: '1st',
            2: '2nd',
            3: '3rd'
        }

    async def set_prop(self, ctx, num: int, prop, content):
        if num and str(num) not in self.settings['features']:
            if num not in range(1, 4):
                await self.bot.say('The num of the feature must be 1, 2, or 3.')
                return
            self.settings['features'][str(num)] = {
                'userId': 0,
                'image1': 0,
                'image2': 0,
                'image3': 0,
                'blurb': ''
            }
        self.settings['features'][str(num)][prop] = content
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
            await self.bot.say('{} is not a valid channel id.'.format(id))
         self.settings['channel'] = str(id)
         await self.save_settings()
         await self.bot.say('Successfully set the channel id to {}.'.format(id))

    @fu.command(pass_context=True, name='new')
    @checks.is_admin()
    async def fu_new(self, ctx):
        self.settings['features'] = {}
        await self.save_settings()
        await self.bot.say('Successfully reset the featured list.')

    @fu.command(pass_context=True, name='display')
    @checks.is_admin()
    async def fu_display(self, ctx):
        await self.bot.say('```json\n{}```'.format(urllib.parse.unquote(json.dumps(self.settings['features'], separators=(', ', ': '), indent=2))))

    '''
    I *could* remove the repetition for these three commands (i.e. compact it into one command that takes the property,)
    but I think I'll keep it this way just to make it easier to use.
    '''

    @fu.command(pass_context=True, name='userId')
    @checks.is_admin()
    async def fu_userId(self, ctx, num: int, userId: int):
        await self.set_prop(ctx, num, 'userId', userId)

    # Note: This must some form of a ROBLOX asset id.
    @fu.command(pass_context=True, name='image1')
    @checks.is_admin()
    async def fu_image1(self, ctx, num: int, image: int):
        await self.set_prop(ctx, num, 'image1', image)

    @fu.command(pass_context=True, name='image2')
    @checks.is_admin()
    async def fu_image2(self, ctx, num: int, image: int):
        await self.set_prop(ctx, num, 'image2', image)

    @fu.command(pass_context=True, name='image3')
    @checks.is_admin()
    async def fu_image3(self, ctx, num: int, image: int):
        await self.set_prop(ctx, num, 'image3', image)

    @fu.command(pass_context=True, name='blurb')
    @checks.is_admin()
    async def fu_blurb(self, ctx, num: int, *, blurb):
        await self.set_prop(ctx, num, 'blurb', blurb)
        
    @fu.command(pass_context=True, name='confirm')
    @checks.is_admin()
    async def fu_confirm(self, ctx):
        #if len(self.settings['features']) < 3:
        #    await self.bot.say('There aren\'t enough features (3 needed.)')
        #    return
        channel = self.bot.get_channel(self.settings['channel'])
        if not channel:
            await self.bot.say('You have to set the channel using "{}fu setchannel <id>"'.format(self.prefix))
            return
        for i in range(1, len(self.settings['features']) + 1):
            await self.bot.send_message(channel, '```json\n{}```'.format(urllib.parse.unquote(json.dumps(self.settings['features'][str(i)], separators=(', ', ': '), indent=2))))
            await asyncio.sleep(0.2)

def setup(bot):
    bot.add_cog(FeatureUpdater(bot, 'featureupdater'))