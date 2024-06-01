from pyrogram import filters
from DAXXMUSIC import app
from config import BANNED_USERS

# Define multiple prefixes for the delete command
DELETE_COMMAND_PREFIXES = ["/", "!", "-"]

# Command to delete a message
@app.on_message(
    filters.command(["delete"], prefixes=DELETE_COMMAND_PREFIXES) & filters.reply & ~BANNED_USERS
)
async def delete_message(bot, message):
    try:
        # Check if the user is the owner
        if message.from_user.id == OWNER_ID:
            # Delete the replied message
            await message.reply_to_message.delete()
            # Delete the command message
            await message.delete()
        else:
            await message.reply_text("You're not authorized to use this command LoL 😂..")
    except Exception as e:
        print("Error deleting message:", e)
