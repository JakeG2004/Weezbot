import os
from dotenv import load_dotenv
import time
import asyncio

import discord

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

SLEEP_TIME = 10

# Load .env file
load_dotenv()

# Spotify credentials
SP_CLIENT_ID = os.getenv('SP_CLIENT_ID')
SP_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
SP_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')

# Discord credentials
DS_TOKEN = os.getenv('DISCORD_TOKEN')
DS_CHANNEL_ID = os.getenv('CHANNEL_ID')
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
user = None

async def CheckPlayback():
    isWeezing = True
    isPaused = True
    isSpotifyOn = True

    while True:
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
            await asyncio.sleep(SLEEP_TIME)
            continue

        try:
            # Extract playback details
            curPlayingName = playback['item']['name']
            isPlaying = playback['is_playing']

            # Handle whether or not it is paused
            if not isPlaying and not isPaused:
                await user.send("Spotify is paused!")
                isPaused = True
                print("Playback is paused...")

            elif isPlaying and isPaused:
                isPaused = False
                print("Playback resumed")

            # Handle switch from weezing to not weezing
            if curPlayingName != SP_DESIRED_SONG_NAME and isWeezing:
                await user.send(f"{SP_DESIRED_SONG_NAME} not playing!")
                isWeezing = False
                print("Weezing halted. Notifying...")

            # Continued not weezing
            elif curPlayingName != SP_DESIRED_SONG_NAME and not isWeezing:
                print("Weezing halted. Notf already sent...")

            # Switch back to weezing
            elif curPlayingName == SP_DESIRED_SONG_NAME and not isWeezing:
                isWeezing = True
                print("Weezing resumed...")

            # Weezing as normal 
            elif curPlayingName == SP_DESIRED_SONG_NAME:
                isWeezing = True
                #print("Weezing...")

        except Exception as e:
            print(f"ERROR! {e}")

        # Wait before looping
        await asyncio.sleep(SLEEP_TIME)


@client.event
async def on_ready():
    global user
    print("Discord logged in!")
    user = await client.fetch_user(DS_USER_ID)
    await user.send("Weezbot online!")
    await CheckPlayback()

client.run(DS_TOKEN)