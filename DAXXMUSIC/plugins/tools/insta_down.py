import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import requests

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        data = response.json()
        video_url = data.get("data")
        return video_url
    return None

@app.on_message(filters.command("instadownload"))
async def instadownload_command(bot, message):
    user = message.from_user
    processing_message = await message.reply("Processing your Instagram video link...")
    
    try:
        link = message.text.split(" ")[1]
        video_url = await download_instagram_video(link)
        if not video_url:
            await processing_message.edit("Failed to download Instagram video. Please ensure the link is valid.")
            return
        
        await bot.send_video(message.chat.id, video_url, caption="Here's your Instagram video.")
        await processing_message.delete()
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
        
