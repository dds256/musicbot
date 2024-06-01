import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import requests
import os

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        data = response.json()
        video_url = data.get("data")
        return video_url
    return None

# Function to download video and send as response
async def send_video_response(chat_id, video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status == 200:
                filename = "instagram_video.mp4"
                with open(filename, "wb") as f:
                    f.write(await response.read())
                await app.send_video(chat_id, video=filename, caption="Here's your Instagram video.")
                os.remove(filename)

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
        
        await send_video_response(message.chat.id, video_url)
        await processing_message.delete()
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
        
