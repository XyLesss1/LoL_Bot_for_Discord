import discord
from discord.ext import commands
import asyncio

from discord.ext.commands import MissingPermissions

import Champion
import config
import LoL
import db
import sqlite3
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

    role = discord.utils.get(member.guild.roles, id=1267123714240020511)
    embed = discord.Embed(
        title="Welcome!",
        description=f"{member.name}#{member.discriminator}\n"
                    f"You get the role of summoner",
        color=0xffffff
    )
    await member.send(embed=embed)
    await member.add_roles(role)
    await db.create_table(db.name_bd)
    await db.create_line_users(member.id)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    for content in message.content.split():
        if content.lower() in bad_words:
            await message.delete()
            await message.channel.send(f'{message.author.mention},')
@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Нарушение правил"):
    await ctx.send(f"Admin {ctx.author.mention} has excluded the user {member.mention}", delete_after=2)
    await member.kick(reason=reason)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))

@bot.command()
async def stats(ctx, name, tag, region):
    puuid = await LoL.get_puuid(name, tag)
    id = await LoL.get_sum_id(region, puuid)
    stats = await LoL.get_stats(id, puuid, region)
    embed = discord.Embed(
        title='Player statistics',
        color=discord.Colour.dark_blue(),
    )
    top_champs = await LoL.get_top_champions(region, puuid, top=3)
    embed.add_field(name='level', value=stats['level'])
    embed.add_field(name='rank', value=stats['rank'])
    embed.add_field(name='winrate', value=stats['winrate'])
    embed.add_field(name='Top Champions', value=f'{top_champs[0]}\n{top_champs[1]}\n{top_champs[2]}')
    embed.set_image(url=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{top_champs[0]}_1.jpg')
    # embed.set_image(url='https://static.wikia.nocookie.net/leagueoflegends/images/6/66/Xayah_OriginalCentered.jpg
    # /revision/latest?cb=20180414203728')
    icon_id = await LoL.get_icon_id(region, puuid)
    embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/14.15.1/img/profileicon/{icon_id}.png')
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def create_acc(ctx, member: discord.Member, name, tag, region):
    user_id = member.id
    global_name = member.global_name
    name = name
    tag = tag
    puuid = await LoL.get_puuid(name, tag)
    try:
        await db.create_table_members(db.name_bd)
        print('Table created')
        await db.create_line(user_id, global_name, name, tag, puuid, region)
        print('Запись добавлена в таблицу members')
    except sqlite3.IntegrityError:
        await ctx.send('An account with this id already exists')




@bot.command()
async def prof(ctx):
    user_id = ctx.author.id
    puuid = await db.get_puuid(user_id)
    region = await db.get_region(user_id)
    if region == 'EUW': region = 'EUW1'
    id = await LoL.get_sum_id(region, puuid)
    stats = await LoL.get_stats(id, puuid, region)
    top_champs = await LoL.get_top_champions(region, puuid, top=3)
    embed = discord.Embed(
        title='Stats',
        colour=discord.Colour.dark_blue()
    )
    embed.add_field(name='level', value=stats['level'])
    embed.add_field(name='rank', value=stats['rank'])
    embed.add_field(name='winrate', value=stats['winrate'])
    embed.add_field(name='Top Champions', value=f'{top_champs[0]}\n{top_champs[1]}\n{top_champs[2]}')
    embed.set_image(url=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{top_champs[0]}_1.jpg')
    icon_id = await LoL.get_icon_id(region, puuid)
    embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/14.15.1/img/profileicon/{icon_id}.png')

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member):
    await db.add_warn(member.id)
    warns = await db.get_warns(member.id)
    await ctx.send(f'The user {member.mention} was issued a warning. Current number of warnings:
{warns}')
    if warns >= 4:
        await member.ban()
        await ctx.send(f'Member {member.mention} was banned')


if __name__ == '__main__':
    bot.run(token=config.BOT_TOKEN)
