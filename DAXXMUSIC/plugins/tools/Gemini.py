import time
import requests
from DAXXMUSIC import app

from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Directly define your API key here
GEMINI_API_KEY = 'AIzaSyCOAdQBvciV1xTqOwGF4wZhPzIhdleBN2g'

# Define a function to call the Gemini API
def call_gemini_api(question):
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',  # Use the API key here
        'Content-Type': 'application/json'
    }
    payload = {
        'question': question
    }
    response = requests.post('https://gemini.api.endpoint/answer', headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if 'answer' in data:
            return data['answer']
    return None

@app.on_message(filters.command(["gemi"], prefixes=["+", ".", "/", "-", "", "$", "#", "&"]))
async def gemini_feature(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "Example:\n\n/gemi Where is the India?"
            )
            return

        query = message.text.split(' ', 1)[1]
        response = call_gemini_api(query)

        if response:
            end_time = time.time()
            telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
            await message.reply_text(
                f"{response}    \n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ➛ Gemini",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("The Gemini service failed to respond.")
    except Exception as e:
        await message.reply_text(f"**á´‡Ê€Ê€á´Ê€: {e} ")
