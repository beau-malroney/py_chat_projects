# Python program to listen for user speech, convert to text and then repeat the text to the user.

import speech_recognition as sr
import pyttsx3 

# Initialize the recognizer 
r = sr.Recognizer() 

# Convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
    
# Loop until exit commmand: User's Speech will be converted to Text
running = True
while(running):    
    
    try:
        print("Listening for input...Say EXIT NOW to end.")
        # Use Microphone as input
        with sr.Microphone() as source2:
            
            # Recognizer will adjust for surrounding noise
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            # Listen for user speech 
            audio2 = r.listen(source2)
            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Recorded speech", MyText)
            SpeakText(MyText)
            if "EXIT NOW" in MyText.upper():
                running = False
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("unknown error occurred")