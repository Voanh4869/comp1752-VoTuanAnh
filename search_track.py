import tkinter as tk
from track_library import list_all, get_name, get_artist

class TrackSearch:
    def __init__(self, window):
        self.window = window
        self.window.title("Jukebox - Search Tracks")

        # Search input field
        self.search_label = tk.Label(window, text="Search Tracks:")
        self.search_label.pack(pady=6)
        
        self.search_entry = tk.Entry(window, width=50)
        self.search_entry.pack(pady=6)

        # Search button
        self.search_button = tk.Button(window, text="Search", command=self.search_tracks)
        self.search_button.pack(pady=5)

        # Results area
        self.results_text = tk.Text(window, width=60, height=15, state=tk.DISABLED)
        self.results_text.pack(pady=10)

        # Clear search button
        self.clear_button = tk.Button(window, text="Clear", command=self.clear_results)
        self.clear_button.pack(pady=5)

    def search_tracks(self):
        # Get the search query
        query = self.search_entry.get().lower().strip()

        # Clear previous results
        self.clear_results()

        # If query is empty, do nothing
        if not query:
            return

        # List to hold matching tracks based on the search query
        matching_tracks = []
        for track_id in list_all().splitlines():
            # Extract track details using the library functions
            track_id = track_id.split()[0]  # Get the track ID from the list_all output
            name = get_name(track_id).lower() if get_name(track_id) else ""
            artist = get_artist(track_id).lower() if get_artist(track_id) else ""

            # Check if the query is in the track's name or artist
            if query in name or query in artist:
                matching_tracks.append(f"Track ID: {track_id}, Name: {name}, Artist: {artist}")

        # Display the results
        self.results_text.config(state=tk.NORMAL)
        if matching_tracks:
            for track_info in matching_tracks:
                # Insert each matching track's information into the results_text widget
                self.results_text.insert(tk.END, track_info + "\n")
        else:
            # If no tracks match the query, display a message indicating that
            self.results_text.insert(tk.END, "No matching tracks found.")
            # Disable the results_text widget to prevent further modification
        self.results_text.config(state=tk.DISABLED)

    def clear_results(self):
        # Clear the results text area
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)

# Main application
if __name__ == "__main__":
    window = tk.Tk()
    app = TrackSearch(window)
    window.mainloop()
