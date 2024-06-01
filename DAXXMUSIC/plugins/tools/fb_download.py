import subprocess
import os
from pyrogram import filters
from DAXXMUSIC import app

# Function to download Facebook video using yt-dlp
async def download_facebook_video(link):
    try:
        output_path = "/tmp"
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'quiet': True
        }
        
        # Run yt-dlp to download the video
        process = subprocess.run(
            ['yt-dlp', '-f', 'best', '-o', output_template, link],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            return None

        # Get the downloaded video file path
        for file in os.listdir(output_path):
            if file.endswith(".mp4"):
                return os.path.join(output_path, file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Improved regex to match various Facebook video URLs
FACEBOOK_VIDEO_REGEX = r'^(https?:\/\/)?(www\.)?(facebook\.com\/(?:[^\/]+\/)?(?:reel|watch|video|videos|story\.php\?story_fbid=))[^\s]+'

@app.on_message(filters.command("fbdownload") | filters.regex(FACEBOOK_VIDEO_REGEX))
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
        video_path = await download_facebook_video(link)
        
        if not video_path:
            await processing_message.edit("Failed to download Facebook video. Please ensure the link is valid.")
            return
        
        # Mention the user who requested the video in the caption
        caption = f"{message.from_user.mention}, here's your Facebook video."
        
        # Send the video with the caption
        await bot.send_video(message.chat.id, video_path, caption=caption)
        
        # Delete the progress message after sending the video
        await processing_message.delete()
        
        # Clean up the downloaded video file
        os.remove(video_path)
    except IndexError:
        await message.reply("Please provide a valid Facebook video link.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        
