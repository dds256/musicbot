import os
import shutil
from pydub import AudioSegment
from pyrogram import filters
from DAXXMUSIC import app
from config import OWNER_ID

# Function to send processing message
async def send_processing_message(chat_id):
    try:
        message = await app.send_message(chat_id, "Processing audio, please wait...")
        return message
    except Exception as e:
        print("Failed to send processing message:", e)

# Function to send voice message
async def send_voice_message(message, audio_file_path, processing_message):
    try:
        # Rename the audio file with the appropriate extension
        voice_file_path = audio_file_path + ".ogg"
        shutil.move(audio_file_path, voice_file_path)
        
        # Embed metadata to ensure waveform display
        audio = AudioSegment.from_file(voice_file_path, format="ogg")
        audio.export(voice_file_path, format="ogg", tags={'artist': 'Your Bot', 'title': 'Voice Message'})

        # Send voice message with the audio file
        await app.send_voice(
            chat_id=message.chat.id,
            voice=voice_file_path,
            caption="Voice Message",
            file_name="voice_message.ogg"  # Specify the file name for display in Telegram
        )

        # Delete processing message
        await processing_message.delete()

        # Delete downloaded audio file
        os.remove(voice_file_path)
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
            processing_message = await send_processing_message(message.chat.id)
            
            # Send voice message
            await send_voice_message(message, audio_file_path, processing_message)
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
