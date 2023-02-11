# Make a tkinter app with a record button that when clicked alters recording.txt to 1.
# When you press it twice, it changes to 0.
# Let there be 2 text boxes next to it that read from transcript.txt and summary.txt respectively every 2 seconds.

import tkinter as tk
import threading
import time
import concurrent.futures

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.recording = False
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def create_widgets(self):
        self.record_button = tk.Button(self, text="Record", command=self.record)
        self.record_button.pack(side="top")

        self.transcript_text = tk.Text(self, width=50, height=10)
        self.transcript_text.pack(side="top")

        self.summary_text = tk.Text(self, width=50, height=10)
        self.summary_text.pack(side="top")

    def record(self):
        if not self.recording:
            self.recording = True
            self.record_button["text"] = "Stop Recording"
            with open("recording.txt", "w") as f:
                f.write("1")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                while self.recording:
                    with open("transcript.txt", "r") as f:
                        self.transcript_text.delete(1.0, tk.END)
                        self.transcript_text.insert(tk.END, f.read())
                    with open("summary.txt", "r") as f:
                        self.summary_text.delete(1.0, tk.END)
                        self.summary_text.insert(tk.END, f.read())
                    time.sleep(2)
        else:
            self.recording = False
            self.record_button["text"] = "Record"
            with open("recording.txt", "w") as f:
                f.write("0")

root = tk.Tk()
app = App(master=root)
app.mainloop()