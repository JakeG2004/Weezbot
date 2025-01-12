# WeezBot for Discord

## What does Weezbot do?
Weezbot is a discord bot that will keep track of your spotify playback, and notify you when things go wrong. It has support for notifications when:
* Spotify is closed
* Spotify is paused
* Spotify is not playing the desired song

# How to use weezbot?
1) Setup a [Discord Bot](https://discord.com/developers/applications)
2) Set up a [spotify App](https://developer.spotify.com/dashboard)
3) From the Spotify bot, get the Client ID, Client Secret, and Redirect URI
4) From the Discord bot, get the bot Token and your Discord user ID
5) Put them into a .env file in the same directory as the weezbot.py file, as so
```
SP_CLIENT_ID=<YOUR SPOTIFY CLIENT ID>
SP_CLIENT_SECRET=<YOUR SPOTIFY CLIENT SECRET>
SP_REDIRECT_URI=http://localhost/callback #(this works for everyone)
DISCORD_TOKEN=<YOUR DISCORD TOKEN>
USER_ID=<YOUR DISCORD USER ID>
```
6) Ensure that the discord bot is in a shared server with you, and that direct messages from users in that server are allowd in your Discord profile
7) Run the Python Script
8) Upon first launch, you will be asked to open a link in your browser. This for Spotify Authentication. Open the link when asked, then copy it and paste it into the terminal of the running python script. The bot should now be functional.
