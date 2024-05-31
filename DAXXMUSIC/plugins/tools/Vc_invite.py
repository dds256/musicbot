from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app
from config import OWNER_ID

# Function to invite all members to a voice chat
async def invite_all_members(chat_id):
    members = await app.get_chat_members(chat_id)
    user_ids = [member.user.id for member in members if not member.user.is_bot]
    return await invite_to_vc(chat_id, user_ids)

# Function to invite specific members to a voice chat
async def invite_to_vc(chat_id, user_ids):
    text = "Invited user(s):"
    for user_id in user_ids:
        try:
            await app.add_chat_members(chat_id=chat_id, user_ids=user_id)
            text += f" {user_id}"
        except Exception as e:
            print(f"Error inviting user {user_id}: {e}")
    return text

# Command to invite specific users to a voice chat
@app.on_message(filters.command("invitevc", prefixes="/") & filters.user(OWNER_ID))
async def invite_vc_command(_, message):
    if len(message.command) < 2:
        await message.reply("Please provide user ID(s) to invite to the voice chat.")
        return
    chat_id = message.chat.id
    user_ids = message.command[1:]
    invite_text = await invite_to_vc(chat_id, user_ids)
    await message.reply_text(invite_text)

# Command to invite all members to a voice chat
@app.on_message(filters.command("inviteallvc", prefixes="/") & filters.user(OWNER_ID))
async def invite_all_vc_command(_, message):
    chat_id = message.chat.id
    await message.reply("Inviting all members to the voice chat...")
    invite_text = await invite_all_members(chat_id)
    await message.reply_text(invite_text)
