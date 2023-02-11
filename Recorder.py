import pyaudio, wave


def record(FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
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
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

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