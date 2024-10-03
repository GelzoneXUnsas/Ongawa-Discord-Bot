import discord
import aiohttp
import os
import json
from discord.ext import commands
from discord import File
from io import BytesIO

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# File to store user data
DATA_FILE = "user_data.json"

# Load user data from file if it exists and is valid
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error loading user data. Initializing empty data.")
        #user_data = {}
else:
    print("FAILED TO LOAD USER DATA")
    user_data = {}

# Define exp thresholds and roles
exp_roles = {
    100: "Pluse",
    200: "Riff",
    400: "Rhythm",
    800: "Harmony",
    1600: "Tempo",
}

# Exp gain values
MESSAGE_EXP = 1
REFERRAL_EXP = 100


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    # Send "hello" when the bot starts
    #for guild in bot.guilds:
    #for channel in guild.text_channels:
    #print(f"Sending 'hello' to {channel.name} in {guild.name}")
    #if channel.permissions_for(guild.me).send_messages:
    #await channel.send("hello")


@bot.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == bot.user:
        return

    # Add exp for regular messages
    await add_exp(message.author, MESSAGE_EXP, message.guild, message.channel)

    # Check for referral messages from Invite Tracker
    if message.author.name == "Invite Tracker":
        await process_referral(message)

    # Respond to the message
    #await message.channel.send(f"that's cool {message.author.name}")

    await bot.process_commands(message)


@bot.command()
async def xp(ctx):
    """Show the user's current XP."""
    user_id = ctx.author.id
    if str(user_id) in user_data:
        current_exp = user_data[str(user_id)]['exp']
        await ctx.send(
            f"{ctx.author.name}, you currently have {current_exp} XP!")
    else:
        await ctx.send(f"{ctx.author.name}, you don't have any XP yet.")


async def process_referral(message):
    content = message.content
    await message.channel.send("someones been referraled")
    if "has been invited by" in content:
        parts = content.split(" ")
        invited_user = parts[0]
        referrer = parts[5]
        #await message.channel.send(
        #f"{invited_user} been referralllled by {referrer}")

        referrer_member = find_member_by_name_or_nickname(
            message.guild, referrer)

        await add_exp(referrer_member, REFERRAL_EXP, message.guild,
                      message.channel)


async def add_exp(member, amount, guild, channel):
    global user_data
    if member.name == None:
        print("Could not find member")
        return
    if str(member.id) not in user_data:
        user_data[str(member.id)] = {'exp': 0, 'referrals': 0}

    user_data[str(member.id)]['exp'] += amount

    current_exp = user_data[str(member.id)]['exp']

    # Save updated user data to file
    save_user_data()

    # Send a message with the user's current exp
    #await channel.send(f"{member.name} now has {current_exp} XP!")

    # Assign roles based on exp thresholds
    for exp_threshold, role_name in exp_roles.items():
        if current_exp >= exp_threshold:
            role = discord.utils.get(guild.roles, name=role_name)
            if role and role not in member.roles:
                await member.add_roles(role)
                print(f"🎉 Congratulations {member.name}! You've leveled up and unlocked the {role_name} role! 🚀")
                await channel.send(f"Assigned {role_name} to {member.name}")


@bot.command()
async def announce(ctx, channel_name: str, *, message: str = ""):
    """Send an announcement message to a specific channel."""

    # Debug print to check if the command is being invoked
    print(
        f"Announce command invoked by {ctx.author.name} for channel '{channel_name}'"
    )

    # Normalize the input channel name by converting to lowercase for comparison
    channel_name = channel_name.lower()

    # Find the closest matching channel by checking if the provided name is in the actual channel name
    channel = None
    for ch in ctx.guild.text_channels:
        if channel_name in ch.name.lower():
            channel = ch
            break

    if channel is None:
        await ctx.send(f"Channel '{channel_name}' not found.")
        return

    try:
        # If an image URL is provided, send the image
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            # Create a discord file object
                            file = discord.File(fp=BytesIO(image_data),
                                                filename="image.png")
                            await channel.send(file=file)
                        else:
                            await ctx.send(
                                f"Failed to download image from URL: {attachment.url}"
                            )
        # Send the message to the specified channel
        if message:
            await channel.send(message)
        await ctx.send(f"Message sent to {channel_name}")
    except discord.Forbidden:
        await ctx.send(
            "I don't have permission to send messages in that channel.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to send message: {e}")


def find_member_by_name_or_nickname(guild, name):
    for member in guild.members:
        if member.name == name or member.nick == name:
            return member
    return None


def save_user_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
