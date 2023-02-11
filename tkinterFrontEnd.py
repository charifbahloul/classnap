import tkinter as tk
import time

def update_transcript():
    global transcript_text
    # Open the transcript.txt file and read the contents
    with open("transcript.txt", "r") as f:
        transcript = f.read()
    
    # Delete the contents of the transcript_text widget
    transcript_text.delete("1.0", tk.END)
    transcript_text.insert(tk.END, transcript)
    root.after(2000, update_transcript)

def update_summary():
    global summary_text
    # Open the summary.txt file and read the contents
    with open("summary.txt", "r") as f:
        summary = f.read()

    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    root.after(2000, update_summary)

def main():
    global root, transcript_text, summary_text
    root = tk.Tk()
    root.title("ClaSSnap")
    root.geometry("500x500")

    transcript_text = tk.Text(root, height=20, width=50)
    transcript_text.pack(side=tk.LEFT)

    summary_text = tk.Text(root, height=20, width=50)
    summary_text.pack(side=tk.RIGHT)

    # Run the update_transcript function every 2 seconds to update the transcript. Now make sure it runs at 2, 4, 6, 8, 10 seconds.
    root.after(2000, update_transcript)
    root.after(2000, update_summary)

    root.mainloop()