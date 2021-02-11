import discord
from discord.ext import commands
import random
from asyncio import sleep
from datetime import datetime


bot = commands.Bot(command_prefix='f!')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot is up.')

@bot.event
async def on_ready():
    print('Bot is up.')
    channel = bot.get_channel(780396225504739338)
    time = datetime.utcnow()
    await channel.send(f"Bot is up. ***{time}*** UTC")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting Down Bot...")
    await ctx.bot.logout()

async def status():
    while True:
        await bot.wait_until_ready()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over {len(bot.guilds)} guilds | f!help'))
        await sleep(60)
        await bot.change_presence(activity=discord.Game(name="I'm on fire! | f!help"))
        await sleep(60)
        await bot.change_presence(activity=discord.Game(name="Made by David™ winter boi⛄#4383! | f!help"))
        await sleep(60)
bot.loop.create_task(status())


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Your latency: {round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_permissions(administrator=True)
async def mod(ctx):
    await ctx.message.delete()
    await ctx.send('https://tenor.com/view/discord-mod-discord-gif-18242678')
@mod.error
async def mod_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}" .format(msg))
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command()
async def poll(ctx, *, message):
    mbed = discord.Embed(title=f"{message}", color = discord.Colour.orange())
    mbed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    msg = await ctx.channel.send(embed=mbed)
    await ctx.message.delete()
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@bot.command(name='avatar', aliases=['av'])
@commands.has_permissions(administrator=True)
async def av_cmd(ctx, user: discord.Member, member: discord.Member = None):
    member = ctx.author if not member else member
    mbed = discord.Embed(
        color = discord.Colour.orange(),
        title=f"{user}"
    )
    mbed.set_image(url=f"{user.avatar_url}")
    mbed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=mbed)
@av_cmd.error
async def av_error(ctx, error):
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command(name='serveravatar', aliases=['sav'])
@commands.has_permissions(administrator=True)
async def sav_cmd(ctx):
    mbed = discord.Embed(
        color = discord.Colour.orange(),
        title=f"{ctx.guild.name}"
    )
    mbed.set_image(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=mbed)
@av_cmd.error
async def sav_error(ctx, error):
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send('Sorry, but you are not allowed to use this command.')

#@bot.command()
#async def support(ctx):
    #user = ctx.message.author
    #await user.send('Join The Support Server If You Have Any Questions!: discord.gg/dm9fbpkzZa')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Definitely.",
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
"Very doubtful.",
"No."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick (ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member}.')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member}.')
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, but you are not allowed to use this command.')

@bot.command()
async def whois(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    mbed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    mbed.set_author(name=f'User Info - {member}.')
    mbed.set_thumbnail(url=member.avatar_url)
    mbed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)

    mbed.add_field(name='ID:', value=member.id)
    mbed.add_field(name='Name:', value=member.display_name)
    mbed.add_field(name='Boost:', value=member.premium_since)

    mbed.add_field(name='Created on: ', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    mbed.add_field(name='Joined on:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

    mbed.add_field(name=f'Roles:({len(roles)})', value=' '.join([role.mention for role in roles]))
    mbed.add_field(name='Top role:', value=member.top_role.mention)

    mbed.add_field(name='Bot?', value=member.bot)

    await ctx.send(embed=mbed)

@bot.command(aliases=['si'])
async def serverinfo(ctx):
    mbed = discord.Embed(
        colour = discord.Colour.orange(),
        title=f"{ctx.guild.name}"
    )
    mbed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    mbed.add_field(name='Region', value=f"`{ctx.guild.region}`")
    mbed.add_field(name='Member Count', value=f"{ctx.guild.member_count}")
    mbed.add_field(name='Created on', value=f'{ctx.guild.created_at}')
    mbed.add_field(name='')
    mbed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Guild ID: {ctx.guild.id}")
    await ctx.send(embed=mbed)

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    mbed = discord.Embed(
        colour = discord.Colour.orange()
    )

    mbed.set_author(name='Help Commands')
    mbed.add_field(name='f!help', value='Shows this message.', inline=False)
    mbed.add_field(name='f!ping', value='Tells what ping you currently have.', inline=False)
    mbed.add_field(name='f!say', value='Makes the bot say what you want it to say.', inline=False)
    mbed.add_field(name='f!poll', value='Makes a poll with the thumbs up and thumbs down emojis.', inline=False)
    mbed.add_field(name='f!support', value='Sends you an invite to the Support Server. (currently, this command is turned off)', inline=False)
    mbed.add_field(name='f!avatar/av', value='Displays the avatar of a certain user.', inline=False)
    mbed.add_field(name='f!serveravatar/sav', value='Displays the avatar of the server.', inline=False)
    mbed.add_field(name='f!whois [user]', value="Displays a message with the users info", inline=False)
    mbed.add_field(name='f!clear [amount]', value='Clears a certain amount of messages.', inline=False)
    mbed.add_field(name='f!8ball [yes/no question]', value='The magic virtual 8ball will answer your question!', inline=False)
    mbed.add_field(name='f!kick [user] [reason]', value='Kicks a certain person along with a reason for the kick.', inline=False)
    mbed.add_field(name='f!ban [user] [reason]', value='Bans a certain person along with a reason for the ban.', inline=False)
    await author.send(embed=mbed)



bot.run("NzU2NTQ0Mjc0OTU0NDUzMTIy.X2TYww.JUfAFGCCoD7UedE6pqmZTy79MIE")
