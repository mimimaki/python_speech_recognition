# Initially written by mimimaki in 26.04.2024,
# tkinter GUI addded in 16.12.2024.

import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import scrolledtext
from scipy.io import wavfile
from scipy.signal import stft

class SpeechRecognizer:
    def __init__(self):
        self.recog = sr.Recognizer()
        self.stop = False
        self.save_audio = True
        self.text = True
        self.plot = False

    def recognize(self, audio):
        try:
            text = self.recog.recognize_google(audio)
            print("Input: "+ text)
            return text
        except Exception as e:
            return f"Error: {e}"

    def record(self, audio):
        with open("media/recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

    def compute_spectrogram(self, audio):
        sample_rate, data = wavfile.read(audio)
        t = np.arange(len(data)) / sample_rate

        freq, times, power_spectrum = stft(data, fs=sample_rate, nperseg=1024)
        power_spectrum_db = 10 * np.log10(np.abs(power_spectrum))
        return t, data, times, freq, power_spectrum_db

class SpeechApp:

    def __init__(self, root):
        self.speech_recognizer = SpeechRecognizer()
        self.is_recording = False
        self.root = root
        self.root.title("Speech Recognizer")

        # Buttons
        self.start = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start.grid(row=0, column=0, padx=10, pady=10)

        self.stop = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop.grid(row=0, column=1, padx=10, pady=10)

        self.recognize = tk.Button(root, text="Recognize Speech", command=self.recognize_speech)
        self.recognize.grid(row=0, column=2, padx=10, pady=10)

        self.spectogram = tk.Button(root, text="Spectrogram", command=self.plot_spectrogram)
        self.spectogram.grid(row=0, column=3, padx=10, pady=10)

        # Output box
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        self.output.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Canvas for Spectrogram
        self.figure = plt.Figure(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    def start_recording(self):
        self.is_recording = True
        self.output.insert(tk.END, "Recording...\n")
        self.root.update()

        with sr.Microphone() as source:
            try:
                self.output.insert(tk.END, "Listening...\n")
                self.root.update()
                self.speech_recognizer.audio_data = self.speech_recognizer.recog.listen(source)
                if self.speech_recognizer.save_audio:
                    self.speech_recognizer.record(self.speech_recognizer.audio_data)
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")

    def stop_recording(self):
        self.is_recording = False
        self.output.insert(tk.END, "Stopped recording.\n")

    def recognize_speech(self):
        if self.speech_recognizer.audio_data is not None:
            text = self.speech_recognizer.recognize(self.speech_recognizer.audio_data)
            self.output.insert(tk.END, f"Recognized speech: {text}\n")
        else:
            self.output.insert(tk.END, "Error: No audio.\n")

    def plot_spectrogram(self):
        try:
            if self.speech_recognizer.audio_data is not None:
                self.speech_recognizer.record(self.speech_recognizer.audio_data)
                audio = "media/recording.wav"

                t, data, times, freq, power_spectrum_db = self.speech_recognizer.compute_spectrogram(audio)

                self.figure.clear()
                ax1 = self.figure.add_subplot(211)
                ax1.plot(t, data)
                ax1.set_xlabel('Time (s)')
                ax1.set_ylabel('Amplitude')

                ax2 = self.figure.add_subplot(212)
                cax = ax2.pcolormesh(times, freq, power_spectrum_db)
                self.figure.colorbar(cax, ax=ax2, label='Power (dB)')
                ax2.set_title('Spectrogram')
                ax2.set_xlabel('Time (s)')
                ax2.set_ylabel('Frequency (Hz)')

                self.canvas.draw()
            else:
                self.output.insert(tk.END, "No audio data.\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error in spectrogram: {e}\n")

if __name__=="__main__":

    root = tk.Tk()
    app = SpeechApp(root)
    root.mainloop()