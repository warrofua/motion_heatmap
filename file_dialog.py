import tkinter as tk
from tkinter import filedialog

def select_video_file():
    # Initialize Tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open file dialog to select a video file
    file_path = filedialog.askopenfilename(title="Select Video File", 
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mov")])

    # Close the Tkinter window
    root.destroy()

    return file_path
