import discord
import dotenv
import os
from discord.ext import commands, tasks
from discord import app_commands
from bishoujoScrape import newFigs as nf
from datetime import datetime

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="#", intents=intents)


@bot.event
async def on_ready():
    print("Bot is running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e)


@bot.tree.command(name="setchannel")
@app_commands.describe(channelid="Channel ID for channel you want updates in.")
async def setchannel(interaction: discord.Interaction, channelid: str):
    await interaction.response.send_message(
        f"{bot.get_channel(int(channelid)).mention} will now be updated with new figure releases from amiami!"
    )

    await update_figs(channelID=channelid)


async def update_figs(channelID):
    embedGenerated = nf()
    channel = bot.get_channel(channelID)

    if embedGenerated != {}:
        embeds = [0 for i in embedGenerated]
        for i in embedGenerated:
            embeds[i] = discord.Embed.from_dict(
                embedGenerated[len(embedGenerated) - 1 - i]
            )
            await channel.send(embed=embeds[i])

    else:
        await channel.send("nothing new to display")


bot.run(TOKEN)
