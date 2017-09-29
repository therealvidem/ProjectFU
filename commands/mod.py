import checks
import discord
import asyncio
from .bases import DataCog
from discord.ext import commands
from discord.utils import get
from discord.utils import find

class Mod(DataCog):
    '''
    Server moderation commands.
    '''

    async def get_members_from_args(self, ctx, *args):
        members = []
        for member in args:
            try:
                members.append(commands.MemberConverter(ctx, member).convert())
            except commands.BadArgument:
                await self.bot.say('User "{}" cannot be found.'.format(member))
                return
        return members

    async def check_server(self, ctx):
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
        if 'muted' not in self.settings[server.id]:
            self.settings[server.id]['muted'] = {}
        if 'muted_role_id' not in self.settings[server.id]:
            self.settings[server.id]['muted_role_id'] = None

    @commands.command(pass_context=True)
    @checks.is_mod()
    async def kick(self, ctx, user: discord.Member):
        '''
        Kicks a user
        '''
        try:
            del self.settings[ctx.message.server.id]['muted'][user.id]
            await self.save_settings()
        except KeyError:
            pass
        await self.bot.kick(user)
        await self.bot.say('Kicked {}'.format(user))

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def ban(self, ctx, user: discord.Member, delete_message_days: int=0):
        '''
        Bans a user; by default, no messages are deleted. However, a maximum of 7
        days can be applied to the number of days worth of messages that should be
        removed.
        '''
        try:
            del self.settings[ctx.message.server.id]['muted'][user.id]
            await self.save_settings()
        except KeyError:
            pass
        await self.bot.ban(user, delete_message_days)
        await self.bot.say('Banned {}'.format(user))

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def unban(self, ctx, query):
        '''
        Finds a user to unban from the banned list using the given query (name).
        '''
        query = query.lower()
        banned_users = await self.bot.get_bans(ctx.message.server)
        for user in banned_users:
            if str(user).lower() == query or user.name.lower() == query or user.id.lower() == query:
                await self.bot.unban(user)
                await self.bot.say('Unbanned {}'.format(user))
                return

    @commands.command(pass_context=True)
    @checks.is_admin()
    async def prune(self, ctx, amount: int):
        '''
        Deletes a specific amount of messages before this message.
        '''
        message = ctx.message
        channel = message.channel
        await self.bot.purge_from(channel, limit=amount, before=message)
        await self.bot.delete_message(message)

    @commands.command(pass_context=True)
    @checks.is_mod()
    async def mute(self, ctx, *users):
        '''
        Adds the "Muted" role to the specified user(s), and removes and stores the current roles of the user.
        '''
        await self.check_server(ctx)
        server_settings = self.settings[ctx.message.server.id]
        muted = server_settings['muted']
        if len(users) < 1:
            await self.send_help(ctx)
            return
        muted_role = find(lambda r: r.id == server_settings['muted_role_id'], ctx.message.server.roles)
        if muted_role is None:
            await self.bot.say('Couldn\'t find the muted role. Set a valid muted role using {}setmutedrole [role name]'.format(self.prefix))
            return
        members = await self.get_members_from_args(ctx, *users)
        if members is None:
            return
        for member in members:
            if muted_role in member.roles:
                await self.bot.say('{} is already muted.'.format(member))
                continue
            muted[member.id] = {
                'removed_roles_ids': [],
                'timestamp': str(ctx.message.timestamp)
            }
            roles = []
            for role in member.roles[1:]:
                muted[member.id]['removed_roles_ids'].append(role.id)
                roles.append(role)
            await self.bot.replace_roles(member, muted_role)
        await self.save_settings()
        await self.bot.say('Muted the specified user(s)')

    @commands.command(pass_context=True)
    @checks.is_mod()
    async def unmute(self, ctx, *users):
        '''
        Removes the "Muted" role from the specified user(s), and adds back the removed roles (if the roles still exist.)
        '''
        await self.check_server(ctx)
        server_settings = self.settings[ctx.message.server.id]
        muted = server_settings['muted']
        if len(users) < 1:
            await self.send_help(ctx)
            return
        muted_role = find(lambda r: r.id == server_settings['muted_role_id'], ctx.message.server.roles)
        if muted_role is None:
            await self.bot.say('Couldn\'t find the muted role. Set a valid muted role using {}setmutedrole [role name]'.format(self.prefix))
            return
        members = await self.get_members_from_args(ctx, *users)
        if members is None:
            return
        for member in members:
            if muted_role not in member.roles or member.id not in muted:
                await self.bot.say('{} is already unmuted.'.format(member))
                continue
            roles = []
            for role_id in muted[member.id]['removed_roles_ids']:
                role = get(ctx.message.server.roles, id=role_id)
                if not role:
                    await self.bot.say('The role "{}" no longer exists.'.format(role.name))
                    continue
                roles.append(role)
            del muted[member.id]
            await self.bot.replace_roles(member, *roles)
        await self.save_settings()
        await self.bot.say('Unmuted the specified user(s)')
        
    @commands.command(pass_context=True)
    @checks.is_admin()
    async def setmutedrole(self, ctx, role):
        '''
        Sets the muted role.
        '''
        await self.check_server(ctx)
        muted_role = get(ctx.message.server.roles, name=role)
        if muted_role is None:
            await self.bot.say('Couldn\'t find the specified role')
            return
        self.settings[ctx.message.server.id]['muted_role_id'] = muted_role.id
        await self.save_settings()
        await self.bot.say('Successfully set the muted role to "{}"'.format(role))

def setup(bot):
    bot.add_cog(Mod(bot, 'mod'))