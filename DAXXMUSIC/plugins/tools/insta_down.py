import aiohttp
from pyrogram import filters
from DAXXMUSIC import app as app

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

# Function to download Instagram video using SaveIG
async def download_instagram_video(link):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://saveig.app/api/ajaxSearch", headers=headers, data={"q": link, "t": "media", "lang": "en"}) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    print(f"Response JSON: {data}")  # Debugging line
                    if 'data' in data and 'url' in data['data'][0]:
                        video_url = data['data'][0]['url']
                        return video_url
                except Exception as e:
                    print(f"Error parsing JSON response: {str(e)}")
            else:
                print(f"Error: Received response with status code {response.status}")
    return None

@app.on_message(filters.command("instadownload"))
async def instadownload_command(bot, message):
    user = message.from_user
    processing_message = await message.reply("Processing your Instagram video link...")

    try:
        link = message.text.split(" ")[1]
        video_url = await download_instagram_video(link)
        if not video_url:
            await processing_message.edit("Failed to download Instagram video. Please ensure the link is valid.")
            return

        try:
            await bot.send_video(message.chat.id, video_url, caption="Here's your Instagram video.")
            await processing_message.delete()
        except Exception as send_error:
            await processing_message.edit(f"Failed to send Instagram video: {str(send_error)}")
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
