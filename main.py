import discord
from discord.ext import commands
import requests

# Bot settings
TOKEN = 'MTMwMjM4NDgwMzUwMDUyNzc2Nw.GIedf6.m4aw4K5c4WnX1uCZnP3FuRN5H-pyYgjXqhijqc'  # replace with your bot token
PREFIX = '!'
ROLE_NAME = 'premium'  # Role name that can use the command
IMAGE_URL = 'https://i.imgur.com/GkrgKt0.jpeg'  # Replace with the actual image URL
ALLOWED_CHANNEL_ID = 1305301733609570355  # ID of the channel where the command can be used

# Services and their links
SERVICES = {
    'discord': 'https://z7services.lol/api/generate.php?type=discord',
    'steam': 'https://z7services.lol/api/generate.php?type=steam',
    'spotify': 'https://z7services.lol/api/generate.php?type=spotify',
    'epicgames': 'https://z7services.lol/api/generate.php?type=epicgames',
    'nitro': 'https://z7services.lol/api/generate.php?type=nitro',
    'r6': 'https://z7services.lol/api/generate.php?type=r6',
    'tiktok': 'https://z7services.lol/api/generate.php?type=tiktok',
}

# Initialize the bot
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


# Check if the user has the premium role
def has_premium_role(member):
    return any(role.name == ROLE_NAME for role in member.roles)


# /generate command with cooldown
@bot.command(name="generate")
@commands.cooldown(
    1, 1,
    commands.BucketType.user)  # Limit usage to every 250 seconds per user
async def generate(ctx, service: str):
    # Check if the command is used in the allowed channel
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        embed = discord.Embed(
            title="Access Denied",
            description=
            "This command can only be used in the designated channel.",
            color=discord.Color.red())
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.send(embed=embed)
        return

    # Check if the user has the premium role
    if not has_premium_role(ctx.author):
        embed = discord.Embed(
            title="Access Denied",
            description=
            "Only users with the 🏅 **Premium** role can use this command.",
            color=discord.Color.red())
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.send(embed=embed)
        return

    # Check if the service exists
    if service not in SERVICES:
        embed = discord.Embed(
            title="Service Not Found",
            description="Invalid service. Please use one of the following: " +
            ", ".join(SERVICES.keys()),
            color=discord.Color.red())
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.send(embed=embed)
        return

    # Service URL
    url = SERVICES[service]

    try:
        # Request data from the service
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.text

        # Send the result in DM with improved formatting
        embed = discord.Embed(title=f"Service Result: {service.capitalize()}",
                              description="Here is the requested data:",
                              color=discord.Color.green())
        embed.add_field(name="Result",
                        value=f"```{data}```")  # Make text easier to copy
        embed.set_footer(text="Thank you for using our service!")
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.author.send(embed=embed)
        await ctx.send(
            f"✅ {ctx.author.mention}, the result for **{service.capitalize()}** has been sent to your DMs!"
        )

    except requests.exceptions.RequestException:
        # Handle connection errors
        embed = discord.Embed(
            title="Service Error",
            description=
            "We couldn't retrieve the requested data. Please try again later.",
            color=discord.Color.red())
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.send(embed=embed)


# /stock command to list available services
@bot.command(name="stock")
async def stock(ctx):
    embed = discord.Embed(
        title="Available Services",
        description=
        "Here are the services you can use with the `!generate` command:",
        color=discord.Color.blue())
    for service in SERVICES.keys():
        embed.add_field(name=service.capitalize(),
                        value=f"`{service}`",
                        inline=False)
    embed.set_image(url=IMAGE_URL)  # Add the image to the embed
    await ctx.send(embed=embed)


# Event to handle cooldown errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Cooldown",
            description=
            f"You need to wait {int(error.retry_after)} seconds before using this command again.",
            color=discord.Color.orange())
        embed.set_image(url=IMAGE_URL)  # Add the image to the embed
        await ctx.send(embed=embed)


# Run the bot
bot.run(TOKEN)
