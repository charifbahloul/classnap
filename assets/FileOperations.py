import json

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

def get_file_contents(file_path, type_content="transcript", max_lines=15):
    with open(file_path, "r") as f:
        contents = f.read()
    formatted_contents = format_contents(contents, type_content)
    # Make sure it's not more than 15 lines (measured by <br> tags)
    formatted_contents = formatted_contents.split("<br>")
    if len(formatted_contents) > max_lines:
        formatted_contents = formatted_contents[-max_lines:]
    return "<br>".join(formatted_contents)

def open_settings():
    with open("files/settings.json", "r") as f:
        settings = json.load(f)

    return settings

def get_settings():
    settings = open_settings()

    print(settings) # Dict
    # Assign the settings to variables with the appropriate type.
    for setting in settings.keys():
        if type(settings[setting]) == int:
            globals()[setting] = int(settings[setting])
        else:
            globals()[setting] = settings[setting]

    with open("files/keys.txt", "r") as f:
        globals()["api_key"] = f.readline()