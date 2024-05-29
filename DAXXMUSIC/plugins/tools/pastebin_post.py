import aiohttp
from aiohttp import ContentTypeError
from pyrogram import filters
from DAXXMUSIC import app as app

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
            paste_url = await response.text()
            paste_id = paste_url.split('/')[-1]
            return True, f"https://pastebin.com/raw/{paste_id}"

async def handle_upload_command(bot, message):
    # Prompt user for the title
    title_msg = await message.reply("Please enter a title for the paste.")

    # Wait for the user's response
    title_response = await app.ask(message.chat.id, "Enter a title:", filters=filters.text)

    # Extract title from user's response
    title = title_response.text

    # Check for content
    if not title:
        await title_msg.edit("Title cannot be empty.")
        return

    # Prompt user for content
    content_msg = await message.reply("Please enter the text content to upload.")

    # Wait for the user's response
    content_response = await app.ask(message.chat.id, "Enter the text content:", filters=filters.text)

    # Extract content from user's response
    content = content_response.text

    # Check for content
    if not content:
        await content_msg.edit("Content cannot be empty.")
        return

    # Upload to Pastebin
    await title_msg.edit("Posting...")
    success, result = await upload_to_pastebin(content, title)

    if not success:
        await title_msg.edit(f"Upload failed: {result}")
        return

    await title_msg.edit("Getting raw link...")
    await message.reply_text(f"Here is your raw link: {result}")

@app.on_message(filters.command("pastebin"))
async def upload_pastebin(bot, message):
    await handle_upload_command(bot, message)
