# from assets.Recorder import record
from assets.Analyzer import summarize, summarizer, clear_files
from assets.tkinterFrontEnd import main as gui
from assets.whisperRealtime import transcribe, load_model
import concurrent.futures

RECORDING_PERIOD = 2 # Record for x seconds
SUMMARIZE_EVERY = 3 # Summarize every x recordings. Shouldn't summarize more than once every minute.
MODEL_NAME = "base.en" # It barely works with the base model. It needs alot of power. Otherwise, it gets overloaded with too many threads trying to transcribe and stops working or worse yet, comes out in the wrong order.
model = load_model(MODEL_NAME)

def main():
    clear_files()
    executor = concurrent.futures.ThreadPoolExecutor()

    # # Start the GUI
    # executor.submit(gui)

    # Start the transcriber.
    executor.submit(transcribe, model) 
    # transcribe(model)

    # # Start the summarizer.
    # executor.submit(summarizer)
        
if __name__ == "__main__":
    main()