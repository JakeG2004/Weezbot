from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
import os

# Load .env file
load_dotenv()

# Get the spotify credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Setup authentication
sp_OAuth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state"
)

# Create the spotify client
spotify = Spotify(auth_manager=sp_OAuth)

def CheckPlayback():
    while True:
        # Get Current Playback
        playback = spotify.current_playback()

        # Must be in try because current playback returns None when ad is playing
        try:
            curPlayingName = playback['item']['name']
            if(curPlayingName != "Say It Ain't So"):
                print("ALER!!!!")
            else:
                print("YAY!")
        # Catch ads
        except:
            print("ERROR CHECKING!")

        # Wait before looping
        time.sleep(10)

CheckPlayback()