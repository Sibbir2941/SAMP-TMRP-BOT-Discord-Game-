import mysql.connector
import discord
import os
from discord.ext import commands
import vars
from discord import File
import discord.utils
from PIL import Image, ImageDraw, ImageFont
import io
import datetime
import asyncio

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='!', case_insensitive=True, help_command=None)

config = {
  'user': vars.USERNAME,
  'password': vars.PASSWORD,
  'host': vars.HOSTNAME,
  'database': vars.DATABASE,
  'raise_on_warnings': True
}

def connectdatabase():
  try:
      cnx = mysql.connector.connect(**config)
      cursor = cnx.cursor()
      print("MySQL Connection Created Successfully")
  except Exception as e:
      print(e)
      print("Exitting...")
      exit()

  def exec(query):
      try:
          cursor.execute(query)
          return cursor.fetchall()
      except Exception as e:
          return str(e)


@client.event
async def on_ready():
    print("Bot is ready.")
    await client.change_presence(activity=discord.Game(name="MultiVerse Hub"))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        pass
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Invalid Command", description="The command you entered is not valid. Please try again.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Command Error", description=f"There was an error while executing the command `{ctx.command}`:\n{error}", color=discord.Color.red())
        await ctx.send(embed=embed)

        raise error

    
# Define a function to check if a message contains a link
def contains_link(message):
    for word in message.content.split():
        if word.startswith('http') or word.startswith('www'):
            return True
    return False
# Define an event listener that triggers when a message is sent
@client.event
async def on_message(message):
    # Check if the message was sent in the desired channel (replace with your own channel ID)
    if message.channel.id == 1057730509783965726:
        # Check if the message contains a link
        if contains_link(message):
            # Get the username of the person who sent the link
            username = message.author.mention
            # Delete the message
            await message.delete()
            # Respond with an embed message
            embed = discord.Embed(title="Links are not allowed in this channel",
                                  description=f"{username}, please refrain from posting any links in this channel.",
                                  color=discord.Color.red())
            warning_message = await message.channel.send(embed=embed)
            # Delete the warning message after 2 minutes
            await asyncio.sleep(120)
            await warning_message.delete()
        else:
            # Let the message pass
            await client.process_commands(message)
    else:
        # Let the message pass if it was not sent in the desired channel
        await client.process_commands(message)




WELCOME_CHANNEL_ID = 1057730489663885382 # Replace with the ID of your welcome channel

