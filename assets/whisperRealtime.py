import argparse
import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import datetime
import concurrent.futures

WAVE_OUTPUT_FILENAME = "files/output.wav"

def load_model(model_name='base.en'):
    model = whisper.load_model(model_name)
    return model

def transcribe(model):
    executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=1) # So that the clips have to get in line.

    with sr.Microphone(sample_rate=16000) as source:
        print("Talking start.")
        while True:
            # load the speech recognizer with CLI settings
            r = sr.Recognizer()
            r.energy_threshold = 500
            r.pause_threshold = .5 # When it decides to launch whisper.
            r.dynamic_energy_threshold = True

            # record audio stream into wav
            audio = r.listen(source)
            print("Finished one.")
            executor2.submit(actually_transcribe, model, audio) # So that I can continuously record.


def actually_transcribe(model, audio):
    start = datetime.datetime.now()

    data = io.BytesIO(audio.get_wav_data())
    audio_clip = AudioSegment.from_file(data)
    audio_clip.export(WAVE_OUTPUT_FILENAME, format="wav")

    result = model.transcribe(WAVE_OUTPUT_FILENAME, language='english')

    predicted_text = result["text"]
    print(predicted_text[1:])

    with open("files/transcript.txt", "a") as f:
        f.write(predicted_text[1:]) # Because it adds a wierd space.
        f.write("\n\n")

    end = datetime.datetime.now()
    duration = end-start
    print("Processing delay: ", duration)

if __name__ == "__main__":
    model = load_model()
    transcribe(model)