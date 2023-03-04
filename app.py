from flask import Flask, render_template
import concurrent.futures
from assets.Analyzer import summarizer
import assets.FileOperations as fo
from assets.whisperRealtime import transcribe, load_model

app = Flask(__name__)
print("Ctrl+Click here: http://127.0.0.1:5000")

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
    print("Please get the session token using this extension: https://chrome.google.com/webstore/detail/chatgpt-cookies/nnkcnhbioochcaoeofflcljhhpceoknl")
    print("Once installed, click on it and it will redirect you to ChatGPT. Click on the extension again and copy the session token.")
    print("Session token: ", end="")
    openai_api_key = input()

    if not fo.use_deepgram:
        model = load_model(fo.model_name)

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(app.run)

    # Start the summarizer.
    executor.submit(summarizer, openai_api_key, fo.prompt, fo.summarize_threshold)
    
    # Transcriber
    if fo.use_deepgram:
        transcribe(pause_threshold = fo.pause_threshold, deepgram_api_key = fo.deepgram_api_key, sound_threshold=fo.sound_threshold)
    else:
        transcribe(model = model, pause_threshold = fo.pause_threshold, use_deepgram = fo.use_deepgram)

if __name__ == "__main__":
    main()
