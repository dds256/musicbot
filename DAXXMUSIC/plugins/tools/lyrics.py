import requests
from pyrogram import filters
from DAXXMUSIC import app as app

# Lyrics.ovh API base URL
LYRICS_OVH_API_URL = "https://api.lyrics.ovh/v1"

# Command to fetch lyrics for a song
@app.on_message(filters.command("lyrics"))
async def fetch_lyrics(bot, message):
    args = message.command[1:]
    if not args:
        await message.reply("Please provide the name of the song after command. example /lyrics aaj phir tumpe pyar aaya hai")
        return

    query = " ".join(args)
    progress_message = await message.reply("Fetching lyrics...")

    response = requests.get(f"{LYRICS_OVH_API_URL}/{query}")
    if response.status_code == 200:
        data = response.json()
        lyrics = data.get("lyrics")
        if lyrics:
            await message.reply(f"Lyrics for {query}:\n\n```{lyrics}```", disable_web_page_preview=True)
            await progress_message.delete()  # Delete progress message
            await message.delete()  # Delete the command message
        else:
            await progress_message.edit("Sorry, lyrics not found for this song.")
    else:
        await progress_message.edit("Sorry, song not found or lyrics unavailable.")
