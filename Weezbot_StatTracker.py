import os
from dotenv import load_dotenv
import time
import asyncio

import json

import discord

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load .env file
load_dotenv()

# Spotify credentials
SP_CLIENT_ID = os.getenv('SP_CLIENT_ID')
SP_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
SP_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')

# Discord credentials
DS_TOKEN = os.getenv('DISCORD_TOKEN')
DS_USER_ID = os.getenv('USER_ID')

# Setup spotify auth
sp_OAuth = SpotifyOAuth(
    client_id = SP_CLIENT_ID,
    client_secret = SP_CLIENT_SECRET,
    redirect_uri = SP_REDIRECT_URI,
    scope="user-read-playback-state"
)

# Create Spotify client
spotify = Spotify(auth_manager=sp_OAuth)
if(spotify):
    print("Spotify logged in!")
else:
    print("Failed to log in spotify!")
    quit()

# DESIRED SONG
SP_DESIRED_SONG_NAME = "Say It Ain't So"

# Create Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# GLOBAL VARS
user = None
SLEEP_TIME = 15
STATS_FILE = "listening_stats.json"

# Load stats to modify
def LoadStats():
    try:
        with open(STATS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Create the file with default values if not found
        return {"ads_time_seconds": 0, "song_time_seconds": 0}

# Write stats to file
def SaveStats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)

# Checks playback status, sends notifications accordingly
async def CheckPlayback():
    isWeezing = True
    isPaused = True
    isSpotifyOn = True
    stats = LoadStats()

    while True:
        # Get time
        start_time = time.time()

        # Get Current Playback
        playback = spotify.current_playback()

        # No active playback (e.g., device off or Spotify not playing anything)
        if playback is None and isSpotifyOn:
            print("No active playback detected. Spotify device might be off.")
            await user.send("No spotify playback!")
            isSpotifyOn = False
            await asyncio.sleep(SLEEP_TIME)
            continue

        elif playback is None and not isSpotifyOn:
            print("No active playback detected. Notification already sent...")
            await asyncio.sleep(SLEEP_TIME)
            continue

        isSpotifyOn = True

        # Ad is playing
        if playback['item'] is None:
            print("Ad is playing. Cannot retrieve song information.")
            stats['ads_time_seconds'] += SLEEP_TIME
            SaveStats(stats)
            await asyncio.sleep(SLEEP_TIME)
            continue

        try:
            # Get playback info
            curPlayingName = playback['item']['name']
            isPlaying = playback['is_playing']

            # Song is playing, save stats
            if isPlaying and curPlayingName == SP_DESIRED_SONG_NAME:
                stats['song_time_seconds'] += SLEEP_TIME
                SaveStats(stats)

            # Song is paused
            if not isPlaying and not isPaused:
                await user.send("Spotify is paused!")
                isPaused = True

            elif isPlaying and isPaused:
                isPaused = False

            # Desired song is not current song
            if curPlayingName != SP_DESIRED_SONG_NAME and isWeezing:
                await user.send(f"{SP_DESIRED_SONG_NAME} not playing!")
                isWeezing = False

            elif curPlayingName == SP_DESIRED_SONG_NAME and not isWeezing:
                isWeezing = True

        except Exception as e:
            print(f"ERROR! {e}")

        # Wait correct amount of time
        elapsed_time = time.time() - start_time
        await asyncio.sleep(max(0, SLEEP_TIME - elapsed_time))


@client.event
async def on_ready():
    global user
    print("Discord logged in!")
    user = await client.fetch_user(DS_USER_ID)
    await user.send("Weezbot online! Send `!stats` here to check listening stats.")
    await CheckPlayback()

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message is sent in a DM
    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == "!stats":
            stats = LoadStats()
            ads_time = stats["ads_time_seconds"]
            song_time = stats["song_time_seconds"]
            await message.channel.send(
                f"Ad Listening Time: {ads_time // 60} minutes {ads_time % 60} seconds\n"
                f"{SP_DESIRED_SONG_NAME} Listening Time: {song_time // 60} minutes {song_time % 60} seconds"
            )
        else:
            await message.channel.send("I don't recognize that command. Try `!stats`.")

    # If the message is not a DM, ignore or handle other cases as needed


client.run(DS_TOKEN)