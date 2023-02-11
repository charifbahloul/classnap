import openai

def summarize(transcript):
    # Initialize the API key for OpenAI

    # Open keys.txt and read the first line
    with open("keys.txt", "r") as f:
        openai.api_key = f.readline()

    # Define the text to input into the ChatGPT model
    text = "Provide a 3-point very consise summary of the following transcript: " + transcript

    # Use the OpenAI API to generate a response from the ChatGPT model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response["choices"][0]["text"]