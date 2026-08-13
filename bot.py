import mysql.connector
import discord
import requests
import datetime
import pytz
import asyncio
import os
from discord.ext import commands
import vars
from discord import File
import discord.utils
from PIL import Image, ImageDraw, ImageFont
import io

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='=', case_insensitive=True, help_command=None)

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



server_ip = "154.6.205.30"
server_port = 7777

bot_token = ""
channel_id = 1091786250635202621


async def send_status():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    # Select online users from the 'users' table
    sql = "SELECT * FROM users WHERE isonline = '1'"
    cursor.execute(sql)

    data = []
    for row in cursor:
        name = row[1]
        score = row[11]
        ping = row[12]
        data.append([name, score, ping])

    # Create a table of online players
    table = "+----------------+---------+-------+\n| USERNAME       | SCORE   | PING  |\n+----------------+---------+-------+\n"
    for row in data:
        name = row[0]
        score = row[1]
        ping = row[2]
        table += f"| {name:<15}| {score:<8}| {ping:<6}|\n"
    table += "+----------------+---------+-------+"

    # Get the number of online players
    players = len(data)
    
    # Get the current time in the UTC timezone
    utc_now = datetime.datetime.now(pytz.utc)
    # Convert the UTC time to the local timezone
    local_now = utc_now.astimezone(pytz.timezone('US/Eastern'))
    
    # Create an embed with server status information
    embed = discord.Embed(
        title='The Multiverse Roleplay',
        description=f'**IP ADDRESS:**\n```{server_ip}:{server_port}```\n\n**Status:**\n```diff\n+ Server Online!\n```\n\n**Players:**\n```{players}/{100}```\n\n **Current Players:**\n```{table}```\n*Status Refreshed every 1 minute*',
        color=0xFF5733 # Set the color to orange
    )
    embed.set_footer(text=f"Last refreshed at {local_now.strftime('%Y-%m-%d %I:%M %p %Z')}")

    try:
        # Send the embed to the designated channel
        channel = await client.fetch_channel(channel_id)
        async for message in channel.history(limit=1):
            await message.delete()
        await channel.send(embed=embed)
    except discord.errors.NotFound:
        print(f"Error: Channel not found for ID {channel_id}")
    except discord.errors.Forbidden:
        print(f"Error: Bot does not have permission to send messages in channel ID {channel_id}")

    # Wait for 1 minute before refreshing the status
    await asyncio.sleep(60) 
    await send_status()
    
    # Close the MySQL connection and cursor
    cursor.close()
    cnx.close()
    
@client.event
async def on_ready():
    print("Bot is ready.")
    await client.change_presence(activity=discord.Game(name="The Multiverse Roleplay"))
    await send_status()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You entered an invalid command. Try =help to see list of commands.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['serverip'])
async def ip(ctx):
   
    embed = discord.Embed(title='Server IP ', description=f'```{"154.6.205.30:7777"}```')
    await ctx.send(embed=embed)
WELCOME_CHANNEL_ID = 1092745471405084722
VERIFY_CHANNEL_NAME = "𝐕𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧"
DC_RULES_CHANNEL_NAME = "📚〢𝙳𝚒𝚜𝚌𝚘𝚛𝚍-𝚁𝚄𝙻𝙴𝚂"
RP_RULES_CHANNEL_NAME = "📩〢server-rules"
ANNOUNCEMENT_CHANNEL_NAME = "📢〢𝙰𝙽𝙽𝙾𝚄𝙽𝙲𝙴𝙼𝙴𝙽𝚃"

