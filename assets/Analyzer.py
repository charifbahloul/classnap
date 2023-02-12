import openai, whisper, time

def summarizer():
    words_transcribed = 0
    while True:
        with open("files/transcript.txt", "r") as f:
            transcript = f.read()

        transcript = transcript.split(" ")
        len_transcript = len(transcript)
        print("Summary: " + str(len_transcript))

        if len_transcript-words_transcribed > 100: # It's due for a summary.
            print("Summarizing...")
            summarize(transcript[words_transcribed:])
            words_transcribed = len_transcript
        
        time.sleep(1)


def summarize(transcript, num_points=3):
    # Open keys.txt and read the first line
    with open("files/keys.txt", "r") as f:
        openai.api_key = f.readline()

    # Define the text to input into the ChatGPT model
    text = "Assume you are a personal assistant. You are summarizing a part of a lecture for a student who's not paying attention. \nProvide a " + str(num_points) + "-point list with a consise summary of the following transcript: " + str(transcript)

    # Use the OpenAI API to generate a response from the ChatGPT model
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.2,
        )
        summary = response["choices"][0]["text"]
    except:
        summary = "Summarizer unavailable right now."

    print("summarized")

    with open("files/summary.txt", "a") as f:
        f.write(summary)
        f.write("\n\n")

    return summary

def clear_files():
    # Clear the transcript.txt file
    with open("files/transcript.txt", "w") as f:
        # f.write("First recording...\n\n")
        f.write("")
    # Clear the summary.txt file
    with open("files/summary.txt", "w") as f:
        # f.write("First recording...\n\n")
        f.write("")

def get_file_contents(file_path, replace=True):
    with open(file_path, "r") as f:
        contents = f.read()
    if replace:
        return contents.replace("\n\n", "\n")
    else:
        return contents

if __name__ == "__main__":
    summarizer()