import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app
import os
from bs4 import BeautifulSoup

# Function to extract Instagram video URL from HTML
async def extract_instagram_video_url(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                video_tag = soup.find('meta', property='og:video')
                if video_tag:
                    video_url = video_tag['content']
                    return video_url
    return None

@app.on_message(filters.command("instadownload"))
async def instadownload_command(bot, message):
    user = message.from_user
    processing_message = await message.reply("Processing your Instagram video link...")
    
    try:
        link = message.text.split(" ")[1]
        video_url = await extract_instagram_video_url(link)
        if not video_url:
            await processing_message.edit("Failed to extract Instagram video URL. Please ensure the link is valid.")
            return
        
        file_name = "instagram_video.mp4"  # You can modify the file name as needed
        file_path = os.path.join("downloads", file_name)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as resp:
                if resp.status == 200:
                    with open(file_path, 'wb') as f:
                        f.write(await resp.read())
                    
                    await bot.send_video(message.chat.id, file_path, caption="Here's your Instagram video.")
                    await processing_message.delete()
                else:
                    await processing_message.edit("Failed to download Instagram video.")
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
