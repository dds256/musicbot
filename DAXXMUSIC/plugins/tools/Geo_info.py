import requests
from pyrogram import filters
from DAXXMUSIC import app as app

# Function to send GraphQL query to the API
def send_graphql_query(query, location):
    url = 'http://geodb-free-service.wirefreethought.com/graphql'
    headers = {'Content-Type': 'application/json'}
    data = {'query': query.format(location)}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Command to get information about a specific location
@app.on_message(filters.command(["geo_info"]))
async def get_geo_info_command(bot, message):
    args = message.command[1:]
    if not args:
        await message.reply("Please provide a location. For example: /geo_info London")
        return
    
    location = args[0]
    process_message = await message.reply("Finding information...")
    
    query = '''
    {{
      find(name:"{}") {{
        name
        type
        code
        population
        latitude
        longitude
        wikiDataId
      }}
    }}
    '''
    response = send_graphql_query(query, location)
    geo_data = response.get('data', {}).get('find')
    
    if geo_data:
        name = geo_data['name']
        location_type = geo_data['type']
        code = geo_data.get('code', '')
        population = geo_data.get('population', '')
        latitude = geo_data.get('latitude', '')
        longitude = geo_data.get('longitude', '')
        wiki_data_id = geo_data.get('wikiDataId', '')

        reply_text = f"Name: {name}\nType: {location_type}\nCode: {code}\nPopulation: {population}\nLatitude: {latitude}\nLongitude: {longitude}\nWikiData ID: {wiki_data_id}"
        await process_message.edit_text(reply_text)
    else:
        await process_message.edit_text("Location not found.")
