from pyrogram import Client, filters
from DAXXMUSIC import app
from config import OWNER_ID
from pyrogram.types import Message

@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(_, message: Message):
    # Extract the command and arguments
    command_parts = message.text.split()

    if len(command_parts) < 2:
        await message.reply("Please specify a destination group/user ID.")
        return

    destination_path = command_parts[1]

    # Check if the path includes a message ID
    if "/" in destination_path:
        try:
            # Split the path into destination ID and message ID
            destination_id, message_id = destination_path.split("/")
            message_id = int(message_id)
        except ValueError:
            await message.reply("Invalid format. Use @username/message_id or -100xxxxxxxxxx/message_id.")
            return
    else:
        destination_id = destination_path
        message_id = None

    # Check if the message is a reply to another message
    if message.reply_to_message:
        try:
            if message_id:
                # Fetch the target message to reply to
                target_message = await app.get_messages(destination_id, message_id)
                # Reply to the target message
                await message.reply_to_message.copy(destination_id, reply_to_message_id=target_message.message_id)
            else:
                # Forward the replied-to message to the specified destination
                await message.reply_to_message.copy(destination_id)
            await message.reply("Post successful.")
        except Exception as e:
            await message.reply(f"Failed to post: {str(e)}")
    else:
        if message_id:
            await message.reply("Please reply to a message to post it to a specific message.")
        else:
            # Use the remaining command parts as the message text
            message_text = " ".join(command_parts[2:])
            if not message_text:
                await message.reply("Please provide a message to post.")
                return
            try:
                # Send the message to the specified destination
                await app.send_message(destination_id, message_text)
                await message.reply("Post successful.")
            except Exception as e:
                await message.reply(f"Failed to post: {str(e)}")
