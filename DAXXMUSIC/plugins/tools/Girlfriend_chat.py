import random
import datetime 
from pyrogram import Client, filters
from DAXXMUSIC import app

# Initialize the bot with your credentials

# Predefined responses to simulate a conversation
responses = {
    "hello": ["Hi there!", "Hello! How's your day going?", "Hey, you!"],
    "how are you": ["I'm doing great, thanks for asking! How about you?", "I'm good! What about you?", "Feeling chatty! How are you?"],
    "what are you doing": ["Just chatting with you. What about you?", "Thinking about you!", "Waiting to hear from you!"],
    "i love you": ["Aww, that's sweet! I love you too!", "Love you more!", "You make me smile!"],
    "goodbye": ["Goodbye! Talk to you later!", "See you soon!", "Take care!"],
    "what's your name": ["I'm your virtual girlfriend, here to chat with you!", "You can call me your chat buddy!", "I'm here to keep you company!"],
    "default": ["Tell me more about that!", "That's interesting!", "I love hearing from you!"],
    "weather": ["I hope the weather is nice where you are!", "It looks like a beautiful day today!", "Stay cozy if it's cold out there!"],
    "favorite color": ["I love all the colors, but blue is special!", "Pink is lovely, don't you think?", "I like vibrant colors, they make me happy!"],
    "hobbies": ["I enjoy chatting with you, of course!", "I love learning new things!", "Listening to music is always fun!"],
    "time": ["It's {} right now.".format(datetime.datetime.now().strftime("%I:%M %p")), "The current time is {}.".format(datetime.datetime.now().strftime("%I:%M %p"))],
    "morning": ["Good morning! Have a fantastic day!", "Morning! Hope you slept well!", "Rise and shine!"],
    "afternoon": ["Good afternoon! How's your day going?", "Hey! Enjoying your afternoon?", "Afternoon! What's up?"],
    "evening": ["Good evening! How was your day?", "Evening! What are you up to?", "Relaxing evening, isn't it?"],
    "night": ["Good night! Sweet dreams!", "Nighty night! Rest well!", "Good night! Talk to you tomorrow!"],
    "playful": ["You're such a tease!", "Stop it, you naughty thing!", "You're making me blush!"],
    "flirty": ["You know how to make a girl smile!", "You're so charming!", "You're quite the flirt, aren't you?"],
}

# Function to generate a response based on the input message
def generate_response(message_text, username):
    # Convert the message to lowercase for case insensitive matching
    message_text = message_text.lower()

    # Time-based responses
    current_hour = datetime.datetime.now().hour
    if "good morning" in message_text and current_hour >= 12:
        return f"It's not morning, {username}, but good morning anyway!"
    elif "good afternoon" in message_text and current_hour >= 18:
        return f"It's not afternoon, {username}, but good afternoon anyway!"
    elif "good evening" in message_text and current_hour < 12:
        return f"It's not evening, {username}, but good evening anyway!"
    elif "good night" in message_text and current_hour < 18:
        return f"It's not night yet, {username}, but good night!"

    # Loop through the predefined responses to find a match
    for key in responses.keys():
        if key in message_text:
            return random.choice(responses[key])
    
    # Return a default response if no match is found, with personalization
    return random.choice(responses["default"]).replace("!", f", {username}!")

# Event handler for incoming messages
@app.on_message(filters.text)
async def chat_with_user(client, message):
    # Generate a response based on the user's message
    username = message.from_user.first_name
    response = generate_response(message.text, username)
    # Send the response to the user
    await message.reply(response)