@client.event
async def on_member_join(member):
    # Get the welcome channel
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)

    # Create the welcome message embed
    embed = discord.Embed(title=f"Welcome {member.display_name} to the server!", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

    # Add a description to the embed
    embed.add_field(name="Introduction", value="Thanks for joining our server. We hope you have a great time here!", inline=False)

    # Send the embed to the welcome channel
    await welcome_channel.send(embed=embed)

    # Send a direct message to the new member
    # Create the message embed
    embed = discord.Embed(title="Welcome to our server!", description="Before you start chatting, please make sure to follow the rules and guidelines below:", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

    # Add the rules and guidelines to the embed
    embed.add_field(name="Rule 1: Be respectful to others in the server.", value="Treat others with kindness and respect at all times.")
    embed.add_field(name="Rule 2: No spamming or flooding the chat with messages.", value="Please refrain from posting repetitive or unnecessary messages.")
    embed.add_field(name="Rule 3: No adult content or NSFW content allowed.", value="Any content that is not suitable for all ages is strictly prohibited.")
    embed.add_field(name="Rule 4: No advertising or self-promotion without permission from the server staff.", value="Please do not promote your own content or products without permission.")
    embed.add_field(name="Rule 5: No hate speech, discrimination, or harassment of any kind.", value="We do not tolerate any form of hate speech, discrimination, or harassment.")
    embed.add_field(name="Rule 6: Do not share personal information or sensitive data.", value="Please keep your personal information and sensitive data private and do not share it with others.")
    embed.add_field(name="Rule 7: Follow the instructions of the server staff.", value="Please follow the instructions of the server staff at all times.")
    embed.add_field(name="Rule 8: Do not use bots or scripts to automate actions in the server.", value="The use of bots or scripts to automate actions in the server is strictly prohibited.")
    embed.add_field(name="Rule 9: No trolling or intentionally causing disruption in the server.", value="Please do not engage in trolling or disruptive behavior.")
    embed.add_field(name="Rule 10: Do not use offensive language or slurs.", value="Please be mindful of the language you use and avoid using offensive slurs.")

    # Send the embed to the new member
    await member.send(embed=embed)


@client.command()
async def cinvite(ctx):
    guild = client.get_guild(1048298202153107508) # replace with your server ID
    channel = ctx.channel
    invite = await channel.create_invite(max_uses=1, unique=True) # creates a single-use invite link
    embed = discord.Embed(title="Join the server", description=f"Click [here]({invite}) to join the server!", color=0x00ff00)
    await ctx.send(embed=embed)

@client.command()
async def server_rules(ctx):
    rules = [
        {"name": "Respectful Behavior", "description": "Be respectful to others in the server."},
        {"name": "No Spamming", "description": "No spamming or flooding the chat with messages."},
        {"name": "No NSFW Content", "description": "No adult content or NSFW content allowed."},
        {"name": "No Unauthorized Promotion", "description": "No advertising or self-promotion without permission from the server staff."},
        {"name": "No Hate Speech or Harassment", "description": "No hate speech, discrimination, or harassment of any kind."},
        {"name": "No Sharing Personal Information", "description": "Do not share personal information or sensitive data."},
        {"name": "Follow Staff Instructions", "description": "Follow the instructions of the server staff."},
        {"name": "No Use of Bots or Scripts", "description": "Do not use bots or scripts to automate actions in the server."},
        {"name": "No Trolling or Disruptive Behavior", "description": "No trolling or intentionally causing disruption in the server."},
        {"name": "No Offensive Language", "description": "Do not use offensive language or slurs."},
        {"name": "No Impersonation", "description": "Do not impersonate other users or staff members."},
        {"name": "No Cheating", "description": "Do not use cheats or exploits in games."},
        {"name": "No Begging or Soliciting", "description": "Do not beg for gifts, roles, or any other benefits."},
        {"name": "English Only", "description": "Please speak in English only in the server."},
        {"name": "No Inappropriate Names", "description": "Do not use inappropriate names or usernames."},
        {"name": "No Voice Changer Software", "description": "Do not use voice changer software or similar programs in the voice channels."}
    ]

    embed = discord.Embed(title="Server Rules", color=0x00ff00)
    for i, rule in enumerate(rules):
        embed.add_field(name=f"{rule['name']} ({i+1})", value=rule['description'], inline=False)

    embed.set_footer(text="Please follow the rules to maintain a friendly and respectful community.")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def aclear(ctx):
    channel = ctx.channel

    confirm_embed = discord.Embed(title="Confirmation Prompt", description="Are you sure you want to delete all messages in this channel? Type `!aclear confirm` to confirm.", color=discord.Color.orange())
    confirm_embed.set_author(name="MultiVerse Hub Bot")
    confirm_message = await ctx.send(embed=confirm_embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == '!aclear confirm'

    try:
        confirm_response = await client.wait_for('message', check=check, timeout=86400.0)  # Changed timeout to 1 day
    except asyncio.TimeoutError:
        await confirm_message.delete()
        timeout_embed = discord.Embed(title="Confirmation Timed Out", description="You took too long to confirm the clear command.", color=discord.Color.red())
        timeout_embed.set_author(name="MultiVerse Hub Bot")
        await ctx.send(embed=timeout_embed)
    else:
        await channel.purge()  # Use the purge() method instead of delete_messages()

        confirm_embed = discord.Embed(title="Clear Command Executed", description=f"All messages in {channel.mention} have been deleted by {ctx.author.mention}", color=discord.Color.red())
        confirm_embed.set_author(name="MultiVerse Hub Bot")
        await ctx.send(embed=confirm_embed)



@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit = amount)


client.run('MTA5MjUyNjQzNDM4NTQxMjE1Nw.GvgGSR.X0CN8ScdUE1zKlDZgKyCYMjxCPvXudv_awSk3Q')
