import json

def clear_files():
    # Clear the transcript.txt file
    with open("files/transcript.txt", "w", encoding="utf-8") as f:
        # f.write("First recording...\n\n")
        f.write("")
    # Clear the summary.txt file
    with open("files/summary.txt", "w", encoding="utf-8") as f:
        # f.write("First recording...\n\n")
        f.write("")

def format_contents(contents, type_content):
    if type_content == "summary":
        # Convert newlines to <br> tags
        contents = contents.replace("\n", "<br>")
        contents = contents.split("<br>")
        
        # Flip the order of the summary
        contents = contents[::-1]

        contents = "<br><br>".join(contents)

    elif type_content == "transcript":
        contents = contents.split("\n")
        contents = [content.replace("\n", " ") for content in contents]
        contents = [content for content in contents if content != ""]
        
        # Flip the order of the transcript
        contents = contents[::-1]

        contents = "<br><br>".join(contents)
    return contents

def get_file_contents(file_path, type_content="transcript"):
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()
    formatted_contents = format_contents(contents, type_content)
    # Make sure it's not more than 500 words
    formatted_contents = formatted_contents.split(" ")
    return " ".join(formatted_contents)

def open_settings():
    with open("files/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    return settings

def get_settings():
    settings = open_settings()

    # Assign the settings to variables with the appropriate type.
    for setting in settings.keys():
        if type(settings[setting]) == int:
            globals()[setting] = int(settings[setting])
        elif type(settings[setting]) == "True" or type(settings[setting]) == "False":
            globals()[setting] = bool(settings[setting])
        elif type(settings[setting]) == float:
            globals()[setting] = float(settings[setting])
        else:
            globals()[setting] = settings[setting]

    globals()["openai_api_key"] = decode_api_key(globals()["openai_api_key_encoded"])
    globals()["deepgram_api_key"] = decode_api_key(globals()["deepgram_api_key_encoded"])

def encode_api_key(api_key): # Basic encoding so that the api key isn't visible in the code.
    api_key = [ord(c) for c in api_key]

    for a, y in enumerate(api_key):
        api_key[a] = y ** 2
    
    return api_key

def decode_api_key(api_key):
    for a, y in enumerate(api_key):
        api_key[a] = int(y ** 0.5)
    
    api_key = [chr(c) for c in api_key]

    return "".join(api_key)

if __name__ == "__main__":
    get_settings()