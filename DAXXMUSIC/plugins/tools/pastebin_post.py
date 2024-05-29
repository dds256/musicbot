import aiohttp
from aiohttp import ContentTypeError
from pyrogram import filters
from DAXXMUSIC import app as app
import random
import string

# PasteBin API details
PASTEBIN_API_KEY = 'e-zy2euWaViTYmi61-KVxPh_KVVvacUP'
PASTEBIN_API_URL = 'https://pastebin.com/api/api_post.php'

async def upload_to_pastebin(content, title=None, visibility=None, expiration=None, format=None):
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': content
    }
    if title:
        data['api_paste_name'] = title
    if visibility:
        data['api_paste_private'] = visibility
    if expiration:
        data['api_paste_expire_date'] = expiration
    if format:
        data['api_paste_format'] = format

    async with aiohttp.ClientSession() as session:
        async with session.post(PASTEBIN_API_URL, data=data) as response:
            if response.status != 200:
                return False, f"HTTP Error: {response.status}"
            return True, await response.text()

async def handle_upload_command(bot, message):
    args = message.command[1:]

    # Set default values
    title = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generate a random title
    visibility = "1"  # Public visibility
    expiration = None  # No expiry
    format = None
    content = None

    # Parse command arguments
    for arg in args:
        if arg.startswith("title="):
            title = arg.split("=", 1)[1]
        elif arg.startswith("visibility="):
            visibility = arg.split("=", 1)[1]
        elif arg.startswith("expiration="):
            expiration = arg.split("=", 1)[1]
        elif arg.startswith("format="):
            format = arg.split("=", 1)[1]
        else:
            content = arg

    # Check for content
    if not content:
        replied = message.reply_to_message
        if not replied or not replied.text:
            return await message.reply("Please provide text to upload, or specify a title and content.")
        content = replied.text

    upload_msg = await message.reply("Processing...")

    success, result = await upload_to_pastebin(content, title, visibility, expiration, format)
    if not success:
        return await upload_msg.edit(f"Upload failed: {result}")
    
    await message.reply_text(f"Here is your raw link: {result}")
    await upload_msg.delete()

@app.on_message(filters.command("pastebin"))
async def upload_pastebin(bot, message):
    await handle_upload_command(bot, message)
