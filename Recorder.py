import pyaudio, wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

def record(record_seconds=120):
    # create & configure microphone
    mic = pyaudio.PyAudio()
    stream = mic.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # read & store microphone data per frame read
    frames = []
    print("Recording...")
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")

    # kill the mic and recording
    stream.stop_stream()
    stream.close()
    mic.terminate()

    # combine & store all microphone data to output.wav file
    outputFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    outputFile.setnchannels(CHANNELS)
    outputFile.setsampwidth(mic.get_sample_size(FORMAT))
    outputFile.setframerate(RATE)
    outputFile.writeframes(b''.join(frames))
    outputFile.close()