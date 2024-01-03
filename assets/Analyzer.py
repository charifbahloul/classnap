import time
import datetime
import traceback
import g4f


def summarizer(prompt, main_logger, summarize_threshold=150):
    # Summarizes by default ~every minute since humans speak ~150 words/min.
    main_logger.info("Summarization thread started.")
    words_summarized = 0

    try:
        while True:
            with open("files/transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()

            transcript = transcript.split(" ")
            len_transcript = len(transcript)

            if (
                len_transcript - words_summarized > summarize_threshold
            ):  # It's due for a summary.
                # Give it the transcript from the last summary to the current transcript.
                new_transcript = []
                if len_transcript <= 3 * summarize_threshold:
                    new_transcript = transcript
                else:
                    new_transcript = transcript[-3 * summarize_threshold :]
                new_transcript = " ".join(new_transcript)

                summarize(new_transcript, prompt, main_logger)
                words_summarized = len_transcript

            time.sleep(1)
    except Exception as e:
        main_logger.error("Summarizer error: " + str(e))


def summarize(transcript, prompt, main_logger):
    prompt = prompt.replace("[TRANSCRIPT]", str(transcript))
    main_logger.info("Prompt: " + str(prompt))
    start = datetime.datetime.now()

    # Use one of the APIs to generate a response from the Gpt3.5 model.
    for i in range(3):
        try:
            summary = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
            )
            break
        except Exception as e:
            main_logger.error("API Error: " + str(e))
            main_logger.error(traceback.format_exc())
            summary = "Summarizer unavailable right now."
            time.sleep(2.5)

    end = datetime.datetime.now()
    duration = end - start
    main_logger.debug("Processing delay: " + str(duration))
    main_logger.info("Summary: " + str(summary))
    summary = summary.replace("\n\n", "\n")

    with open("files/summary.txt", "a", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")

    return summary


if __name__ == "__main__":
    # Direct main_logger to print to console.
    import logging

    main_logger = logging.getLogger("main")
    main_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    main_logger.addHandler(handler)

    summarizer(
        "We introduce CLASS TLDR NOTES generation, a new form of extreme summarization of error-prone transcripts of a lecture for a student who isn't listening. CLASS TLDR NOTES generation involves high source compression, removes stop words and summarizes the transcript whilst retaining meaning and insight. The result is the shortest possible note (approx. 3-5 points) that retains all of the original meaning and context of the transcript. The speaker is a teacher.\n\nParagraph:\n\n[TRANSCRIPT]\n\nCLASS TLDR NOTES: ",
        main_logger,
    )
