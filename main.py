from Recorder import record
from Analyzer import analyze, summarize
import concurrent.futures

SUMMARIZE_PERIOD = 90
MODEL_NAME = "base.en"

def main():
    futures = []
    # Clear the transcript.txt file
    with open("transcript.txt", "w") as f:
        f.write("")
    # Clear the summary.txt file
    with open("summary.txt", "w") as f:
        f.write("")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            while True:
                record(SUMMARIZE_PERIOD)

                # print("Simulating recording...")
                # time.sleep(5)
            
                future = executor.submit(analyze, MODEL_NAME)
                # futures.append(future)

                # analyze()
                # all_results.append(future.result())
                # print(future.result())
        except KeyboardInterrupt:
            executor.shutdown(wait=False)
            all_results = []
            # for future in concurrent.futures.as_completed(futures):
            #     all_results.append(future.result())

            # Read all of the summaries from the summary.txt file
            with open("summary.txt", "r") as f:
                all_results = f.readlines()
            all_results = '\n'.join(all_results) # Join all of the summaries into one string
            print("Here's the summary of the whole thing: ")
            summarize(all_results, 7)
        
if __name__ == "__main__":
    main()