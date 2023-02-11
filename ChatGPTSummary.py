import openai

# Initialize the API key for OpenAI
openai.api_key = "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"

transcript = "This is a lion. A lion is a beast. They are the kings of the jungle!"

# Define the text to input into the ChatGPT model
text = "Provide a summary: " + transcript

# Use the OpenAI API to generate a response from the ChatGPT model
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=text,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Print the response from the ChatGPT model
print(response["choices"][0]["text"])