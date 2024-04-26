# This is a project by Miikka Mäki, initially written 26.04.2024
# Just started to play aroung speech recognition, it's a cool tool

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
    plt.subplot(2, 1, 1)
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    frequencies, times, power_spectrum = stft(data, fs=sample_rate, nperseg=1024)
    power_spectrum_db = 10 * np.log10(np.abs(power_spectrum))
    plt.subplot(2, 1, 2)
    plt.pcolormesh(times, frequencies, power_spectrum_db, shading='gouraud')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar(label='Power (dB)')

    plt.tight_layout()
    plt.show()

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