import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import pdb
from scipy.io import wavfile
from scipy.signal import stft

# Start listening
r = sr.Recognizer()
stop = False
plot = False

def draw_plots(audio):
    sample_rate, data = wavfile.read(audio)
    time = np.arange(len(data)) / sample_rate
    plt.figure(figsize=(12,6))
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

    pdb.set_trace()

while(stop==False):
# Open microphone
    with sr.Microphone() as source:
        print("Ready for speech") 
        audio2text = r.listen(source)

        try:
            # google speech recognition to read input
            text = r.recognize_google(audio2text)
            print("Input: "+ text)

            # use keyword "stop" to quit function
            match text:
                case "stop":
                    stop = True
                case "plot":
                    plot = True
                case "record":
                    with open("microphone-results.wav", "wb") as f:
                        f.write(audio2text.get_wav_data())
        except:
            print("Did not understand, could you repeat?")
if (plot==True):
    draw_plots(audio="microphone-results.wav")