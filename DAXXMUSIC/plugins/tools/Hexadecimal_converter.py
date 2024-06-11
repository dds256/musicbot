from pyrogram import Client, filters
from DAXXMUSIC import app

# Function to convert decimal to hexadecimal
def decimal_to_hex(decimal_number):
    try:
        hex_representation = hex(decimal_number)
        return hex_representation
    except Exception as e:
        return f"Error converting decimal to hex: {str(e)}"

# Command handler
def register_decimal_to_hex_handler(app):
    @app.on_message(filters.command("tohex"))
    def convert_decimal_to_hex(_, message):
        if len(message.command) > 1:
            try:
                decimal_number = int(message.command[1])
                hex_representation = decimal_to_hex(decimal_number)
                response_text = f"Decimal: {decimal_number}\nHexadecimal: {hex_representation}"
            except ValueError:
                response_text = "Please provide a valid decimal number."
        else:
            response_text = "Usage: /tohex <decimal_number>"

        message.reply_text(response_text)
        
