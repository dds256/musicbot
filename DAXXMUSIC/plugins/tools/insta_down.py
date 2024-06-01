import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import os

# Function to download Instagram video using RapidAPI
async def download_instagram_video(link):
    url = "https://instagram-video-or-images-downloader.p.rapidapi.com/dl"
    headers = {
        'x-rapidapi-key': '77dd9d1e3bms8',
        'x-rapidapi-host': 'instagram-video-or-images-downloader.p.rapidapi.com'
    }
    params = {
        'url': link
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                video_url = data.get("data").get("video_url")
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
        
