import time
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
            main_logger.debug(
                "len_transcript: "
                + str(len_transcript)
                + "   words_summarized: "
                + str(words_summarized)
            )

            if (
                len_transcript - words_summarized > summarize_threshold
            ):  # It's due for a summary.
                main_logger.info("Summarizing...")
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

    # Use one of the APIs to generate a response from the Gpt3.5 model.
    try:
        summary = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        main_logger.error("API Error: " + str(e))
        summary = "Summarizer unavailable right now."

    main_logger.info("Summary: " + str(summary))
    summary = summary.replace("\n\n", "\n")

    with open("files/summary.txt", "a", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")

    return summary


# if __name__ == "__main__": # Before uncommenting this, remove main_logger.
# summarizer(
#     "We introduce CLASS TLDR NOTES generation, a new form of extreme summarization of error-prone transcripts of a lecture for a student who isn't listening. CLASS TLDR NOTES generation involves high source compression, removes stop words and summarizes the transcript whilst retaining meaning and insight. The result is the shortest possible note (approx. 3-5 points) that retains all of the original meaning and context of the transcript. The speaker is a teacher.\n\nParagraph:\n\n[TRANSCRIPT]\n\nCLASS TLDR NOTES: "
# )
