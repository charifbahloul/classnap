from flask import Flask, render_template
import concurrent.futures
from assets.Analyzer import summarizer
import assets.FileOperations as fo
from assets.whisperRealtime import transcribe, load_model
import os
import logging
import traceback

app = Flask(__name__)
version_number = "1.4.2"

log = logging.getLogger("werkzeug")  # To keep the console clean.
log.setLevel(logging.ERROR)


@app.route("/")
def index():
    return render_template("index.html")


@app.after_request
def add_header(response):  # I know this is brute force. But I like brute force.
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/summary", methods=["GET"])
def get_summary():
    # return "1\n2\n3"
    return fo.get_file_contents("files/summary.txt", "summary")


@app.route("/transcript", methods=["GET"])
def get_transcript():
    transcript_file = fo.get_file_contents("files/transcript.txt")
    transcript_file = transcript_file.split(" ")
    return " ".join(transcript_file)


def main():
    fo.get_settings()
    fo.clear_files()

    if not fo.use_deepgram:
        model = load_model(fo.model_name)

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(app.run, port=8000, debug=False)

    # Start the summarizer.
    main_logger.info("Summarize Threshold: " + str(fo.summarize_threshold))
    executor.submit(summarizer, fo.prompt, main_logger, fo.summarize_threshold)

    print("\n\nCopy and paste this link into your browser: http://127.0.0.1:8000\n\n")

    # Transcriber
    if fo.use_deepgram:
        transcribe(
            main_logger,
            pause_threshold=fo.pause_threshold,
            deepgram_api_key=fo.deepgram_api_key,
            sound_threshold=fo.sound_threshold,
            deepgram_model_name=fo.deepgram_model_name,
            use_deepgram=fo.use_deepgram,
        )
    else:
        transcribe(
            main_logger,
            model=model,
            pause_threshold=fo.pause_threshold,
            use_deepgram=fo.use_deepgram,
        )


if __name__ == "__main__":
    path_to_files = os.path.join(os.path.dirname(__file__), "files")
    main_logger = fo.setup_logger(
        "main_logger", os.path.join(path_to_files, "main.log")
    )
    main_logger.info("\nProgram started. V" + str(version_number))
    retries = 3

    for attempt in range(retries):
        try:
            main()
        except Exception as e:
            main_logger.critical("Main process is dead. Here's why: " + str(e))
            main_logger.critical(traceback.format_exc())
            main_logger.info(str(attempt) + " tries left.")
            print("Critical error. Retrying...")
