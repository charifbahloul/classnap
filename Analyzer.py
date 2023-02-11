import openai, whisper

WAVE_OUTPUT_FILENAME = "output.wav"
model = whisper.load_model("base.en")


def whisperStuff():
    # Read the audio data from the file into a numpy array
    result = model.transcribe(WAVE_OUTPUT_FILENAME, language = "english")["text"]
    # print(result)

    return result

def summarize(transcript, num_points=3):
    # Initialize the API key for OpenAI

    # Open keys.txt and read the first line
    with open("keys.txt", "r") as f:
        openai.api_key = f.readline()

    # Define the text to input into the ChatGPT model
    text = "Provide a " + str(num_points) + "-point very consise summary of the following transcript: " + transcript

    # Use the OpenAI API to generate a response from the ChatGPT model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.4,
    )

    return response["choices"][0]["text"]


def analyze():
    result = whisperStuff()
    summary = summarize(result)
    print(summary)
    return summary