import openai, whisper

WAVE_OUTPUT_FILENAME = "output.wav"

def load_model(model_name):
    model = whisper.load_model(model_name)
    return model

def whisperStuff(model):
    # Read the audio data from the file into a numpy array
    print("Begin whisper.")
    result = model.transcribe(WAVE_OUTPUT_FILENAME, language = "english")["text"]
    # print(result)
    print("End whisper.")
    return result

def summarize(transcript, num_points=3):
    # Initialize the API key for OpenAI

    # Open keys.txt and read the first line
    with open("keys.txt", "r") as f:
        openai.api_key = f.readline()

    # Define the text to input into the ChatGPT model
    text = "Assume you are a personal assistant. You are summzarizing a part of a lecture for your boss. \nProvide a " + str(num_points) + "-point list with a consise summary of the following transcript: " + transcript

    # Use the OpenAI API to generate a response from the ChatGPT model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.3,
    )

    return response["choices"][0]["text"]


def analyze(model_name="base.en"):
    model = load_model(model_name)
    result = whisperStuff(model)
    print(result)
    # Save the transcript to a text file
    with open("transcript.txt", "a") as f:
        f.write(result)

    summary = summarize(result)
    print(summary)
    # Save the summary to a text file
    with open("summary.txt", "a") as f:
        f.write(summary)
    return summary