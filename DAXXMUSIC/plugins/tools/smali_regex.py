import re
from pyrogram import filters
from DAXXMUSIC import app as app

@app.on_message(filters.command("smali2regex"))
async def smali_to_regex_command(bot, message):
    # Check if Smali code is provided in the command or replied to a message
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("Please provide Smali code or reply to a message containing Smali code. Example: /smali2regex your code here.")
        return

    # Extract Smali code from the command or replied message
    smali_code = " ".join(message.command[1:])
    if not smali_code:
        smali_code = message.reply_to_message.text

    # Check if Smali code is provided
    if not smali_code:
        await message.reply("Please provide Smali code or reply to a message containing Smali code. Example: /smali2regex your code here.")
        return

    # Send "Converting..." message
    await message.reply("Converting Smali code to regex pattern...")

    # Convert Smali code to regex pattern
    regex_pattern = convert_smali_to_regex(smali_code)

    # Send the generated regex pattern or error message
    if regex_pattern:
        await message.reply(f"Generated Regex Pattern:\n`{regex_pattern}`", parse_mode="markdown")
    else:
        await message.reply("Failed to generate regex pattern. Please check your input and try again.")

def convert_smali_to_regex(smali_code):
    try:
        # Escape special regex characters
        regex_pattern = re.escape(smali_code)

        # Additional replacements for specific characters
        regex_pattern = regex_pattern.replace("{", "\\{").replace("}", "\\}")
        regex_pattern = regex_pattern.replace("(", "\\(").replace(")", "\\)")
        regex_pattern = regex_pattern.replace("[", "\\[").replace("]", "\\]")
        regex_pattern = regex_pattern.replace("+", "\\+")
        regex_pattern = regex_pattern.replace(";", "\\;")

        return regex_pattern
    except Exception as e:
        print(f"Error converting Smali code to regex: {e}")
        return None
