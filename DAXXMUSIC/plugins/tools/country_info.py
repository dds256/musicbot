import requests
from pyrogram import filters
from DAXXMUSIC import app as app

# Function to fetch country information from REST Countries API
def get_country_info(query):
    try:
        # Determine if the query is a country code (usually 2-3 letters) or a country name
        if len(query) <= 3:
            url = f"https://restcountries.com/v3.1/alpha/{query}"
        else:
            url = f"https://restcountries.com/v3.1/name/{query}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching country information: {e}")
        return None

# Command to retrieve country information
@app.on_message(filters.command("country"))
async def country_info_command(bot, message):
    try:
        # Extract country name or code from command
        query = message.text.split(maxsplit=1)[1].strip().lower()

        # Send a "processing" message
        processing_message = await message.reply("Processing...")

        # Fetch country information from API
        country_data_list = get_country_info(query)
        if country_data_list:
            country_data = country_data_list[0]  # Assuming the first result is the most relevant
            # Format and send country information as a message
            info_message = f"**Country:** {country_data['name']['common']}\n" \
                           f"**Capital:** {country_data['capital'][0] if 'capital' in country_data else 'N/A'}\n" \
                           f"**Population:** {country_data['population']}\n" \
                           f"**Region:** {country_data['region']}\n" \
                           f"**Languages:** {', '.join(country_data['languages'].values()) if 'languages' in country_data else 'N/A'}"
            await processing_message.edit(info_message)
        else:
            await processing_message.edit("Country information not found.")
    except IndexError:
        await message.reply("Please specify a country name or code after the command, e.g., `/country India` or `/country IN`.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
