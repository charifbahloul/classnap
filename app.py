from flask import Flask, render_template
import concurrent.futures
from assets.Analyzer import summarizer
import assets.FileOperations as fo
from assets.whisperRealtime import transcribe, load_model

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
    model = load_model(fo.model_name)

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(app.run)

    # Start the summarizer.
    executor.submit(summarizer, fo.api_key, fo.summarize_threshold, fo.max_tokens, fo.max_lines)
    transcribe(model, fo.pause_threshold)

if __name__ == "__main__":
    main()