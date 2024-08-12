from gtts import gTTS
import os

# Text to be spoken
text = "Hello! This is an example of using gTTS."

# Language and voice selection
language = 'en'
voice = 'slt'

# Create a GtTs instance with the language and voice
tts = gTTS(text=text, lang=language, tld='com.au', slow=False)

# Save the audio file
tts.save("output.mp3")

# Play the audio file using the default media player
os.system("start output.mp3")