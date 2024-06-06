import random
import asyncio
import datetime
from pyrogram import Client, filters
from DAXXMUSIC import app

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
    "playful": ["You're such a tease!", "Stop it, you naughty thing!", "You're making me blush!", "You know how to make a girl giggle!", "Are you trying to distract me?", "I love your sense of humor!", "I'm feeling mischievous today!", "You're in for some fun with me!", "Let's keep it playful!"],
    "flirty": ["You know how to make a girl smile!", "You're so charming!", "You're quite the flirt, aren't you?", "I'm all yours, you smooth talker!", "You're making my heart race!", "Careful, you're melting my heart!", "You're turning up the heat!", "Let's spice things up a bit!", "You're irresistible!"],
    "favorite food": ["I love pizza, what about you?", "Sushi is my favorite, what's yours?", "I can't get enough of chocolate!", "I'm craving some ice cream right now!", "Italian food is always a good choice!", "How about some comfort food?"],
    "movies": ["I love watching romantic comedies, what about you?", "Action movies are so thrilling!", "Horror movies give me the chills!", "Let's have a movie night together!", "I'm in the mood for a movie marathon!", "What's your favorite movie genre?"],
    "music": ["I enjoy listening to pop music, what about you?", "Rock music really gets me going!", "Classical music is so soothing!", "Let's dance to some tunes!", "Music always lifts my spirits!", "What's your favorite song right now?", "I'm in the mood for some live music!"],
    "dreams": ["I had the most interesting dream last night!", "Do you ever have weird dreams?", "Dreams can be so mysterious!", "I love it when dreams feel so real!", "Tell me about your craziest dream!", "I wonder what our dreams say about us!", "I wish we could control our dreams!", "Dreams are like a window to our subconscious!", "I had a dream about us..."],
    "memories": ["Remember that time we...", "I cherish all our memories together!", "Some memories just never fade!", "Let's make more unforgettable memories!", "Do you ever think about our first meeting?", "I'll never forget the moment we..."],
    "compliments": ["You always know how to make me smile!", "You're one of a kind!", "You're the highlight of my day!", "I love spending time with you!", "You have the most beautiful eyes!", "You make my heart skip a beat!", "You're amazing just the way you are!"],
    "secrets": ["I have a little secret to tell you...", "Promise not to tell anyone?", "Can you keep a secret?", "I trust you with my deepest secrets!", "I feel like I can tell you anything!", "You're the keeper of all my secrets!", "Let's share our secrets with each other!", "You're about to learn my darkest secret...", "I can't keep this secret any longer..."]
}

# Function to generate a response based on the input message
async def generate_response(message_text, username):
    # Simulate typing
    await asyncio.sleep(random.uniform(1, 3))

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
            # Simulate typing before sending the response
            await asyncio.sleep(random.uniform(1, 3))
            return random.choice(responses[key])
    
    # Return a default response if no match is found, with personalization
    # Simulate typing before sending the response
    await asyncio.sleep(random.uniform(1, 3))
    return random.choice(responses["default"]).replace("!", f", {username}!")

# Event handler for incoming messages
@app.on_message(filters.text)
async def chat_with_user(client, message):
    # Simulate typing before generating a response
    await app.send_chat_action(message.chat.id, "typing" if "typing" in ["typing", "upload_photo", "record_video", "upload_video", "record_audio", "upload_audio", "upload_document", "find_location", "record_video_note", "upload_video_note"] else "typing")
    
    # Generate a response based on the user's message
    username = message.from_user.first_name
    response = await generate_response(message.text, username)
    
    # Simulate typing before sending the response
    await app.send_chat_action(message.chat.id, "typing" if "typing" in ["typing", "upload_photo", "record_video", "upload_video", "record_audio", "upload_audio", "upload_document", "find_location", "record_video_note", "upload_video_note"] else "typing")
    
    # Send the response to the user
    await message.reply(response)
