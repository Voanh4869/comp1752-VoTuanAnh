import tkinter as tk
import tkinter.scrolledtext as tkst

# Importing track library for accessing track information and font manager for styling
import track_library as lib
import font_manager as fonts
 

def set_text(text_area, content):
    """
    Sets the content of the text area widget.
    
    Parameters:
    text_area (tk.Text): The text widget where the content will be displayed.
    content (str): The text content to be inserted into the text area.
    """
    # Clear the current content of the text area
    text_area.delete("1.0", tk.END)
    # Insert new content starting from the first line
    text_area.insert(1.0, content)


class TrackViewer():
    def __init__(self, window):
        # Set window geometry and title
        window.geometry("750x350")
        window.title("View Tracks")

        # Button to list all tracks
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Label and input field to enter a track number
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)
        
        # Button to view a specific track by its number
        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Scrollable text area for displaying track details
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Scrollable text area for displaying track details
        self.track_txt = tk.Text(window, width=24, height=4, wrap="none")
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.list_tracks_clicked()

    def view_tracks_clicked(self):
        """
        Event handler for the "View Track" button.
        Retrieves and displays details of a specific track based on user input.
        """
        key = self.input_txt.get()
        name = lib.get_name(key) # Attempt to retrieve the track details from the library
        if name is not None:  # If track is found, format the details for display
            artist = lib.get_artist(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}" # Display detailed information about the track
            set_text(self.track_txt, track_details)
        else:
            set_text(self.track_txt, f"Track {key} not found") # Display a message if the track was not found
        self.status_lbl.configure(text="View Track button was clicked!")

    def list_tracks_clicked(self):
        track_list = lib.list_all() # Retrieve all track details from the library
        set_text(self.list_txt, track_list)
        self.status_lbl.configure(text="List Tracks button was clicked!")

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    TrackViewer(window)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
