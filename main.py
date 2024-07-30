import discord
from discord.ext import commands
import asyncio
import config

from discord.ext.commands import MissingPermissions, guild_only

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)
bad_words = []

@bot.command()
async def get_id(ctx, member: discord.Member):
    print(int(member.id))

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready to work')

@bot.event
async def on_member_join(member):
    await member.send('Привет, ты можешь получить всю необходимую информацию по команде !info')
    role = discord.utils.get(member.guild.roles, id=1267123714240020511)
    embed = discord.Embed(
        title="Добро пожаловать на сервер!",
        description=f"{member.name}#{member.discriminator}\n"
                    f"Вы получаете роль - Новичок",
        color=0xffffff
    )
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'общее':
            await bot.get_channel(ch.id).send(embed=embed)
    await member.add_roles(role)
@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'общее':
            await bot.get_channel(ch.id).send(f'Нам будет не хватать тебя, {member.mention}')
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    for content in message.content.split():
        if content.lower() in bad_words:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, следи за базаром.')

@bot.command()
async def info(ctx):
    info = discord.Embed(
        title='info',
        description=f'!prof - профиль\n'
                    f'!stats - статистика'
    )
    await ctx.send(embed=info)
@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Нарушение правил"):
    await ctx.send(f"Admin {ctx.author.mention} исключил пользователя {member.mention}", delete_after=2)
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason = "Многократное нарушение правил"):
    await ctx.send(f"Admin {ctx.author.mention} забанил пользователя {member.mention}", delete_after=2)
    await member.ban(reason=reason)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, H=0, M=0, S =5, *, reason="Нарушение правил"):
    roles = member.roles
    role = discord.utils.get(ctx.guild.roles, id=1267405498706169867)
    for role_mem in roles[1:]:
        await member.remove_roles(role_mem)
    await member.add_roles(role, reason=reason)
    message: discord.Message = await ctx.send(f'User {member.mention} has been muted.')
    time = H*3600 + M*60 + S
    await asyncio.sleep(time)
    await member.remove_roles(role)
    for role_mem in roles[1:]:
        await member.add_roles(role_mem)
    await ctx.send(f'user {member.mention} has been unmuted.')

'''@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int, *, reason="Отстуствует"):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user, reason=reason)'''

@bot.command()
async def get_roles(ctx, member: discord.Member):
    roles = member.roles
    for role in roles[1:]:
        await ctx.send(role.id)

@bot.command()
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))

'''@bot.command()
async def get_bans(ctx):
    banned_users = ctx.guild.bans()
    async for user in banned_users:
        print(user)'''
@bot.command()
async def unban (ctx, name, reason='reason'):
    banned_users = ctx.guild.bans()
    async for user in banned_users:
        if user.user.global_name == name:
            await ctx.guild.unban(user.user)
if __name__ == '__main__':
    bot.run(token=config.BOT_TOKEN)