import openai, time, traceback

def summarizer(api_key, prompt, summarize_threshold=100, max_tokens=70):
    words_transcribed = 0
    try:
        while True:
            with open("files/transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()

            transcript = transcript.split(" ")
            len_transcript = len(transcript)
            print(len_transcript, words_transcribed)
            if len_transcript-words_transcribed > summarize_threshold: # It's due for a summary.
                print("Summarizing...")
                # Give it the transcript from the last summary to the current transcript.
                new_transcript = []
                if len_transcript <= 4*summarize_threshold:
                    new_transcript = transcript
                else:
                    new_transcript = transcript[-4*summarize_threshold:]
                summarize(new_transcript, api_key, prompt, max_tokens=max_tokens)
                words_transcribed = len_transcript
            
            time.sleep(1)
    except:
        traceback.print_exc()

def summarize(transcript, api_key, prompt, max_tokens=70):
    # Get openai api key
    openai.api_key = api_key

    # Use the OpenAI API to generate a response from the ChatGPT model
    try:
        print("prompt: ", prompt.replace("[TRANSCRIPT]", str(transcript)))
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt.replace("[TRANSCRIPT]", str(transcript)),
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.2
        )
        summary = response["choices"][0]["text"]
    except:
        summary = "Summarizer unavailable right now."

    print("summarized")
    summary = summary.replace("\n\n", "\n")

    with open("files/summary.txt", "a", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n\n")

    return summary

if __name__ == "__main__":
    summarizer("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", "We introduce CLASS TLDR NOTES generation, a new form of extreme summarization of very error-prone transcripts for a student who isn't listening. CLASS TLDR NOTES generation involves high source compression, removes stop words and summarizes the very error-prone transcript whilst retaining meaning and insight. The result is the shortest possible note that retains all of the original meaning and context of the error-prone transcript. The speaker is a teacher.\n\nExample\n\nParagraph:\n\n[TRANSCRIPT]\n\n CLASS TLDR NOTES: ")