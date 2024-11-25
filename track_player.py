# Import required modules
import tkinter as tk  # Core tkinter module for GUI creation.
from tkinter import ttk  # ttk module for themed tkinter widgets.
import tkinter.scrolledtext as tkst  # ScrolledText widget for scrollable text areas.
import track_library as lib  # External library for track data management.
import font_manager as fonts  # External library for managing font configurations.

def set_text(text_area, content):
    """
    Utility function to update the content of a given text area widget.
        text_area (tk.Text or tkst.ScrolledText): The widget where content is displayed.
        content (str): The string to be displayed in the widget.
    """
    text_area.delete("1.0", tk.END)  # Clear existing text in the widget.
    text_area.insert(1.0, content)  # Insert new content starting from the top.

class TrackPlayer:
    """
    Main application class for the Track Player GUI.
    """
    def __init__(self, window):
        """
        Initialize the TrackPlayer application and its GUI layout.
            window (tk.Tk): The main application window.
        """
        self.window = window
        self.window.title("Track Player")  # Set the window title.
        self.window.geometry("1200x550")  # Define window size.
        self.window.configure(bg="lightgrey")  # Set the background color.

        fonts.configure()  # Configure fonts using the font_manager module.

        # Configure grid layout for flexible widget placement.
        self.window.grid_rowconfigure((0, 1), weight=1, uniform="row")
        self.window.grid_columnconfigure((0, 1), weight=1, uniform="col")

        # Status label for user feedback.
        self.status_lbl = tk.Label(self.window, text="Welcome to the Track Player!", bg="lightgrey")
        self.status_lbl.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

        # Setup sections for various functionalities.
        self.setup_view_tracks_section(0, 0)  # Section for viewing tracks.
        self.setup_create_playlist_section(0, 1)  # Section for creating playlists.
        self.setup_update_tracks_section(1, 0)  # Section for updating tracks.
        self.setup_search_tracks_section(1, 1)  # Section for searching tracks.

        # Initialize an empty playlist.
        self.playlist = []

        # Automatically click "List All Tracks" when the window opens.
        self.list_tracks_clicked()

    def list_tracks_clicked(self):
        """
        Handles the 'List All Tracks' button click event.
        Retrieves the list of all tracks from the track library and displays it in the text area.
        """
        track_list = lib.list_all()  # Fetch the list of all tracks from the track library.
        set_text(self.list_txt, track_list)  # Display the list in the text area.
        self.status_lbl.configure(text="List Tracks button was clicked!")  # Update the status label.

    def setup_view_tracks_section(self, row, col):
        """
        Create the "View Tracks" section in the GUI.
            row (int): Row position in the grid layout.
            col (int): Column position in the grid layout.
        """
        view_frame = tk.LabelFrame(self.window, text="View Tracks", bg="lightgrey", padx=5, pady=5)
        view_frame.grid(row=row, column=col, padx=5, pady=7, sticky="nsew")

        # Button to list all tracks.
        tk.Button(view_frame, text="List All Tracks", command=self.list_tracks_clicked).grid(row=0, column=0, padx=5, pady=2)
        # Input field and button to view details of a specific track.
        tk.Label(view_frame, text="Track Number:").grid(row=0, column=1, padx=5, pady=2)
        self.input_txt = tk.Entry(view_frame, width=5)
        self.input_txt.grid(row=0, column=2, padx=5, pady=2)
        tk.Button(view_frame, text="View", command=self.view_tracks_clicked).grid(row=0, column=3, padx=5, pady=2)

        # Text areas for displaying the list of tracks and track details.
        self.list_txt = tk.Text(view_frame, width=40, height=8, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, padx=5, pady=3)
        self.track_txt = tk.Text(view_frame, width=20, height=5, wrap="none")
        self.track_txt.grid(row=1, column=3, padx=5, pady=3)

    def setup_create_playlist_section(self, row, col):
        """
        Create the "Create Playlist" section in the GUI.
            row (int): Row position in the grid layout.
            col (int): Column position in the grid layout.
        """
        playlist_frame = tk.LabelFrame(self.window, text="Create Playlist", bg="lightgrey", padx=5, pady=5)
        playlist_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Input field and buttons for managing playlists.
        tk.Label(playlist_frame, text="Track Number:").grid(row=0, column=0, padx=5, pady=2)
        self.track_number_entry = tk.Entry(playlist_frame, width=5)
        self.track_number_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Button(playlist_frame, text="Add", command=self.add_track).grid(row=0, column=2, padx=5, pady=2)
        tk.Button(playlist_frame, text="Play", command=self.play_playlist).grid(row=0, column=3, padx=5, pady=2)
        tk.Button(playlist_frame, text="Reset", command=self.reset_playlist).grid(row=0, column=4, padx=5, pady=2)

        # Scrollable text area for displaying the playlist.
        self.playlist_text_area = tkst.ScrolledText(playlist_frame, width=60, height=8, wrap="none")
        self.playlist_text_area.grid(row=1, column=0, columnspan=5, padx=5, pady=2)

    def setup_update_tracks_section(self, row, col):
        """
        Create the "Update Tracks" section in the GUI.

        Args:
            row (int): Row position in the grid layout.
            col (int): Column position in the grid layout.
        """
        update_frame = tk.LabelFrame(self.window, text="Update Tracks", bg="lightgrey", padx=5, pady=5)
        update_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Input fields and button for updating track ratings.
        tk.Label(update_frame, text="Track Number:").grid(row=0, column=0, padx=5, pady=2)
        self.update_track_number_entry = tk.Entry(update_frame, width=5)
        self.update_track_number_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(update_frame, text="New Rating:").grid(row=0, column=2, padx=5, pady=2)
        self.new_rating_entry = tk.Entry(update_frame, width=5)
        self.new_rating_entry.grid(row=0, column=3, padx=5, pady=2)
        tk.Button(update_frame, text="Update", command=self.update_rating).grid(row=0, column=4, padx=5, pady=2)

        # Scrollable text area for displaying the result of updates.
        self.update_text_area = tkst.ScrolledText(update_frame, width=60, height=8, wrap="none")
        self.update_text_area.grid(row=1, column=0, columnspan=5, padx=5, pady=2)

    def setup_search_tracks_section(self, row, col):
        """
        Create the "Search Tracks" section in the GUI.
            row (int): Row position in the grid layout.
            col (int): Column position in the grid layout.
        """
        search_frame = tk.LabelFrame(self.window, text="Search Tracks", bg="lightgrey", padx=5, pady=5)
        search_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Input field and button for searching tracks.
        tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=2)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Button(search_frame, text="Find", command=self.search_tracks).grid(row=0, column=2, padx=5, pady=2)

        # Scrollable text area for displaying search results.
        self.search_results_text = tkst.ScrolledText(search_frame, width=60, height=8, wrap="none")
        self.search_results_text.grid(row=1, column=0, columnspan=3, padx=5, pady=2)

    def list_tracks_clicked(self):
        """
        Handles the 'List All Tracks' button click event.
        Retrieves the list of all tracks from the track library and displays it in the text area.
        """
        track_list = lib.list_all()  # Fetch the list of all tracks from the track library.
        set_text(self.list_txt, track_list)  # Display the list in the text area.
        self.status_lbl.configure(text="List Tracks button was clicked!")  # Update the status label.

    def view_tracks_clicked(self):
        """
        Handles the 'View' button click event for a specific track.
        Displays details of the track corresponding to the entered track number.
        """
        key = self.input_txt.get()  # Get the track number from the input field.
        name = lib.get_name(key)  # Retrieve the name of the track.

        if name is not None:
            # If the track exists, retrieve and format its details.
            artist = lib.get_artist(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            track_details = f"{name}\n{artist}\nrating: {rating} plays: {play_count}"
            set_text(self.track_txt, track_details)  # Display the track details.
        else:
            # Display an error message if the track does not exist.
            set_text(self.track_txt, f"Track {key} not found")

        self.status_lbl.configure(text="View Track button was clicked!")  # Update the status label.

    def add_track(self):
        """
        Handles the 'Add' button click event for adding a track to the playlist.
        Validates the track number and updates the playlist if the track is valid.
        """
        track_number = self.track_number_entry.get()  # Get the track number from the input field.

        if not track_number:
            # Display an error message if no track number is entered.
            self.display_message("Error: Track number cannot be empty.", self.playlist_text_area)
            return

        track_name = lib.get_name(track_number)  # Retrieve the name of the track.

        if track_name:
            # If the track exists, add it to the playlist and update the display.
            self.playlist.append(track_number)
            self.update_playlist_display()
        else:
            # Display an error message if the track number is invalid.
            self.display_message("Error: Invalid track number.", self.playlist_text_area)

    def play_playlist(self):
        """
        Handles the 'Play' button click event to play all tracks in the playlist.
        Validates each track, increments its play count, and displays a summary.
        """
        if not self.playlist:
            # Display an error message if the playlist is empty.
            self.display_message("Error: Playlist is empty. Add tracks first.", self.playlist_text_area)
            return

        tracks_played = 0  # Counter for successfully played tracks.

        for track_number in self.playlist:
            if lib.get_name(track_number) is not None:
                # Increment the play count for valid tracks.
                lib.increment_play_count(track_number)
                tracks_played += 1
            else:
                # Display a warning if a track is invalid and skip it.
                self.display_message(f"Warning: Track {track_number} does not exist and was skipped.", self.playlist_text_area)

        if tracks_played > 0:
            # Display the number of successfully played tracks.
            self.display_message(f"{tracks_played} track(s) played successfully.", self.playlist_text_area)

        self.update_playlist_display()  # Update the playlist display.

    def reset_playlist(self):
        """
        Handles the 'Reset' button click event to clear the playlist.
        """
        self.playlist.clear()  # Clear all tracks from the playlist.
        self.display_message("Playlist reset.", self.playlist_text_area)  # Update the user with a reset message.

    def update_playlist_display(self):
        """
        Updates the text area to show the current playlist with track details.
        """
        content = "Current Playlist:\n"  # Initialize the display content.

        for track_number in self.playlist:
            track_name = lib.get_name(track_number)  # Retrieve the name of the track.

            if track_name:
                # If the track exists, format its details.
                artist = lib.get_artist(track_number)
                rating = lib.get_rating(track_number)
                play_count = lib.get_play_count(track_number)
                content += f"{track_name} by {artist} - {rating} stars, Played {play_count} times\n"
            else:
                # Append a message for invalid tracks.
                content += f"Track {track_number} not found.\n"

        # Update the playlist text area with the formatted content.
        self.playlist_text_area.delete(1.0, tk.END)
        self.playlist_text_area.insert(tk.END, content)

    def update_rating(self):
        """
        Handles the 'Update' button click event to update the rating of a track.
        Validates the input and updates the track rating if valid.
        """
        track_number = self.update_track_number_entry.get()  # Get the track number from the input field.
        new_rating = self.new_rating_entry.get()  # Get the new rating from the input field.

        if not new_rating.isdigit() or not (1 <= int(new_rating) <= 5):
            # Display an error message if the rating is invalid.
            self.display_message("Error: Rating must be a number between 1 and 5.", self.update_text_area)
            return

        if lib.get_name(track_number) is not None:
            # Update the track's rating and display its details.
            lib.set_rating(track_number, int(new_rating))
            play_count = lib.get_play_count(track_number)
            content = f"Name: {lib.get_name(track_number)}\n New Rating: {new_rating} stars\n Play Count: {play_count}"
            self.display_message(content, self.update_text_area)
        else:
            # Display an error message if the track number is invalid.
            self.display_message("Error: Invalid track number.", self.update_text_area)

    def search_tracks(self):
        """
        Handles the 'Find' button click event to search for tracks based on a query.
        Displays a list of matching tracks or an appropriate message if no matches are found.
        """
        query = self.search_entry.get().lower().strip()  # Get and normalize the search query.

        self.search_results_text.delete("1.0", tk.END)  # Clear previous search results.

        if not query:
            # Display an error message if no query is entered.
            self.search_results_text.insert(tk.END, "Please enter a search term.\n")
            return

        matching_tracks = []  # List to hold matching tracks.

        for track_id in lib.list_all().splitlines():
            # Extract the track ID and details from the track list.
            track_id = track_id.split()[0]
            name = lib.get_name(track_id).lower() if lib.get_name(track_id) else ""
            artist = lib.get_artist(track_id).lower() if lib.get_artist(track_id) else ""

            if query in name or query in artist:
                # Add matching tracks to the list.
                matching_tracks.append(f"Track ID: {track_id}, Name: {name}, Artist: {artist}")

        if matching_tracks:
            # Display all matching tracks.
            for track_info in matching_tracks:
                self.search_results_text.insert(tk.END, track_info + "\n")
        else:
            # Display a message if no tracks match the query.
            self.search_results_text.insert(tk.END, "No matching tracks found.\n")

    def display_message(self, message, text_area):
        """
        Utility method to display a message in a given text area.
            message (str): The message to display.
            text_area (tk.Text or tkst.ScrolledText): The widget where the message is displayed.
        """
        text_area.delete("1.0", tk.END)  # Clear the text area.
        text_area.insert(tk.END, f"{message}\n")  # Insert the message.
    
if __name__ == "__main__":
    window = tk.Tk()
    app = TrackPlayer(window)
    window.mainloop()
