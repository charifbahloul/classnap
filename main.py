from Recorder import record
from Analyzer import analyze, summarize
import concurrent.futures

RECORD_LENGTH = 90
MODEL_NAME = "base.en"

def main():
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            while True:
                record(RECORD_LENGTH)

                # print("Simulating recording...")
                # time.sleep(5)
            
                future = executor.submit(analyze, MODEL_NAME)
                futures.append(future)

                # analyze()
                # all_results.append(future.result())
                # print(future.result())
        except KeyboardInterrupt:
            # executor.shutdown(wait=False)
            all_results = []
            for future in concurrent.futures.as_completed(futures):
                all_results.append(future.result())
            all_results = '\n'.join(all_results)
            print("Here's the summary of the whole thing: ")
            summarize(all_results, 7)
        
if __name__ == "__main__":
    main()