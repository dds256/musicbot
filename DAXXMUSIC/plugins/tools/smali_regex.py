import re
from pyrogram import filters
from DAXXMUSIC import app as app

@app.on_message(filters.command("smali2regex"))
async def smali_to_regex_command(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: /smali2regex <smali_code>")
        return

    smali_code = " ".join(message.command[1:])
    if not smali_code and not message.reply_to_message:
        await message.reply("Please provide Smali code or reply to a message containing Smali code. example: /smali2regex your code here..")
        return

    if not smali_code:
        smali_code = message.reply_to_message.text

    regex_pattern = convert_smali_to_regex(smali_code)

    if regex_pattern:
        await message.reply(f"Generated Regex Pattern:\n`{regex_pattern}`", parse_mode="markdown")
    else:
        await message.reply("Failed to generate regex pattern. Please check your input and try again.")

def convert_smali_to_regex(smali_code):
    try:
        # Example conversion: Replace method invocation syntax with regex pattern
        regex_pattern = re.escape(smali_code)  # Escape special regex characters
        regex_pattern = regex_pattern.replace("\{", "\\{").replace("\}", "\\}")  # Escape curly braces
        regex_pattern = regex_pattern.replace("(", "\\(").replace(")", "\\)")  # Escape parentheses
        regex_pattern = regex_pattern.replace("[", "\\[").replace("]", "\\]")  # Escape square brackets
        regex_pattern = regex_pattern.replace(".", "\\.")  # Escape dots
        regex_pattern = regex_pattern.replace("(", "\\(").replace(")", "\\)")  # Escape parentheses
        regex_pattern = regex_pattern.replace("+", "\\+")  # Escape plus signs
        regex_pattern = regex_pattern.replace(";", "\\;")  # Escape semicolons
        return regex_pattern
    except Exception as e:
        print(f"Error converting Smali code to regex: {e}")
        return None
