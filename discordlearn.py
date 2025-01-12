import discord
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Discord credentials
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
USER_ID = os.getenv('USER_ID')

# Init bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Logged in")
    user = await client.fetch_user(USER_ID)
    await user.send("Hello there!")

@client.event
async def on_message(message):
    if(message.author == clientuser):
        return
    
    if(message.content.startswith('$hello')):
        await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)