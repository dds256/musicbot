import aiohttp
from aiohttp import ContentTypeError
from pyrogram import filters
from DAXXMUSIC import app as app
import json

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

    content = None

    # Check if the command has arguments
    if not args:
        # Check if there's a reply
        replied = message.reply_to_message
        if replied and replied.text:
            content = replied.text
        else:
            content = message.text
    else:
        content = ' '.join(args)

    upload_msg = await message.reply("Processing...")

    success, result = await upload_to_pastebin(content)
    if not success:
        return await upload_msg.edit(f"Upload failed: {result}")

    await message.reply_text(f"Here is your raw link: {result}")
    await upload_msg.delete()

@app.on_message(filters.command("pastebin"))
async def upload_pastebin(bot, message):
    await handle_upload_command(bot, message)
