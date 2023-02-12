from flask import Flask, render_template
import time
import concurrent.futures
from assets.Analyzer import summarize, summarizer, clear_files
from assets.tkinterFrontEnd import main as gui
from assets.whisperRealtime import transcribe, load_model
import concurrent.futures

RECORDING_PERIOD = 2 # Record for x seconds
SUMMARIZE_EVERY = 3 # Summarize every x recordings. Shouldn't summarize more than once every minute.
MODEL_NAME = "base.en" # It barely works with the base model. It needs alot of power. Otherwise, it gets overloaded with too many threads trying to transcribe and stops working or worse yet, comes out in the wrong order.
model = load_model(MODEL_NAME)

app = Flask(__name__)

@app.route("/")
def index():
    transcript = get_file_contents("files/transcript.txt")
    summary = get_file_contents("files/summary.txt")
    return render_template("index.html", transcript=transcript, summary=summary)

def get_file_contents(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
    return contents.replace("\n\n", "\n")

def main():
    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(app.run)

    clear_files()
    executor = concurrent.futures.ThreadPoolExecutor()

    # Start the GUI
    executor.submit(gui)

    # # Start the summarizer.
    executor.submit(summarizer)


    # Start the transcriber. Wouldn't work.
    # executor.submit(transcribe, model) 


    transcribe(model)

    print("hi.")
