from flask import Flask, render_template
import concurrent.futures
from assets.Analyzer import summarizer
import assets.FileOperations as fo
from assets.whisperRealtime import transcribe, load_model
import os

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def add_header(response): # I know this is brute force. But I like brute force.
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
    executor.submit(app.run)

    # Start the summarizer.
    print(fo.prompt, fo.summarize_threshold)
    executor.submit(summarizer, fo.prompt, fo.summarize_threshold)

    try: # Clear the screen.
        os.system("clear")  
    except:
        os.system("cls")
    print("\n\nCtrl+Click here: http://127.0.0.1:5000\n\n\n\n\n\n")
    
    # Transcriber
    if fo.use_deepgram:
        transcribe(pause_threshold = fo.pause_threshold, deepgram_api_key = fo.deepgram_api_key, sound_threshold=fo.sound_threshold, deepgram_model_name=fo.deepgram_model_name, use_deepgram = fo.deepgram_model_name)
    else:
        transcribe(model = model, pause_threshold = fo.pause_threshold, use_deepgram = fo.use_deepgram)

if __name__ == "__main__":
    main()
