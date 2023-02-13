import openai, time

def summarizer(api_key, summarize_threshold=100, max_tokens=70, max_lines=3):
    words_transcribed = 0
    while True:
        with open("files/transcript.txt", "r") as f:
            transcript = f.read()

        transcript = transcript.split(" ")
        len_transcript = len(transcript)

        if len_transcript-words_transcribed > summarize_threshold: # It's due for a summary.
            print("Summarizing...")
            summarize(transcript[words_transcribed:], api_key, num_points=max_lines, max_tokens=max_tokens)
            words_transcribed = len_transcript
        
        time.sleep(1)


def summarize(transcript, api_key, num_points=3, max_tokens=70):
    # Get openai api key
    openai.api_key = api_key

    # Define the text to input into the ChatGPT model
    text = "Assume you are a personal assistant. You are summarizing a part of a lecture for a slacking student who's not paying attention. \nProvide a " + str(num_points) + "-point numbered list with a newline for each point detailing a consise summary of the following transcript (which is error-prone): " + str(transcript)

    # Use the OpenAI API to generate a response from the ChatGPT model
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.2
        )
        summary = response["choices"][0]["text"]
    except:
        summary = "Summarizer unavailable right now."

    print("summarized")

    with open("files/summary.txt", "a") as f:
        f.write(summary)
        f.write("\n\n")

    return summary

if __name__ == "__main__":
    summarizer()