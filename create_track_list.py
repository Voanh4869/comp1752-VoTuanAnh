import tkinter as tk
import tkinter.scrolledtext as tkst
import track_library as lib  # Use the functions from the original track_library.py

class CreateTrackList:
    def __init__(self, window):
        """
        Initializes the CreateTrackListApp class and sets up the GUI elements.
        Parameters:
        window (tk.Tk): The main window where the GUI is displayed.
        """
        self.window = window
        self.window.geometry("750x400")
        self.window.title("Create Track List")

        # Initialize playlist
        self.playlist = []

        # Entry for track number
        tk.Label(self.window, text="Enter Track Number:").grid(row=0, column=0, padx=10, pady=10)
        self.track_number_entry = tk.Entry(self.window)
        self.track_number_entry.grid(row=0, column=1, padx=10, pady=10)

        # Buttons for adding, playing, and resetting the playlist
        tk.Button(self.window, text="Add to Playlist", command=self.add_track).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.window, text="Play Playlist", command=self.play_playlist).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.window, text="Reset Playlist", command=self.reset_playlist).grid(row=1, column=1, padx=10, pady=10)

        # Scrolled text area to display the playlist
        self.text_area = tkst.ScrolledText(self.window, width=85, height=15)
        self.text_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def add_track(self):
        """
        Adds a track to the playlist if valid.
        """
        track_number = self.track_number_entry.get()
        if not track_number: # Check if the input is empty
            self.display_message("Error: Track number cannot be empty.")
            return
        
        track_name = lib.get_name(track_number)

        # Check if the track exists
        if track_name is not None:
            self.playlist.append(track_number) # Add track to the playlist
            self.display_message(f"Track added: {track_name}")
            self.update_playlist_display() # Update the display to show the new playlist
        else:
            self.display_message("Error: Invalid track number.")

    def play_playlist(self):
        """
        Simulates playing the playlist by incrementing play counts.
        """
        if not self.playlist: # Check if the playlist is empty
            self.display_message("Error: Playlist is empty. Add tracks first.")
            return

        # Keep track of the number of tracks successfully played
        tracks_played = 0

        for track_number in self.playlist:
            # Check if the track exists before incrementing play count
            if lib.get_name(track_number) is not None:
                lib.increment_play_count(track_number) # Increment the play count
                tracks_played += 1
            else:
                self.display_message(f"Warning: Track {track_number} does not exist and was skipped.")

        if tracks_played > 0:
            self.display_message(f"{tracks_played} track(s) played successfully.")
        else:
            self.display_message("No valid tracks found to play.")
        self.update_playlist_display()  # Update the display to reflect the new play counts

    def reset_playlist(self):
        """
        Clears the playlist and resets the display.
        """
        self.playlist.clear() # Empty the playlist
        self.display_message("Playlist reset.")
        self.update_playlist_display() # Update the display to show the empty playlist


    def update_playlist_display(self):
        """
        Updates the text area to show the current playlist.
        """
        content = "Current Playlist:\n"
        for track_number in self.playlist:
            track_name = lib.get_name(track_number)
            if track_name is not None:
                artist = lib.get_artist(track_number)
                rating = lib.get_rating(track_number)
                play_count = lib.get_play_count(track_number)
                content += f"{track_name} by {artist} - {rating} stars, Played {play_count} times\n"
            else:
                content += f"Track {track_number} not found.\n"
        self.text_area.delete(1.0, tk.END) # Clear previous content
        self.text_area.insert(tk.END, content) # Insert updated content

    def display_message(self, message):
        """
        Displays a message in the text area.
        """
        self.text_area.insert(tk.END, f"{message}\n")

# Main code to run the application
if __name__ == "__main__":
    window = tk.Tk()
    app = CreateTrackList(window)
    window.mainloop()
