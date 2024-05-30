import os
import subprocess
from pyrogram import filters
from DAXXMUSIC import app as app

# Function to extract APK info
def extract_apk_info(apk_path):
    try:
        result = subprocess.run(['aapt', 'dump', 'badging', apk_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Handler for receiving APK files
@app.on_message(filters.document.mime_type("application/vnd.android.package-archive"))
async def handle_apk_file(bot, message):
    # Download the APK file
    apk_file = await message.download()
    apk_info = extract_apk_info(apk_file)
    
    # Clean up downloaded APK file
    os.remove(apk_file)
    
    # Format and send the APK info as a message
    formatted_info = format_apk_info(apk_info)
    await message.reply(formatted_info, parse_mode="markdown")

# Function to format APK info with titles
def format_apk_info(apk_info):
    # Split the output into lines
    lines = apk_info.split('\n')
    
    # Create a dictionary to store formatted information
    formatted_info = {}
    
    # Iterate over each line and extract key-value pairs
    for line in lines:
        # Split the line into key and value (if possible)
        parts = line.split(":")
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            # Add the key-value pair to the dictionary
            formatted_info[key] = value
    
    # Format the information with titles
    formatted_text = ""
    for key, value in formatted_info.items():
        formatted_text += f"*{key}:* `{value}`\n"
    
    return formatted_text

# Handler for the /apkinfo command to be used in reply to an APK file
@app.on_message(filters.command("apkinfo") & filters.reply)
async def apk_info_command(bot, message):
    if message.reply_to_message and message.reply_to_message.document:
        apk_file = await message.reply_to_message.download()
        apk_info = extract_apk_info(apk_file)
        
        # Clean up downloaded APK file
        os.remove(apk_file)
        
        # Format and send the APK info as a message
        formatted_info = format_apk_info(apk_info)
        await message.reply(formatted_info, parse_mode="markdown")
    else:
        await message.reply("Please reply to an APK file to extract its info.")