import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app

# Function to get a random joke
async def get_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Any") as response:
            if response.status == 200:
                return await response.json()
            return None

@app.on_message(filters.command("joke"))
async def joke_command(bot, message):
    processing_message = await message.reply("Fetching a joke...")
    try:
        joke_data = await get_joke()
        if not joke_data:
            await processing_message.edit("Failed to get a joke. Please try again later.")
            return
        
        joke = joke_data.get("joke") if "joke" in joke_data else f"{joke_data.get('setup')} - {joke_data.get('delivery')}"
        await processing_message.edit(joke)
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
