import os
from stegano import lsb
from pathlib import Path
import wave

# --- IMAGE LOGIC ---
def encode_image(filepath, message, save_path="secret_image.png"):
    try:
        secret = lsb.hide(filepath, message)
        secret.save(save_path)
        full_path = Path(save_path).resolve()
        return f"Success! Saved as {full_path}"
    except Exception as e:
        return f"Error: {str(e)}"

def decode_image(filepath):
    try:
        clear_message = lsb.reveal(filepath)
        return clear_message if clear_message else "No hidden data found."
    except Exception as e:
        return f"Error: {str(e)}"

# --- AUDIO LOGIC (Standard Wave LSB) ---
def encode_audio(filepath, message, save_path="secret_audio.wav"):
    try:
        audio = wave.open(filepath, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        
        # Add a delimiter so we know when the text ends
        message = message + "###END###"
        
        # Convert message to binary bits
        bits = ''.join(format(ord(i), '08b') for i in message)
        
        # Replace LSB of audio frames with message bits
        for i in range(len(bits)):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(bits[i])
            
        frame_modified = bytes(frame_bytes)
        
        # Write to new file
        newAudio = wave.open(save_path, 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)
        
        newAudio.close()
        audio.close()
        full_path = Path(save_path).resolve()
        return f"Success! Saved as {full_path}"
    except Exception as e:
        return f"Error: {str(e)}"

def decode_audio(filepath):
    try:
        audio = wave.open(filepath, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        
        # Extract LSBs
        extracted = [str(frame_bytes[i] & 1) for i in range(len(frame_bytes))]
        string_bits = "".join(extracted)
        
        # Convert bits back to characters
        decoded_msg = ""
        for i in range(0, len(string_bits), 8):
            byte = string_bits[i:i+8]
            decoded_msg += chr(int(byte, 2))
            # Stop if we find our delimiter
            if decoded_msg.endswith("###END###"):
                return decoded_msg[:-9] # Remove the delimiter
                
        return "No hidden message found (or file too large)."
    except Exception as e:
        return f"Error: {str(e)}"