import requests
from pyrogram import filters
from DAXXMUSIC import app as app

# Function to fetch country information from REST Countries API
def get_country_info(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data[0]  # Assuming the API returns data for the first matching country
    except requests.RequestException as e:
        print(f"Error fetching country information: {e}")
        return None

# Command to retrieve country information
@app.on_message(filters.command("country"))
async def country_info_command(bot, message):
    try:
        # Extract country name from command
        country_name = message.text.split(maxsplit=1)[1].strip().lower()

        # Fetch country information from API
        country_data = get_country_info(country_name)
        if country_data:
            # Format and send country information as a message
            info_message = f"Country: {country_data['name']['common']}\n" \
                           f"Capital: {country_data['capital'][0]}\n" \
                           f"Population: {country_data['population']}\n" \
                           f"Region: {country_data['region']}\n" \
                           f"Languages: {', '.join(country_data['languages'].keys())}"
            await message.reply(info_message)
        else:
            await message.reply("Country information not found.")
    except IndexError:
        await message.reply("Please specify a country name.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")