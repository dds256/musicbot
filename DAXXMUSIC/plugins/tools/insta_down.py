import requests
from DAXXMUSIC import app
from pyrogram import filters
import asyncio
import re
from bs4 import BeautifulSoup
import wget

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

async def download(client, event) -> bool:
    link = event.message.text.split(" ", 1)[1]  # Extract the link from the command

    start_message = await event.respond("Processing Your insta link ....")
    try:
        url = link.replace("instagram.com", "ddinstagram.com").replace("==", "%3D%3D")
        await client.send_file(event.chat_id, url[:-1] if url.endswith("=") else url[:],
                               caption="Here's your Instagram content")
        return True
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

async def download_reel(client, event, link):
    try:
        meta_tag = await get_meta_tag(link)
        content_value = f"https://ddinstagram.com{meta_tag['content']}"
    except Exception as e:
        print(f"Error downloading reel: {e}")
        return None

    if content_value:
        await send_file(client, event, content_value)
    else:
        print("No content value found for reel")
        return None

async def download_post(client, event, link):
    meta_tags = await search_saveig(link)
    if meta_tags:
        for meta in meta_tags[:-1]:
            await asyncio.sleep(1)
            await send_file(client, event, meta)
    else:
        print("No meta tags found for post")
        return None

async def download_story(client, event, link):
    meta_tag = await search_saveig(link)
    if meta_tag:
        await send_file(client, event, meta_tag[0])
    else:
        print("No meta tag found for story")
        return None

async def get_meta_tag(link):
    getdata = requests.get(link).text
    soup = BeautifulSoup(getdata, 'html.parser')
    return soup.find('meta', attrs={'property': 'og:video'})

async def search_saveig(link):
    meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"},
                             headers=headers)
    if meta_tag.ok:
        res = meta_tag.json()
        return re.findall(r'href="(https?://[^"]+)"', res['data'])
    return None

async def send_file(client, event, content_value):
    try:
        await client.send_file(event.chat_id, content_value, caption="Here's your Instagram content")
    except Exception as e:
        print(f"Error sending file: {e}")
        return None

@app.on_message(filters.command("instadownload"))
async def handle_insta_download(client, message):
    await download(client, message)
    
