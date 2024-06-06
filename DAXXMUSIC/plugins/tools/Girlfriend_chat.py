import random
import datetime
from pyrogram import Client, filters
from DAXXMUSIC import app
from collections import defaultdict
import time
import re

# Predefined responses to simulate a conversation
responses = {
    "hello": ["Hi there!", "Hello! How's your day going?", "Hey, you!"],
    "how are you": ["I'm doing great, thanks for asking! How about you?", "I'm good! What about you?", "Feeling chatty! How are you?"],
    "what are you doing": ["Just chatting with you. What about you?", "Thinking about you!", "Waiting to hear from you!"],
    "i love you": ["Aww, that's sweet! I love you too!", "Love you more!", "You make me smile!"],
    "goodbye": ["Goodbye! Talk to you later!", "See you soon!", "Take care!"],
    "what's your name": ["I'm your virtual girlfriend, here to chat with you!", "You can call me your chat buddy!", "I'm here to keep you company!"],
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
    "naughty": ["Oh, you're naughty!", "You cheeky thing!", "Behave yourself, you!"],
    "default": ["Tell me more about that!", "That's interesting!", "I love hearing from you!"],
}

# Improved dynamic responses
dynamic_responses = {
    "how are you": ["I'm great, thanks for asking! How about you?", "Doing well! What about yourself?", "Feeling awesome! How's your day going?"],
    "time": ["The current time is {}.".format(datetime.datetime.now().strftime("%I:%M %p"))],
}

# Context tracking (simple version)
user_context = defaultdict(lambda: {"last_message": "", "last_response_time": 0})

COOLDOWN_PERIOD = 5  # seconds

# Function to generate a response based on the input message
def generate_response(message_text, username):
    # Convert the message to lowercase for case-insensitive matching
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
        if re.search(r'\b' + re.escape(key) + r'\b', message_text):
            return random.choice(responses[key])

    # Return a default response if no match is found, with personalization
    return None

# Function to handle dynamic responses
def generate_dynamic_response(message_text, username):
    for key in dynamic_responses.keys():
        if re.search(r'\b' + re.escape(key) + r'\b', message_text):
            return dynamic_responses[key][0]  # Simplified for this example
    return None

# Event handler for incoming messages
@app.on_message(filters.text)
async def chat_with_user(client, message):
    username = message.from_user.first_name
    current_time = time.time()

    # Check if user is in cooldown period
    if current_time - user_context[username]["last_response_time"] < COOLDOWN_PERIOD:
        return

    # Generate a response based on the user's message
    response = generate_response(message.text, username)
    dynamic_response = generate_dynamic_response(message.text, username)
    
    # Update context
    user_context[username]["last_message"] = message.text
    user_context[username]["last_response_time"] = current_time

    # Choose an appropriate chat action
    chat_action = random.choice(["typing", "record_audio", "upload_photo"])

    # Show the typing/sending/recording action
    await client.send_chat_action(message.chat.id, chat_action)
    await asyncio.sleep(2)  # Simulate the time taken to type/send/record

    # Send the response to the user if there is a valid response
    if response:
        await message.reply(response)
    elif dynamic_response:
        await message.reply(dynamic_response)
