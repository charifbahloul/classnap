import tkinter as tk
import time

def update_transcript():
    global transcript_text
    # Open the transcript.txt file and read the contents
    with open("files/transcript.txt", "r") as f:
        transcript = f.read()
    
    transcript = transcript.replace("\n\n", " ")
    
    # Delete the contents of the transcript_text widget
    transcript_text.delete("1.0", tk.END)
    if len(transcript) > 1000: # If the transcript is longer than 1000 characters, take the last 1000 characters
        transcript = transcript[-1000:]
    transcript_text.insert(tk.END, transcript)
    root.after(500, update_transcript)

def update_summary():
    global summary_text
    # Open the summary.txt file and read the contents
    with open("files/summary.txt", "r") as f:
        summary = f.read()

    # summary = summary.replace("\n\n", "\n")
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    root.after(500, update_summary)

def main():
    global root, transcript_text, summary_text
    root = tk.Tk()
    root.title("ClaSSnap")
    root.geometry("1000x720")

    transcript_text = tk.Text(root, height=20, width=50)
    transcript_text.pack(side=tk.LEFT)

    summary_text = tk.Text(root, height=20, width=50)
    summary_text.pack(side=tk.RIGHT)

    # Run the update_transcript function every 2 seconds to update the transcript. Now make sure it runs at 2, 4, 6, 8, 10 seconds.
    root.after(500, update_transcript)
    root.after(500, update_summary)

    root.mainloop()