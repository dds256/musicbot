import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import requests
import os
from bs4 import BeautifulSoup

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video')
        if video_tag:
            video_url = video_tag['src']
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
        
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as resp:
                if resp.status == 200:
                    file_name = "instagram_video.mp4"  # You can modify the file name as needed
                    file_path = os.path.join("downloads", file_name)
                    with open(file_path, 'wb') as f:
                        f.write(await resp.read())
                    
                    await bot.send_video(message.chat.id, file_path, caption="Here's your Instagram video.")
                    await processing_message.delete()
                else:
                    await processing_message.edit("Failed to download Instagram video.")
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
        
