import time, traceback
import g4f


def summarizer(prompt, summarize_threshold=100):
    print("Summarization thread started.")
    words_summarized = 0
    try:
        while True:
            with open("files/transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()

            transcript = transcript.split(" ")
            len_transcript = len(transcript)
            print(
                "len_transcript: ",
                len_transcript,
                "   words_summarized: ",
                words_summarized,
            )

            if (
                len_transcript - words_summarized > summarize_threshold
            ):  # It's due for a summary.
                print("Summarizing...")
                # Give it the transcript from the last summary to the current transcript.
                new_transcript = []
                if len_transcript <= 3 * summarize_threshold:
                    new_transcript = transcript
                else:
                    new_transcript = transcript[-3 * summarize_threshold :]
                new_transcript = " ".join(new_transcript)

                summarize(new_transcript, prompt)
                words_summarized = len_transcript

            time.sleep(1)
    except:
        traceback.print_exc()


def summarize(transcript, prompt):
    prompt = prompt.replace("[TRANSCRIPT]", str(transcript))
    print("Prompt: ", prompt)

    # Use the OpenAI API to generate a response from the ChatGPT model
    try:
        summary = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print("Error: ", e)
        summary = "Summarizer unavailable right now."

    print("Summary: ", summary)
    summary = summary.replace("\n\n", "\n")

    with open("files/summary.txt", "a", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")

    return summary


if __name__ == "__main__":
    summarizer(
        "We introduce CLASS TLDR NOTES generation, a new form of extreme summarization of error-prone transcripts of a lecture for a student who isn't listening. CLASS TLDR NOTES generation involves high source compression, removes stop words and summarizes the transcript whilst retaining meaning and insight. The result is the shortest possible note (approx. 3-5 points) that retains all of the original meaning and context of the transcript. The speaker is a teacher.\n\nParagraph:\n\n[TRANSCRIPT]\n\nCLASS TLDR NOTES: "
    )
