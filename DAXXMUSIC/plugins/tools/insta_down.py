import requests
from pyrogram import filters
from DAXXMUSIC import app
from bs4 import BeautifulSoup

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    response = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
    if response.ok:
        data = response.json()
        html_content = data.get("data")
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            download_link = soup.find('a', {'title': 'Download Video'})
            if download_link:
                return download_link['href']
    return None

@app.on_message(filters.command("instadownload") | filters.regex(r'^https?:\/\/(?:www\.)?instagram\.com\/p\/[\w\-]+\/?$'))
async def instadownload_command(bot, message):
    user = message.from_user
    link = None
    if message.reply_to_message:
        replied_message = message.reply_to_message
        if replied_message.text:
            link = replied_message.text.strip()
    if not link:
        try:
            link = message.text.split(" ")[1]
        except IndexError:
            await message.reply("Please provide a valid Instagram video link.")
            return

    processing_message = await message.reply(f"Downloading Instagram video from...\n\nLink: {link}")
    
    try:
        video_url = await download_instagram_video(link)
        if not video_url:
            await processing_message.edit("Failed to download Instagram video. Please ensure the link is valid.")
            return
        
        try:
            sent_message = await bot.send_video(message.chat.id, video_url, caption=f"{user.mention}, Here's your Instagram video.\n Downloaded from: {link}")
            await bot.delete_messages(message.chat.id, message.message_id)
            await processing_message.delete()
            await sent_message.edit_caption(f"Here's your Instagram video from {user.mention}: {link}")
        except Exception as send_error:
            await processing_message.edit(f"Failed to send Instagram video: {str(send_error)}")
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
        
