from flask import Flask, render_template, after_this_request, Response
import time
import concurrent.futures
from assets.Analyzer import summarize, summarizer, clear_files, get_file_contents
from assets.whisperRealtime import transcribe, load_model
import concurrent.futures
import cv2
import numpy as np

RECORDING_PERIOD = 2 # Record for x seconds
SUMMARIZE_EVERY = 3 # Summarize every x recordings. Shouldn't summarize more than once every minute.
MODEL_NAME = "tiny.en" # It barely works with the base model. It needs alot of power. Otherwise, it gets overloaded with too many threads trying to transcribe and stops working or worse yet, comes out in the wrong order.
model = load_model(MODEL_NAME)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def add_header(response): # I know this is brute force. But I like brute force.
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/summary", methods=["GET"])
def get_summary():
    return get_file_contents("files/summary.txt", replace=False)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    transcript_file = get_file_contents("files/transcript.txt").split(" ")
    if len(transcript_file) > 250:
        return " ".join(transcript_file[-250:])
    else:
        return " ".join(transcript_file)

# # Get logo. Turns out I don't like it.
# @app.route("/logo", methods=["GET"])
# def get_logo():
#     logo = cv2.imread("files/logo.jpg")
#     _, img_encoded = cv2.imencode(".jpg", logo)
#     return Response(img_encoded.tobytes(), content_type="image/jpeg")

def main():
    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(app.run)

    clear_files()
    executor = concurrent.futures.ThreadPoolExecutor()
    # Start the summarizer.
    executor.submit(summarizer)

    # Start the transcriber. Wouldn't work.
    # executor.submit(transcribe, model) 
    transcribe(model)
 

if __name__ == "__main__":
    main()