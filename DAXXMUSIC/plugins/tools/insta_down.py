import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import requests

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        content_type = response.headers.get('content-type')
        if content_type == 'application/json':
            data = response.json()
            video_url = data.get("data")
            return video_url
        else:
            return None  # Handle unexpected content type
    return None

@app.on_message(filters.command("instadownload"))
async def handle_instagram_download(bot, message):
    user = message.from_user
    link = message.text.split(" ", 1)[1]

    processing_message = await message.reply("Processing your Instagram link...")

    try:
        video_url = await download_instagram_video(link)
        if video_url:
            await bot.send_video(message.chat.id, video_url)
            await processing_message.delete()
        else:
            await processing_message.edit("Failed to download the Instagram video.")
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
        
