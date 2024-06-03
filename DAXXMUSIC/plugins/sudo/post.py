from pyrogram import Client, filters
from DAXXMUSIC import app
from config import OWNER_ID, BOT_USERNAME
from pyrogram.types import Message

# Dictionary to map original message IDs to copied message IDs
message_map = {}

@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(client: Client, message: Message):
    if message.reply_to_message:
        destination_group_id = -1001927107785

        # Copy the message and get the message ID of the copied message
        copied_message = await message.reply_to_message.copy(destination_group_id)
        
        # Map the original message ID to the copied message ID
        message_map[message.reply_to_message.message_id] = copied_message.message_id

        await message.reply("ᴘᴏsᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴏɴᴇ")

# Handler for replies to the bot's messages
@app.on_message(filters.reply & filters.chat(destination_group_id))
async def handle_replies(client: Client, message: Message):
    original_message_id = message_map.get(message.reply_to_message.message_id)
    if original_message_id:
        # Forward or handle the reply as needed
        await app.send_message(
            chat_id=message.from_user.id,
            text=f"You have a reply to your message: {message.text}"
        )
