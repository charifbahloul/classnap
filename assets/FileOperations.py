import json
import logging


def clear_files():
    # Move the summary.txt file to the old_summaries.txt file.
    with open("files/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()

    if summary != "":
        with open("files/old_summaries.txt", "a", encoding="utf-8") as f:
            f.write(summary)
            f.write("\n\n")

    # Move the transcript.txt file to the old_transcripts.txt file.
    with open("files/transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    # Check if the transcript is just composed of spaces and newlines.
    is_empty = True
    for char in transcript:
        if char != " " and char != "\n":
            is_empty = False
            break

    if not is_empty:
        with open("files/old_transcripts.txt", "a", encoding="utf-8") as f:
            f.write(transcript)
            f.write("\n\n")

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
        contents = contents.split("\n")

        contents = [content.replace("\n", " ") for content in contents]
        contents = [content for content in contents if content != ""]

        # Flip the order of the summary
        contents = contents[::-1]

        while len(contents) > 0 and contents[0] == " ":
            contents = contents[1:]

        contents = "<br>".join(contents)

    elif type_content == "transcript":
        contents = contents.split("\n")
        contents = [content.replace("\n", " ") for content in contents]
        contents = [content for content in contents if content != ""]

        # Flip the order of the transcript
        contents = contents[::-1]
        while len(contents) > 0 and contents[0] == " ":
            contents = contents[1:]

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

    globals()["deepgram_api_key"] = decode_api_key(
        globals()["deepgram_api_key_encoded"]
    )


def encode_api_key(
    api_key,
):  # Basic encoding so that the api key isn't visible in the code.
    api_key = [ord(c) for c in api_key]

    for a, y in enumerate(api_key):
        api_key[a] = y**2

    return api_key


def decode_api_key(api_key):
    for a, y in enumerate(api_key):
        api_key[a] = int(y**0.5)

    api_key = [chr(c) for c in api_key]

    return "".join(api_key)


def setup_logger(name, log_file, level=logging.DEBUG, include_level=True):
    # To setup as many loggers as you want.
    if include_level:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    else:
        formatter = logging.Formatter("%(asctime)s- %(message)s")
    handler = logging.FileHandler(log_file, "a", "utf-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    get_settings()
