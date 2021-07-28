import discord
import os
import json
import datetime, time
from discord.client import Client
import requests
import random
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.ext.commands import Bot
import asyncio
from asyncio import sleep
import math
import aiosqlite
import bs4
from bs4 import BeautifulSoup as bs4
import io
import aiohttp
from discord.ext import tasks
from itertools import cycle
from datetime import datetime
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions



client = commands.Bot(command_prefix = '^')
client.remove_command('help')

client.launch_time = datetime.utcnow()


client.sniped_messages = {}


status = cycle(['Watching 20 servers','^help','^invite'])


@client.event
async def on_ready():
  change_status.start()
  print('{0.user}'.format(client))
  print('Is Online')



client.load_extension('cogs.moderation')



@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(status))))




@client.command()
async def ping(ctx):
    embed=discord.Embed(title= "Bot Ping", color=0x065be5)
    embed.add_field(name="Ping", value= f' {round(client.latency * 1000)}ms' , inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)
   





@client.command()
async def uptime(ctx):
    embed=discord.Embed(title="Uptime", color=0x065be5)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed.add_field(name="Kronos has been online for", value=f"{days}d, {hours}h, {minutes}m, {seconds}s", inline=False)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Kronos Help", color=0x065be5)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.add_field(name="Command List", value="List of command functions", inline=False)
    embed.add_field(name="•uptime", value="How long the bot has been up", inline=True)
    embed.add_field(name="•8ball :8ball: ", value="Ask the magic 8ball a question", inline=True)
    embed.add_field(name="•ping", value="Bot Latency Ping", inline=True)
    embed.add_field(name="•invite", value="Invite me to your server!", inline=True)
    embed.add_field(name="•ban", value="Ban a member", inline=True)
    embed.add_field(name="•kick", value="Kick a member", inline=True)
    embed.add_field(name="•clear/purge/delete", value="Delete messages", inline=True)
    embed.add_field(name="•unban", value="Unban a member", inline=True)
    embed.add_field(name="•userinfo/whois", value="Info about a member", inline=True)
    embed.add_field(name="•avatar/av/pfp", value="Sends a members pfp", inline=True)
    embed.add_field(name="•snipe", value="Snipe the last deleted message", inline=True)
    embed.add_field(name="•roleinfo", value="gives information on the role you type", inline=True)
    embed.add_field(name="•slots", value="plays slots", inline=True)
    embed.add_field(name="•dong", value="see your dong size", inline=True)
    embed.add_field(name="•joke", value="tells a joke", inline=True)
    embed.add_field(name="•servericon", value="Server Icon", inline=True)
    embed.add_field(name="•btc/bitcoin", value="check the current Bitcoin price", inline=True)
    embed.add_field(name="•etc/ethereum", value="check the current Ethereum price", inline=True)
    embed.add_field(name="•wyr/wouldyourather", value="asks you a would you rather question", inline=True)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)
    





@client.command(aliases=['8ball', '8Ball', 'eightball', 'Eightball'])
async def _8ball(ctx, *, question):
    embed=discord.Embed(title="8Ball :8ball: ", color=0x065be5)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=client.user.avatar_url)
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    embed.add_field(name=f'Question: {question}', value = f'Answer: {random.choice(responses)}', inline=False)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)



@has_permissions(manage_messages=True)
@client.command(aliases=['purge','delete'])
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages were deleted')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Sorry you do not have permissions to delete messages!")
        
        



@client.command()
async def invite(ctx):
    embed=discord.Embed(title="Invite", color=0x065be5)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.add_field(name="Thank you for inviting!", value="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=862180355473932288&permissions=134604807&scope=bot)", inline=False)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)

   
    

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member=None, reason=None):
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title="ERROR:", description="You can not ban yourself.", color=0xff0000)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
        embed.set_footer(text="made by z!#5199")
        await ctx.send(embed=embed)
        return
    if reason == None: 
        reason = 'None given'
    await member.ban(reason=reason)
    embed=discord.Embed()
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.add_field(name="Ban Hammer", value= f'{ctx.message.author} has banned {member} from server.\nReason: {reason}' , inline=False)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Sorry you do not have permissions to ban members")





