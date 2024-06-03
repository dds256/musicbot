from pyrogram import Client, filters
from DAXXMUSIC import app
from config import OWNER_ID, BOT_USERNAME
from pyrogram.types import Message

# Dictionary to map original message IDs to copied message details
message_map = {}

@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def post_message(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply("Usage: /post \"message\" \"group_id\"")
        return
    
    # Extract the message and destination group ID from the command arguments
    try:
        post_message = message.command[1]
        destination_group_id = int(message.command[2])
    except (IndexError, ValueError):
        await message.reply("Invalid format. Usage: /post \"message\" \"group_id\"")
        return
    
    # Send the message to the destination group
    copied_message = await client.send_message(destination_group_id, post_message)
    
    # Map the original message ID to the copied message ID
    message_map[copied_message.message_id] = {
        "original_chat_id": message.chat.id,
        "original_message_id": message.message_id,
        "destination_chat_id": destination_group_id,
    }

    await message.reply("Post successfully done.")

# Handler for replies to the bot's messages
@app.on_message(filters.reply)
async def handle_replies(client: Client, message: Message):
    # Check if the replied message is in our map
    reply_details = message_map.get(message.reply_to_message.message_id)
    if reply_details:
        original_chat_id = reply_details["original_chat_id"]
        original_message_id = reply_details["original_message_id"]

        # Forward or handle the reply as needed
        await app.send_message(
            chat_id=original_chat_id,
            text=f"You have a reply to your message: {message.text}",
            reply_to_message_id=original_message_id
        )

        # Optionally, store the reply for further handling
        message_map[message.message_id] = {
            "original_chat_id": message.chat.id,
            "original_message_id": message.message_id,
            "destination_chat_id": original_chat_id,
        }

@app.on_message(filters.command(["reply"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def reply_to_message(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply("Usage: /reply \"message_id\" \"reply_text\"")
        return
    
    try:
        original_message_id = int(message.command[1])
        reply_text = " ".join(message.command[2:])
    except (IndexError, ValueError):
        await message.reply("Invalid format. Usage: /reply \"message_id\" \"reply_text\"")
        return

    # Find the original message details
    original_message_details = message_map.get(original_message_id)
    if original_message_details:
        destination_chat_id = original_message_details["destination_chat_id"]
        
        # Send the reply to the original message
        await client.send_message(
            chat_id=destination_chat_id,
            text=reply_text,
            reply_to_message_id=original_message_id
        )

        await message.reply("Reply successfully sent.")
    else:
        await message.reply("Original message not found.")
