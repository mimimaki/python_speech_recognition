import speech_recognition as speechrecognition

# Start listening
r = speechrecognition.Recognizer()
stop = False

while(stop==False):
# Open microphone
    with speechrecognition.Microphone() as source:
        print("Ready for speech") 
        audio2text = r.listen(source)

        try:
            # google speech recognition to read input
            text = r.recognize_google(audio2text)
            print("Input: "+ text)
            if (text == "stop"):
                stop = True
        except:
            print("Did not understand, could you repeat?")