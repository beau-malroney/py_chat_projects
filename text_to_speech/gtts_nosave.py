from gtts import gTTS
from io import BytesIO

text = "Hello World!"

# get audio from server
tts = gTTS(text=text, lang='en')

# convert to file-like object
fp = BytesIO()
tts.write_to_fp(fp)
fp.seek(0)

# --- play it ---

from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_file(fp, format="mp3")
play(song)