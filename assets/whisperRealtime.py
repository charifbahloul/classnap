import io
from pydub import AudioSegment
import speech_recognition as sr
import datetime
import concurrent.futures
from deepgram import Deepgram
import asyncio
import traceback

WAVE_OUTPUT_FILENAME = "files/output.wav"


def load_model(model_name="base.en"):
    global whisper
    import whisper

    model = whisper.load_model(model_name)
    return model


def transcribe(
    main_logger,
    model="",
    pause_threshold=0.5,
    deepgram_api_key="",
    sound_threshold=700,
    use_deepgram=True,
    deepgram_model_name="nova",
):
    executor2 = concurrent.futures.ThreadPoolExecutor(
        max_workers=1
    )  # So that the clips have to get in line (queue).

    main_logger.info("Talking start.")
    with sr.Microphone(sample_rate=16000) as source:
        while True:
            # load the speech recognizer with CLI settings
            r = sr.Recognizer()
            r.energy_threshold = sound_threshold
            r.pause_threshold = pause_threshold
            r.dynamic_energy_threshold = True

            # record audio stream into wav
            audio = r.listen(source)
            if use_deepgram:
                # asyncio.set_event_loop(asyncio.new_event_loop())
                # Converted to thread.
                executor2.submit(
                    asyncio.get_event_loop().run_until_complete,
                    transcribe_deepgram(
                        audio, deepgram_api_key, main_logger, deepgram_model_name
                    ),
                )
                # asyncio.run(transcribe_deepgram(audio, deepgram_api_key, deepgram_model_name)) # So that I can continuously record.
            else:
                executor2.submit(transcribe_whisper, main_logger, model, audio)


def transcribe_whisper(main_logger, model, audio):
    start = datetime.datetime.now()

    try:
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(WAVE_OUTPUT_FILENAME, format="wav")

        result = model.transcribe(WAVE_OUTPUT_FILENAME, language="english")
        predicted_text = result["text"][1:]
        main_logger.info(str(predicted_text))
        if predicted_text != "":
            with open("files/transcript.txt", "a", encoding="utf-8") as f:
                f.write(predicted_text)  # Because it adds a wierd space.
                f.write("\n\n")

        end = datetime.datetime.now()
        duration = end - start
        main_logger.debug("Processing delay: " + str(duration))
    except Exception as e:
        main_logger.error("Transcribe_whisper error: " + str(e))


async def transcribe_deepgram(
    audio, deepgram_api_key, main_logger, deepgram_model_name="nova"
):
    start = datetime.datetime.now()
    dg_client = Deepgram(deepgram_api_key)
    try:
        # Convert to bytes.
        audio_wav = audio.get_wav_data()

        # Set the source
        source = {"buffer": audio_wav, "mimetype": "audio/x-wav"}

        result = await asyncio.create_task(
            dg_client.transcription.prerecorded(
                source,
                {"punctuate": True, "model": deepgram_model_name, "language": "en-US"},
            )
        )
        predicted_text = result["results"]["channels"][0]["alternatives"][0][
            "transcript"
        ]
        main_logger.info(str(predicted_text))

        with open("files/transcript.txt", "a", encoding="utf-8") as f:
            f.write(predicted_text)
            f.write("\n")

        end = datetime.datetime.now()
        duration = end - start
        main_logger.debug("Processing delay: " + str(duration))
    except Exception as e:
        main_logger.error("Transcribe_deepgram error: " + str(e))
        main_logger.error(traceback.format_exc())


if __name__ == "__main__":
    # model = load_model()

    # Direct main_logger to print to console.
    import logging

    main_logger = logging.getLogger("main")
    main_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    main_logger.addHandler(handler)

    transcribe(main_logger, deepgram_api_key="hi")
