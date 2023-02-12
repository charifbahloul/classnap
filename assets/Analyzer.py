import openai, time, re

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
    text = "Assume you are a personal assistant. You are summarizing a part of a lecture for a slacking student who's not paying attention. \nProvide a " + str(num_points) + "-point numbered list with a newline for each point detailing a consise summary of the following transcript: " + str(transcript)

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

def format_contents(contents, type_content):
    if type_content == "summary":
        new_contents = []
        line_num = 0

        for line in contents.split("\n"):
            if line != "":
                new_contents.append(line)

        for line in new_contents:
            if line_num % 3 == 2:
                new_contents[line_num] += "<br>"
            line_num += 1

        contents = "<br>".join(new_contents)
    elif type_content == "transcript":
        contents = contents.split("\n\n")
        contents = [content.replace("\n", " ") for content in contents]
        contents = [content for content in contents if content != ""]

        contents = "<br>".join(contents)
    return contents

def get_file_contents(file_path, type_content="transcript"):
    with open(file_path, "r") as f:
        contents = f.read()
    formatted_contents = format_contents(contents, type_content)
    # Make sure it's not more than 15 lines (measured by <br> tags)
    formatted_contents = formatted_contents.split("<br>")
    if len(formatted_contents) > 15:
        formatted_contents = formatted_contents[-15:]
        formatted_contents = "<br>".join(formatted_contents)
    return formatted_contents

if __name__ == "__main__":
    summarizer()