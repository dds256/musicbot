import requests
from pyrogram import filters
from DAXXMUSIC import app
from bs4 import BeautifulSoup

# Function to download Facebook video using fbdown.net
async def download_facebook_video(link):
    response = requests.get(f"https://fbdown.net/download.php?URL={link}")
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        video_element = soup.find('a', {'class': 'btn btn-download'})
        if video_element and 'href' in video_element.attrs:
            return video_element['href']
    return None

@app.on_message(filters.command("fbdownload") | filters.regex(r'^https?:\/\/(?:www\.)?facebook\.com\/.+\/videos\/.+\/?$'))
async def fbdownload_command(bot, message):
    try:
        link = None
        
        # Check if the message is a reply and contains a link
        if message.reply_to_message and message.reply_to_message.text:
            link = message.reply_to_message.text.strip()
            # Delete only the command message
            await message.delete()
            processing_message = await message.reply("Processing your Facebook video link...")
        else:
            # If not a reply, try to extract the link from the command message
            link = message.text.split(" ")[1]
            # Delete the command message
            await message.delete()
            # Send a progress message
            processing_message = await message.reply("Processing your Facebook video link...")
        
        # Download the Facebook video
        video_url = await download_facebook_video(link)
        
        if not video_url:
            await processing_message.edit("Failed to download Facebook video. Please ensure the link is valid.")
            return
        
        # Mention the user who requested the video in the caption
        caption = f"{message.from_user.mention}, Here's your Facebook video."
        
        # Send the video with the caption
        await bot.send_video(message.chat.id, video_url, caption=caption)
        
        # Delete the progress message after sending the video
        await processing_message.delete()
    except IndexError:
        await message.reply("Please provide a valid Facebook video link.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        
