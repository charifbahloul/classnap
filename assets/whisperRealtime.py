import io
from pydub import AudioSegment
import speech_recognition as sr
import datetime
import concurrent.futures
import traceback
from deepgram import Deepgram
import asyncio

WAVE_OUTPUT_FILENAME = "files/output.wav"

def load_model(model_name='base.en'):
    global whisper
    import whisper
    model = whisper.load_model(model_name)
    return model

def transcribe(model="", pause_threshold=.8, deepgram_api_key = "", use_deepgram=True):
    executor2 = concurrent.futures.ThreadPoolExecutor(max_workers=1) # So that the clips have to get in line.

    with sr.Microphone(sample_rate=16000) as source:
        print("Talking start.")
        while True:
            # load the speech recognizer with CLI settings
            r = sr.Recognizer()
            r.energy_threshold = 500
            r.pause_threshold = pause_threshold # When it decides to launch whisper.
            r.dynamic_energy_threshold = True

            # record audio stream into wav
            audio = r.listen(source)
            print("Finished one.")
            if use_deepgram:
                executor2.submit(asyncio.run, transcribe_deepgram(audio, deepgram_api_key)) # So that I can continuously record.
            else:
                executor2.submit(transcribe_whisper, model, audio)

def transcribe_whisper(model, audio):
    start = datetime.datetime.now()

    try:
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(WAVE_OUTPUT_FILENAME, format="wav")
        print("Converted to wav.")

        result = model.transcribe(WAVE_OUTPUT_FILENAME, language='english')
        predicted_text = result["text"][1:]
        print(predicted_text)
        with open("files/transcript.txt", "a") as f:
            f.write(predicted_text) # Because it adds a wierd space.
            f.write("\n\n")

        end = datetime.datetime.now()
        duration = end-start
        print("Processing delay: ", duration)
    except:
        print("Big problem with transcribe_whisper.")
        traceback.print_exc()

async def transcribe_deepgram(audio, deepgram_api_key):
    start = datetime.datetime.now()
    dg_client = Deepgram(deepgram_api_key)

    try:
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(WAVE_OUTPUT_FILENAME, format="wav")

        audio = open(WAVE_OUTPUT_FILENAME, 'rb')

        # Set the source
        source = {'buffer': audio, 'mimetype': "files/output.wav"}

        result = await asyncio.create_task(dg_client.transcription.prerecorded(source, {'punctuate': True, "model": "whisper", "language": "en-US"}))
        predicted_text = result["results"]['channels'][0]["alternatives"][0]["transcript"][1:]
        print(predicted_text)

        with open("files/transcript.txt", "a") as f:
            f.write(predicted_text) # Because it adds a wierd space.
            f.write("\n\n")

        end = datetime.datetime.now()
        duration = end-start
        print("Processing delay: ", duration)
    except:
        print("Big problem with transcribe_deepgram.")
        traceback.print_exc()

if __name__ == "__main__":
    # model = load_model()
    transcribe(deepgram_api_key="c824aba5580e54bbace2d704359123cbba3876aa")