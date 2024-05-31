import os
from pyrogram import filters
from DAXXMUSIC import app
from config import OWNER_ID

# Function to send voice message
async def send_voice_message(message, audio_file_path):
    try:
        # Send processing message
        await message.reply_chat_action("record_audio")
        
        # Send voice message
        await app.send_voice(message.chat.id, audio_file_path)
        
        # Delete downloaded audio file
        os.remove(audio_file_path)
    except Exception as e:
        print("Failed to send voice message:", e)

# Function to handle received audio message
async def handle_audio_message(message):
    try:
        # Download audio file
        audio_file_id = message.reply_to_message.audio.file_id
        audio_file_path = await app.download_media(audio_file_id)
        if audio_file_path:
            # Send processing message
            processing_message = await message.reply_text("Processing audio...")
            
            # Send voice message
            await send_voice_message(message, audio_file_path)
            
            # Delete processing message
            await processing_message.delete()
        else:
            await message.reply_text("Failed to download audio file")
    except Exception as e:
        await message.reply_text("An error occurred while processing the audio: {}".format(e))

# Command handler for audio to voice message
@app.on_message(filters.command("voice", prefixes="/") & filters.reply)
async def audio_to_voice(_, message):
    if message.reply_to_message and message.reply_to_message.audio:
        await handle_audio_message(message)
    else:
        await message.reply_text("Please reply to an audio message with /voice to send it as a voice message.")