@client.event
async def on_member_join(member):
    # Get the welcome and verify channels
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    verify_channel = discord.utils.get(member.guild.channels, name=VERIFY_CHANNEL_NAME)

    # Create the welcome message embed
    embed = discord.Embed(title=f"Welcome {member.display_name} to the server!", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

    # Add a description and "go to channel" system to the embed
    embed.add_field(name="Introduction", value=f"Please verify yourself in the {verify_channel.mention} channel.", inline=False)
    embed.set_footer(text=f"Click on the {verify_channel.mention} channel name above to go there now!")

    # Send the embed to the welcome channel
    await welcome_channel.send(embed=embed)

    # Send a direct message to the new member
    # Get the verify channel and send a message telling the user to go there
    verify_channel = discord.utils.get(member.guild.channels, name=VERIFY_CHANNEL_NAME)
    dc_rules_channel = discord.utils.get(member.guild.channels, name=DC_RULES_CHANNEL_NAME)
    rp_rules_channel = discord.utils.get(member.guild.channels, name=RP_RULES_CHANNEL_NAME)
    announcement_channel = discord.utils.get(member.guild.channels, name=ANNOUNCEMENT_CHANNEL_NAME)

    # Create the message embed
    embed = discord.Embed(title="Welcome to the server!", description=f"Please go to the {verify_channel.mention} channel to verify yourself!\n\nBefore you start chatting, please make sure to:\n- Read the Discord server rules from {dc_rules_channel.mention}\n- Read the server roleplay rules from {rp_rules_channel.mention}\n- Always check the {announcement_channel.mention} channel for important server announcements. Have fun!", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)

# Send the embed to the new member
    await member.send(embed=embed)
   
LEAVE_CHANNEL_ID = 1092750912113606707
SERVER_LINK = "https://discord.gg/nW4z8a5ZFF"

@client.event
async def on_member_remove(member):
    # Get the leave channel using the channel ID
    leave_channel = client.get_channel(LEAVE_CHANNEL_ID)

    # Create the embed message
    embed = discord.Embed(title=f"{member.display_name} has left the server. :(", color=discord.Color.red())
    embed.set_thumbnail(url=member.avatar.url)

    # Get the current time in Bangladesh time zone
    bd_time = datetime.datetime.now(pytz.timezone('Asia/Dhaka')).strftime('%Y-%m-%d %H:%M:%S')

    # Add a description to the embed with the Bangladesh time
    embed.add_field(name="User Information", value=f"**Name:** {member.name}\n**ID:** {member.id}\n**Joined at:** {member.joined_at}\n**Left at:** {bd_time} (Bangladesh Standard Time)", inline=False)

    # Send the embed message to the leave channel
    await leave_channel.send(embed=embed)

    embed = discord.Embed(title="Goodbye!", description=f"We're sorry to see you go, {member.name}! If you ever want to rejoin the server, you're always welcome back.", color=discord.Color.red())
    embed.add_field(name="Server Link", value=SERVER_LINK)

# Send the embed to the new member
    await member.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def takecitizenrole(ctx):
    # Get the TMRP Citizen role
    role = discord.utils.get(ctx.guild.roles, name='🤵• TMRP CITIZEN')

    # If the role does not exist, send an error message and return
    if role is None:
        await ctx.send('TMRP Citizen role not found')
        return

    # Loop through all members in the server and remove the TMRP Citizen role
    for member in ctx.guild.members:
        await member.remove_roles(role)

    # Create an embed message to notify the user that the operation was successful
    embed = discord.Embed(
        title='TMRP Citizen role removed',
        description='The TMRP Citizen role has been removed from all members',
        color=discord.Color.green()
    )

    # Send the embed message to the command user
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Command List:", description="")
    embed.add_field(name="=players", value="```Displays the number of players currently online```", inline=False)
    embed.add_field(name="=stats [player]", value="```Displays statistics for the specified player```", inline=False)
    embed.add_field(name="=botinfo", value="```Displays information about the bot, such as its version and creator```", inline=False)
    embed.add_field(name="=mostgifts", value="```Displays a list of the users with the most gifts received```", inline=False)
    embed.add_field(name="=ip", value="```Displays the server IP```", inline=False)
    await ctx.send(embed=embed)

@client.command(aliases=['online', 'total'])
async def players(ctx):
    if ctx.channel.id != 1091786260265304205:
        await ctx.send('Wrong channel. Use this command in <#1091786260265304205>.')
        return

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE isonline = '1'"
    cursor.execute(sql)

    data = []
    for row in cursor:
        name = row[1]
        score = row[11]
        ping = row[12]
        data.append([name, score, ping])

    table = "+----------------+---------+-------+\n| USERNAME       | SCORE   | PING  |\n+----------------+---------+-------+\n"
    for row in data:
        name = row[0]
        score = row[1]
        ping = row[2]
        table += f"| {name:<15}| {score:<8}| {ping:<6}|\n"
    table += "+----------------+---------+-------+"

    players = len(data)
    embed = discord.Embed(
        title='The Multiverse Roleplay',
        description=f'**IP ADDRESS:** \n```{"154.6.205.30:7777"}```\n\n**Status**```\n✅ Server Online!```\n\n**Players**\n```{players}/{100}```\n\n **Current Players** \n```{table}```'
    )
    
    await ctx.send(embed=embed)

    cursor.close()
    cnx.close()

@client.command()
async def mostgifts(ctx):

    if ctx.channel.id != 1091786260265304205:
      if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send('Wrong channel. Use this command in <#1091786260265304205>.')
        return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE `gifts` > '0' ORDER BY `gifts` DESC LIMIT 10"
    cursor.execute(sql)
    total="Name - Gifts\n"
    substring=""
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("No one collected gifts yet.")
      return
    players=0;
    for row in cursor:
        name = row[1]
        level = row[203]
        substring= f'\n{name} - {level}'
        total =  total + substring
        players += 1
    await ctx.send(f'```{total}\n\nGifts Leaderboard | Fall Festival```')
    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def record(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return    
    if not name:
      await ctx.send("=record [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE p_name = %s", (name, ))
    myresult = cursor.fetchall()
    if not  myresult:
      await ctx.send("Couldnot find the specified name in the database.")
      return
    for x in myresult:
      userid = x[0]
    admin_name="None"
    reason = "None"
    cursor.execute("SELECT record.*, users.p_name AS admin_name FROM record LEFT JOIN users ON record.admin_id = users.user_id WHERE punished_id = %s", (userid, ))
    myresult = cursor.fetchall()
    if not  myresult:
      await ctx.send("Couldnot find any record on specified name.")
      return

    total=""
    substring=""
    rowcount = 1
    for x in myresult:
      admin_name=x[6]
      reason = x[2]
      punishid = x[0]
      typeofpunishment = x[5]
      punishment = f'{rowcount}. [SqlID: {punishid}] Name: {name} | Punished by: {admin_name} | Type: {typeofpunishment} | Reason: {reason}\n\n'
      total = total+punishment
      rowcount +=1

    filename = f'{name} Record.txt'
    with open(filename, 'w') as f:
        f.write(total)
        f.close()
    
    await ctx.send(file=discord.File(filename))
    os.remove(filename)

    cursor.close()
    cnx.close()

# Replace with your own values
VERIFY_CHANNEL_ID = 1092803041553547274 # Replace with the ID of your verification channel
EMOJI = '✅' # Replace with the emoji you want to use
TMRP_ROLE_ID = 1091786197166215280 # Replace with the ID of the TMRP Citizen role
@client.command()
@commands.has_permissions(manage_messages=True)
async def verify(ctx):
    # Get the verification channel by ID
    verify_channel = client.get_channel(VERIFY_CHANNEL_ID)

    # If the channel does not exist, send an error message and return
    if verify_channel is None:
        await ctx.send('Verification channel not found')
        return

    # Create a new embedded message using the discord.Embed class
    embed = discord.Embed(
        title='Server Verification',
        description='Welcome to our server! To gain access to all channels, please complete the following steps:\n\n1. Read our Discord server rules in #📚〢𝐃𝐢𝐬𝐜𝐨𝐫𝐝-𝐑𝐮𝐥𝐞𝐬 .\n2. Read our Roleplay server rules in #📩〢𝐑𝐨𝐥𝐞𝐩𝐥𝐚𝐲-𝐑𝐮𝐥𝐞𝐬.\n3. React to this message with the check mark emoji to verify that you have read and agree to our rules.\n\nOnce you have completed these steps, our bot will grant you access to the rest of the server. Thank you!',
        color=discord.Color.green()
    )

    # Send the embedded message to the verification channel
    message = await verify_channel.send(embed=embed)

    # Add a check mark emoji reaction to the message
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

@client.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id
    if channel_id != VERIFY_CHANNEL_ID:
        return

    guild_id = payload.guild_id
    guild = client.get_guild(guild_id)
    if guild is None:
        return

    member_id = payload.user_id
    member = guild.get_member(member_id)
    if member is None:
        return

    if str(payload.emoji) == '\N{WHITE HEAVY CHECK MARK}':
        role = guild.get_role(TMRP_ROLE_ID)
        if role is not None:
            await member.add_roles(role)

            # Send a private message to the user to inform them they have been verified
            embed = discord.Embed(
                title="Verification Successful!",
                description="Congratulations, you have been verified! You now have access to all channels.",
                color=discord.Color.green()
            )
            await member.send(embed=embed)


@client.command()
async def botinfo(ctx):
    servers = ['The Multiverse Roleplay']

    embed = discord.Embed(title='Multiverse Bot nformation', color=discord.Color.green())
    embed.add_field(name='Creator & Developer', value='Mohammad Sibbir')
    embed.add_field(name='Bot Prefix', value='"="')
    embed.add_field(name='UI Language', value='English')
    embed.add_field(name='Ping', value=f'{client.latency * 1000:.0f}ms')
    embed.add_field(name='Version', value='v0.1')
    embed.add_field(name='Total Commands', value=f'{len(client.commands)} Command(s)')
    embed.add_field(name='Watching Servers', value='\n'.join(servers))
    embed.add_field(name='Description', value='It\'s a discord client which is made by Python(v3.11) and used libraries are Discord.py (v2.1.0) and Samp-Client library (3.0.1). The script of this client is fully written by Mohammad Sibbir. This bot is fully dedicated to SA-MP server.')
    await ctx.send(embed=embed)




@client.command()
async def roles(ctx):
    embed = discord.Embed(title='Available Roles')
    embed.add_field(name='Samp', value='React with 👍 to get Samp role', inline=False)
    embed.add_field(name='FiveM', value='React with 🚀 to get FiveM role', inline=False)
    embed.add_field(name='PC Player', value='React with 💻 to get PC Player role', inline=False)
    embed.add_field(name='Mobile Player', value='React with 📱 to get Mobile Player role', inline=False)
    embed.add_field(name='Male', value='React with 👨 to get Male role', inline=False)
    embed.add_field(name='Female', value='React with 👩 to get Female role', inline=False)
    embed.add_field(name='18-', value='React with 🔞 to get 18- role', inline=False)
    embed.add_field(name='18+', value='React with 🔞 to get 18+ role', inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('🚀')
    await message.add_reaction('💻')
    await message.add_reaction('📱')
    await message.add_reaction('👨')
    await message.add_reaction('👩')
    await message.add_reaction('🔞')
    await message.add_reaction('🔞')

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    message = reaction.message
    if message.author.bot:
        if reaction.emoji == '👍':
            role = discord.utils.get(user.guild.roles, name='Samp')
            await user.add_roles(role)
        elif reaction.emoji == '🚀':
            role = discord.utils.get(user.guild.roles, name='FiveM')
            await user.add_roles(role)
        elif reaction.emoji == '💻':
            role = discord.utils.get(user.guild.roles, name='PC Player')
            await user.add_roles(role)
        elif reaction.emoji == '📱':
            role = discord.utils.get(user.guild.roles, name='Mobile Player')
            await user.add_roles(role)
        elif reaction.emoji == '👨':
            role = discord.utils.get(user.guild.roles, name='Male')
            await user.add_roles(role)
        elif reaction.emoji == '👩':
            role = discord.utils.get(user.guild.roles, name='Female')
            await user.add_roles(role)
        elif reaction.emoji == '🔞':
            role = discord.utils.get(user.guild.roles, name='🔞 18-')
            await user.add_roles(role)
            role = discord.utils.get(user.guild.roles, name='18+')
            await user.add_roles(role)


@client.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    message = reaction.message
    if message.author.bot:
        if reaction.emoji == '👍':
            role = discord.utils.get(user.guild.roles, name='Samp')
            await user.remove_roles(role)
        elif reaction.emoji == '🚀':
            role = discord.utils.get(user.guild.roles, name='FiveM')
            await user.remove_roles(role)
        elif reaction.emoji == '💻':
            role = discord.utils.get(user.guild.roles, name='PC Player')
            await user.remove_roles(role)
        elif reaction.emoji == '📱':
            role = discord.utils.get(user.guild.roles, name='Mobile Player')
            await user.remove_roles(role)
        elif reaction.emoji == '👨':
            role = discord.utils.get(user.guild.roles, name='Male')
            await user.remove_roles(role)
        elif reaction.emoji == '👩':
            role = discord.utils.get(user.guild.roles, name='Female')
            await user.remove_roles(role)
        elif reaction.emoji == '🔞':
            role = discord.utils.get(user.guild.roles, name='🔞 18-')
            await user.remove_roles(role)
            role = discord.utils.get(user.guild.roles, name='18+')
            await user.remove_roles(role)


@client.command()
@commands.has_permissions(manage_messages=True)
async def names(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=name [Name]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM namehistory WHERE log LIKE CONCAT('%', %s, '%') LIMIT 1", (name, ))
    myresult = cursor.fetchall()
    if not  myresult:
      await ctx.send("There is no name history on specified name.")
      return
    for x in myresult:
      userid=x[2]

    cursor.execute("SELECT * FROM namehistory WHERE user_id = %s", (userid, ))
    total = ""
    myresult = cursor.fetchall()
    for x in myresult:
      log=x[1]
      total = total + log + '\n'

    filename = f'{name}_Names.txt'
    with open(filename, 'w') as f:
        f.write(total)
        f.close()
    await ctx.send(file=discord.File(filename))
    os.remove(filename)

    cursor.close()
    cnx.close()


@client.command()
@commands.has_permissions(manage_messages=True)
async def expunge(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=expunge [Punishment ID]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM record WHERE punish_ID = %s", (name, ))
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("Couldnot find a punishment with that ID.")
      return
    cnx.commit()
    await ctx.send("You have successfully expunged the specified punishment.")

    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=unban [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM banned WHERE user_name = %s", (name, ))
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("Couldnot find a banned player with that name.")
      return
    cnx.commit()
    await ctx.send("You have successfully unbanned the specified player.")

    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def whitelist(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=whitelist [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM whitelist WHERE p_name = %s", (name, ))
    myresult = cursor.fetchall()
    if myresult:
      await ctx.send("Player already exists in the database.")
      return
    cursor.execute("INSERT INTO whitelist (p_name) VALUES (%s)", (name, ))
    cnx.commit()
    await ctx.send(f'You have successfully added {name} to whitelist.')
    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def acremove(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=acremove [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM users WHERE p_name = %s", (name, ))
    myresult = cursor.fetchall()
    if not myresult:
      await ctx.send("Couldnot find a registered user with that name.")
      return
    cursor.execute("UPDATE users SET acforced = '0' WHERE p_name = %s", (name, ))
    cnx.commit()
    await ctx.send(f'You have successfully removed {name} from launcher.')
    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def acforce(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=acforce [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM users WHERE p_name = %s", (name, ))
    myresult = cursor.fetchall()
    if not myresult:
      await ctx.send("Couldnot find a registered user with that name.")
      return
    cursor.execute("UPDATE users SET acforced = '1' WHERE p_name = %s", (name, ))
    cnx.commit()
    await ctx.send(f'You have successfully added {name} to launcher list.')
    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def vpnlist(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=vpnlist **[Firstname_LastName]**")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM vpnlist WHERE p_name = %s", (name, ))
    myresult = cursor.fetchall()
    if myresult:
      await ctx.send("Player already exists in the VPN list.")
      return
    cursor.execute("INSERT INTO vpnlist (p_name) VALUES (%s)", (name, ))
    cnx.commit()
    embed = discord.Embed(title='Add Player Name To VPN List!!', description=f'You have successfully added {name} to vpn list.')
    await ctx.send(embed=embed)
    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def removevpnlist(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=removevpnlist [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM vpnlist WHERE p_name = %s", (name, ))
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("Couldnot find a vpn list player with that name.")
      return
    cnx.commit()

    embed = discord.Embed(title='Remove Player From VPN List', description=f"You have successfully removed {name} from vpn list.")
    await ctx.send(embed=embed)

    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def removewhitelist(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=removewhitelist [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM whitelist WHERE p_name = %s", (name, ))
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("Couldnot find a whitelisted player with that name.")
      return
    cnx.commit()
    await ctx.send(f"You have successfully removed {name} from whitelist.")

    cursor.close()
    cnx.close()

@client.command()
@commands.has_permissions(manage_messages=True)
async def checkban(ctx, *, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=checkban [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM banned WHERE user_name = %s", (name, ))
  
    myresult = cursor.fetchall()
    if not  myresult:
      message=f'``{name} is not banned.``'
      await ctx.send(message)
      return
    for x in myresult:
      admin=x[5]
      reason=x[4]
    message=f'``{name} is banned by {admin}. Reason: {reason}``'
    await ctx.send(message)

    cursor.close()
    cnx.close()

BASEDIR = "/home/ogp_agent/OGP_User_Files/port_5333/scriptfiles/Ostalo"

@client.command()
@commands.has_permissions(manage_messages=True)
async def logs(ctx, type=None, date=None, name=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return        
    if not name:
      await ctx.send("=logs [type] [date]  [search]")
      return
    if not type:
      await ctx.send("=logs [type] [date]  [search]")
      return
    if not date:
      await ctx.send("=logs [type] [date] [search]")
      return
    if type == "b":
        list_open = open(os.path.join(BASEDIR, 'LogBChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'OOC logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "l":
        list_open = open(os.path.join(BASEDIR, 'LogICChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Local IC logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "s":
        list_open = open(os.path.join(BASEDIR, 'LogSChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Shout logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "w":
        list_open = open(os.path.join(BASEDIR, 'LogWChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Whisper logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "cw":
        list_open = open(os.path.join(BASEDIR, 'LogCChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Vehicle whisper logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "wt":
        list_open = open(os.path.join(BASEDIR, 'LogWT.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Walkie Talkie logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "kill":
        list_open = open(os.path.join(BASEDIR, 'DeathLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Kill logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "pm":
        list_open = open(os.path.join(BASEDIR, 'LogAODG.log'), encoding="utf8")
        line = list_open.readline()
        total=f'PM logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "me":
        list_open = open(os.path.join(BASEDIR, 'ActionLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Action(ME) logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "attempt":
        list_open = open(os.path.join(BASEDIR, 'AttemptLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Attempt logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "do":
        list_open = open(os.path.join(BASEDIR, 'DoLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Action(DO) logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line)
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)


    elif type == "hit":
        list_open = open(os.path.join(BASEDIR, 'HitLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Damage logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line) + '\n'
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "weapon":
        list_open = open(os.path.join(BASEDIR, 'WeaponLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Weapon logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line) + '\n'
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "disconnect":
        list_open = open(os.path.join(BASEDIR, 'Disconnect.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Disconnection logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line) + '\n'
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "connect":
        list_open = open(os.path.join(BASEDIR, 'Connect.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Connection logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line) + '\n'
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "buy":
        list_open = open(os.path.join(BASEDIR, 'Purchase.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Purchase logs containing word {name}\n'
        while line:
            line = list_open.readline()
            if name in line and date in line:
                total =  total + str(line) + '\n'
        list_open.close()
        filename = f'{name}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

@client.command()
@commands.has_permissions(manage_messages=True)
async def wholelogs(ctx, type=None, date=None):
    if ctx.channel.id != 1091786316506726491:
      await ctx.send('Wrong channel. Use this command in <#1091786316506726491>.')
      return            
    if not type:
      await ctx.send("=wholelogs [type] [date]")
      return
    if not date:
      await ctx.send("=wholelogs [type] [date")
      return
    if type == "b":
        list_open = open(os.path.join(BASEDIR, 'LogBChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'OOC logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "l":
        list_open = open(os.path.join(BASEDIR, 'LogICChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Local IC logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "s":
        list_open = open(os.path.join(BASEDIR, 'LogSChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Shout logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "w":
        list_open = open(os.path.join(BASEDIR, 'LogWChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Whisper logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "cw":
        list_open = open(os.path.join(BASEDIR, 'LogCChat.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Vehicle whisper logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "wt":
        list_open = open(os.path.join(BASEDIR, 'LogWT.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Walkie Talkie logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "pm":
        list_open = open(os.path.join(BASEDIR, 'LogAODG.log'), encoding="utf8")
        line = list_open.readline()
        total=f'PM logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        
    elif type == "me":
        list_open = open(os.path.join(BASEDIR, 'ActionLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Action(ME) logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "attempt":
        list_open = open(os.path.join(BASEDIR, 'AttemptLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Attempt logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    elif type == "do":
        list_open = open(os.path.join(BASEDIR, 'DoLogs.log'), encoding="utf8")
        line = list_open.readline()
        total=f'Action(DO) logs containing for date {date}\n'
        while line:
            line = list_open.readline()
            if date in line:
                total =  total + str(line)
        list_open.close()
        date = date.replace("/", "-")
        filename = f'{date}.txt'
        with open(filename, 'w') as f:
            f.write(total)
            f.close()
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    
@client.command(aliases=['signature', 'sig'])
async def stats(ctx,*, name=None ):

    if not name:
      await ctx.send("=stats [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE p_name = %s", (name, ))
    
    myresult = cursor.fetchall()
    if not  myresult:
      await ctx.send("Couldnot find the specified name in the database.")
      return

    bank = 0
    for x in myresult:
      user_id = x[0]
      playername=x[1]
      level=x[11]
      money=x[10]
      hours=x[38]
      lastlogin=x[52]
      skin=x[17]

    cursor.execute("SELECT * FROM bank WHERE bankOwner = %s LIMIT 5", (user_id, ))
    
    for row in cursor:
        bank = bank + row[1]


    SKIN_SIZE = 256
    AVATAR_SIZE = 256
    background_image = Image.open('tmrp.png') 
    background_image = background_image.convert('RGBA')
    image = background_image.copy()

    image_width, image_height = image.size



    draw = ImageDraw.Draw(image) 
    text = f'Name: {playername}'
    font = ImageFont.truetype("goodtimes.ttf", 45, encoding="unic")

    text_width, text_height = draw.textsize(text, font=font)


    draw.text((460, 100), text, fill=(255,255,255,255), font=font)
    text = f'Level: {level}'
    draw.text((460, 200), text, fill=(255,255,255,255), font=font)
    text = f'Cash: {money}$'
    draw.text((460, 300), text, fill=(255,255,255,255), font=font)
    text = f'Bank: {bank}$'
    draw.text((460, 400), text, fill=(255,255,255,255), font=font)
    text = f'Hours Played: {hours}'
    draw.text((460, 500), text, fill=(255,255,255,255), font=font)
    text = f'Last Login: {lastlogin}'
    draw.text((460, 600), text, fill=(255,255,255,255), font=font)


    imagelink = f'skins/{skin}.png'
    avatar_image= Image.open(imagelink)
    avatar_image = avatar_image.convert('RGBA')
    avatar_image = avatar_image.resize((350, 800)) 
    image.paste(avatar_image, (0, 0), avatar_image)


    buffer_output = io.BytesIO()
    image.save(buffer_output, format='PNG')
    buffer_output.seek(0)
    await ctx.send(file=File(buffer_output, f'{name}.png'))
    cursor.close()
    cnx.close()

client.run('MTA5MTMyOTY4MTMwOTA0ODg4Mg.GGjT9b.GDf4Fr2H-YOb-IDjrj0fA8akmXXGNOHZDpthf0')
