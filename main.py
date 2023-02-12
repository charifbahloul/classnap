from Recorder import record
from Analyzer import open_file, whisperStuff, summarize, load_model
from tkinterFrontEnd import main as gui
import concurrent.futures

RECORDING_PERIOD = 15 # Record for x seconds
SUMMARIZE_EVERY = 3 # Summarize every x recordings. Shouldn't summarize more than once every minute.
MODEL_NAME = "base.en" # It barely works with the base model. It needs alot of power. Otherwise, it gets overloaded with too many threads trying to transcribe and stops working or worse yet, comes out in the wrong order.
model = load_model(MODEL_NAME)

def main():
    # Clear the transcript.txt file
    with open("transcript.txt", "w") as f:
        # f.write("First recording...\n\n")
        f.write("")
    # Clear the summary.txt file
    with open("summary.txt", "w") as f:
        # f.write("First recording...\n\n")
        f.write("")

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

        if counter >= SUMMARIZE_EVERY*3:
            # Delete the first summary.
            with open("summary.txt", "r") as f:
                summaries = f.readlines()
            # Split it by \n\n.
            summaries = summaries.split("\n\n")
            # Delete the first element.
            summaries = summaries[1:]
            # Join it back together.
            summaries = "\n\n".join(summaries)
            # Write it back to the file.
            with open("summary.txt", "w") as f:
                f.writelines(summaries)

        counter += 1
        
if __name__ == "__main__":
    main()