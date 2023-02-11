import pyaudio
import whisper
import numpy as np
from Recorder import record
from ChatGPTSummary import summarize

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "output.wav"
model = whisper.load_model("base.en")

def whisperStuff():
    # Read the audio data from the file into a numpy array
    result = model.transcribe(WAVE_OUTPUT_FILENAME, language = "english")["text"]
    print(result)

    return result

if __name__ == "__main__":
    record(FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)
    result = whisperStuff()
    print(summarize(result))