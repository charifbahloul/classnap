import time, traceback
import g4f


def summarizer(api_key, prompt, summarize_threshold=100):
    print("hi")
    print("Summarization thread started.")
    try:
        while True:
            with open("files/transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()
            words_summarized = transcript.split("\n")[0]

            transcript = transcript.split(" ")
            len_transcript = len(transcript)
            print(len_transcript)
            if len_transcript-words_summarized > summarize_threshold: # It's due for a summary.
                print("Summarizing...")
                # Give it the transcript from the last summary to the current transcript.
                new_transcript = []
                if len_transcript <= 4*summarize_threshold:
                    new_transcript = transcript
                else:
                    new_transcript = transcript[-4*summarize_threshold:]
                new_transcript = " ".join(new_transcript)
                summarize(chatbot, new_transcript, prompt)
                words_summarized = len_transcript

            
            time.sleep(1)
    except:
        traceback.print_exc()

def summarize(chatbot, transcript, prompt):
    prompt = prompt.replace("[TRANSCRIPT]", str(transcript))

    # Use the OpenAI API to generate a response from the ChatGPT model
    try:
        print("prompt: ", prompt)
        for data in chatbot.ask(prompt):
            summary = data["message"]

    except Exception as e:
        print("Error: ", e)
        summary = "Summarizer unavailable right now."

    print("Summary: ", summary)
    summary = summary.replace("\n\n", "\n")

    with open("files/summary.txt", "a", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")

    return summary

def once_summarized(words_summarized, summary):
    # words_summarized should become the new first line.
    with open("files/transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    transcript = transcript.split("\n")
    transcript[0] = str(words_summarized)

    with open("files/transcript.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(transcript))

if __name__ == "__main__":
    summarizer("your-session-token", "We introduce CLASS TLDR NOTES generation, a new form of extreme summarization of error-prone transcripts of a lecture for a student who isn't listening. CLASS TLDR NOTES generation involves high source compression, removes stop words and summarizes the transcript whilst retaining meaning and insight. The result is the shortest possible note (approx. 3-5 points) that retains all of the original meaning and context of the transcript. The speaker is a teacher.\n\nParagraph:\n\n[TRANSCRIPT]\n\nCLASS TLDR NOTES: ")