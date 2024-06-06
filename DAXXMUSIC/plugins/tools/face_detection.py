import cv2
import numpy as np
from PIL import Image
from DAXXMUSIC import app as app
from pyrogram import Client, filters

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.on_message(filters.command("detectface"))
async def detect_faces(_, message):
    try:
        processing_message = await message.reply("Processing the replied image for face detection...")

        # Check if the message is a reply and contains an image
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]  # Get the highest resolution photo
            photo_path = await app.download_media(photo)
        elif message.reply_to_message and message.reply_to_message.document and message.reply_to_message.document.mime_type.startswith("image/"):
            document_path = await app.download_media(message.reply_to_message.document)
            photo_path = document_path
        else:
            await processing_message.edit("Please reply to a valid image file.")
            return

        # Open the image using PIL and convert it to OpenCV format
        pil_image = Image.open(photo_path)
        open_cv_image = np.array(pil_image.convert('RGB'))
        open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR

        # Convert the image to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(open_cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Convert the image back to PIL format and save it
        result_image = Image.fromarray(open_cv_image[:, :, ::-1])  # Convert BGR to RGB
        result_image_path = "detected_faces.jpg"
        result_image.save(result_image_path)

        # Send the processed image back to the user
        await app.send_photo(message.chat.id, result_image_path, caption="Here are the detected faces.")
        
        # Delete the progress message after sending the image
        await processing_message.delete()
    except Exception as e:
        await processing_message.edit(f"An error occurred: {str(e)}")
