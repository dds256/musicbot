import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pyrogram import filters
from DAXXMUSIC import app as app

# Default key for AES encryption and decryption
DEFAULT_KEY = b'UYGy723!Po-efjve'

# Function to encrypt plaintext using AES ECB mode with PKCS5 padding
def encrypt_aes_ecb(plaintext, key=None):
    if key is None:
        key = DEFAULT_KEY
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode('utf-8')

# Function to decrypt AES ECB ciphertext with PKCS5 padding
def decrypt_aes_ecb(ciphertext, key=None):
    if key is None:
        key = DEFAULT_KEY
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    return unpad(decrypted, AES.block_size).decode('utf-8')

# Command to encrypt plaintext using AES ECB mode
@app.on_message(filters.command("aes_enc"))
async def encrypt_aes_command(bot, message):
    args = message.command[1:]
    if len(args) != 1:
        await message.reply("Usage: /aes_enc <plaintext>")
        return
    
    plaintext = args[0]
    try:
        ciphertext = encrypt_aes_ecb(plaintext)
        await message.reply(f"Encryption Result: {ciphertext}")
    except Exception as e:
        await message.reply(f"Encryption failed: {str(e)}")

# Command to decrypt AES ECB ciphertext
@app.on_message(filters.command("aes_dec"))
async def decrypt_aes_command(bot, message):
    args = message.command[1:]
    if len(args) != 1:
        await message.reply("Usage: /aes_dec <base64_encoded_ciphertext>")
        return
    
    ciphertext = args[0]
    try:
        plaintext = decrypt_aes_ecb(ciphertext)
        await message.reply(f"Decryption Result: {plaintext}")
    except Exception as e:
        await message.reply(f"Decryption failed: {str(e)}")
