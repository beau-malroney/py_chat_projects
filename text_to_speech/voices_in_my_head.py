import pyttsx3 
# Initialize the engine
engine = pyttsx3.init()
# rate = engine.getProperty('rate')
engine.setProperty('rate', 400)
# engine.setProperty('pitch', 0.5)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
for v in voices:
    print(v)
engine.setProperty('voice', voices[1].id)
engine.say("The voices in my head keep on telling me to pray.") 
engine.runAndWait()