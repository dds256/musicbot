import os
from PIL import Image, ImageDraw
from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app

def add_round_corners(image, radius):
    print("Adding round corners...")
    # Create a mask to add rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # Apply the mask to the image
    image = image.convert("RGBA")
    image.putalpha(mask)
    
    return image

@app.on_message(filters.command("round"))
async def round_corner_command(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Please reply to a photo with the command `/round [radius]` to add rounded corners to the image.")
        return

    processing_message = await message.reply("Processing your image...")

    try:
        print("Command received, processing started...")
        # Get the radius from the command or set a default
        radius = int(message.command[1]) if len(message.command) > 1 else 30

        # Download the image
        photo = message.reply_to_message.photo[-1]
        photo_path = await client.download_media(photo.file_id)
        print(f"Image downloaded to {photo_path}")

        # Open the image
        image = Image.open(photo_path)
        
        # Apply rounded corners
        rounded_image = add_round_corners(image, radius)
        
        # Save the rounded image
        output_path = "rounded_image.png"
        rounded_image.save(output_path)
        print(f"Image saved to {output_path}")
        
        # Send the rounded image back to the user as a document
        await processing_message.edit("Uploading your image with rounded corners...")
        await message.reply_document(document=output_path, caption="Here is your image with rounded corners!")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        await processing_message.edit(f"An error occurred: {str(e)}")

    finally:
        # Clean up
        if os.path.exists(photo_path):
            os.remove(photo_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        await processing_message.delete()
