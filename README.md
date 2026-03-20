# Stegano Vault

> A simple cross-media steganography GUI & backend toolkit to hide and reveal secret messages in images and audio files.

Steganography is the art of hiding information in plain sight. This project lets you conceal text in images (.png/.jpg) and hide/retrieve text in audio (.wav) using Least-Significant Bit (LSB) techniques.

---
### How It Works (Overview)
=> **Image:**
Uses LSB steganography where message bits replace the least significant bits of image pixels. The visual difference is usually unnoticeable.

=> **Audio**
Message bits are inserted into the least significant bits of audio frame bytes. A delimiter (like ###END###) is used to know where the message stops.

###  Features

###  Image Steganography  
✔ Hide secret messages inside PNG/JPEG images  
✔ Reveal hidden messages from stego images  
✔ GUI-friendly interface  

###  Audio Steganography  
✔ Encode text in a WAV file using LSB manipulation  
✔ Decode hidden text from encoded WAV audio  

###  Easy to Use  
✔ Clean GUI with intuitive tabs  
✔ Simple Python backend logic  
✔ Minimal dependencies  

---

##  Installation

1. **Clone the repository**

```
git clone https://github.com/aditya05005/stegano_vault.git
cd stegano_vault
```

2. **Install dependencies**
```
pip install -r requirements.txt
```
---
### Usage 
Run the app with:
```
python frontend.py
```

This opens a window with three section:
-> Image Encode
-> Image Decode
-> Audio Stegnography

---

### Encoding a Message

Images:
Select a cover image (.png/.jpg)
Enter the message you want to hide
Click Encrypt / Hide

Audio:
Select a .wav file
Enter the secret text
Click Hide in Audio

### Decoding a Message

Choose a stego image or encoded audio file

Click the appropriate Reveal / Decode button

The hidden message will be displayed

### Future Enhancements

-> Password-based encryption

-> More audio formats

-> CLI version

-> Stego file previews
