import pyaudio
import whisper
from Recorder import record
from Analyzer import analyze, summarize
import concurrent.futures
import time

if __name__ == "__main__":
    all_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            while True:
                record(10)

                # print("Simulating recording...")
                # time.sleep(5)
            
                future = executor.submit(analyze)
                # all_results.append(future.result())
                # print(future.result())
        except KeyboardInterrupt:
            executor.shutdown(wait=False)
            all_results = '\n'.join(all_results)
            print("Here's the summary of the whole thing: ")
            summarize(all_results, 7)
        