from Recorder import record
from Analyzer import open_file, whisperStuff, summarize, load_model
from tkinterFrontEnd import main as gui
import concurrent.futures

RECORDING_PERIOD = 10
SUMMARIZE_EVERY = 9 # Summarize every 9 recordings
MODEL_NAME = "base.en"
model = load_model(MODEL_NAME)

def main():
    # futures = []
    # Clear the transcript.txt file
    with open("transcript.txt", "w") as f:
        f.write("First recording...")
    # Clear the summary.txt file
    with open("summary.txt", "w") as f:
        f.write("First recording...")

    executor = concurrent.futures.ThreadPoolExecutor()

    # Start the GUI
    executor.submit(gui)

    counter = 0
    while True:
        record(RECORDING_PERIOD)
        future = executor.submit(whisperStuff, model)
        
        if counter % SUMMARIZE_EVERY == 0:
            # Read all of the transcripts from the transcript.txt file
            with open("transcript.txt", "r") as f:
                transcript = f.readlines()
            transcript = '\n'.join(transcript)
            summarize(transcript, num_points=3)

        counter += 1
        
if __name__ == "__main__":
    main()