@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member=None, reason=None):
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title="ERROR:", description="You can not kick yourself.", color=0xff0000)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
        embed.set_footer(text="made by z!#5199")
        await ctx.send(embed=embed)
        return
    if reason == None: 
        reason = 'None given'
    await member.kick(reason=reason)
    embed=discord.Embed()
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.add_field(name="Kick", value= f'{ctx.message.author} kicked {member} from the server.\nReason: {reason}' , inline=False)
    embed.set_footer(text="made by z!#5199")
    await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Sorry you do not have permissions to kick members!")




@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned User {user.mention}")


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Sorry you do not have permissions to unban members!")


@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Registered:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p"))
    embed.add_field(name="Joined:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.set_author(name="Kronos ✪", icon_url=client.user.avatar_url)
    embed.set_footer(text='ID: ' + str(member.id))
    await ctx.send(embed=embed)




@client.command(aliases=['av','pfp'])
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)


@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)



@client.command(aliases=['ri', 'role'])
async def roleinfo(ctx, *, role: discord.Role): # b'\xfc'
    guild = ctx.guild
    since_created = (ctx.message.created_at - role.created_at).days
    role_created = role.created_at.strftime("%d %b %Y %H:%M")
    created_on = "{} ({} days ago)".format(role_created, since_created)
    users = len([x for x in guild.members if role in x.roles])
    if str(role.colour) == "#000000":
        colour = "default"
        color = ("#%06x" % random.randint(0, 0xFFFFFF))
        color = int(colour[1:], 16)
    else:
        colour = str(role.colour).upper()
        color = role.colour
    em = discord.Embed(colour=color)
    em.set_author(name=f"Name: {role.name}"
    f"\nRole ID: {role.id}")
    em.add_field(name="Mentionable", value=role.mentionable)
    em.add_field(name="Position", value=role.position)
    em.add_field(name="Colour", value=colour)
    em.add_field(name='Creation Date', value=created_on)
    await ctx.send(embed=em)


@client.command(aliases=['bitcoin'])
async def btc(ctx): # b'\xfc'
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.set_author(name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
    await ctx.send(embed=em)

@client.command(aliases=['dong', 'penis'])
async def dick(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    em = discord.Embed(title=f"{user}'s Dick size", description=f"8{dong}D", colour=0x0000)
    await ctx.send(embed=em)

@client.command(aliases=['slots', 'bet'])
async def slot(ctx): # b'\xfc'
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if (a == b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} All matchings, you won!"}))
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} 2 in a row, you won!"}))
    else:
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} No match, you lost"}))


@client.command()
async def joke(ctx):  # b'\xfc'
    headers = {
        "Accept": "application/json"
    }
    async with aiohttp.ClientSession()as session:
        async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
            r = await req.json()
    await ctx.send(r["joke"])

@client.command(aliases=['guildpfp'])
async def servericon(ctx): # b'\xfc'
    em = discord.Embed(title=ctx.guild.name)
    em.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=em)


@client.command(aliases=['ethereum'])
async def eth(ctx): # b'\xfc'
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.set_author(name='Ethereum', icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
    await ctx.send(embed=em)

@client.command(aliases=['wouldyourather', 'would-you-rather', 'wyrq'])
async def wyr(ctx): # b'\xfc'
    r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qor = soup.find(id='qor').text
    qb = soup.find(id='qb').text
    em = discord.Embed(description=f'{qa}\n{qor}\n{qb}')
    await ctx.send(embed=em)








for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')







client.run('ODYyMTgwMzU1NDczOTMyMjg4.YOUmBw.xE2jVBkza6640wTC3NftyNcUNtc')