import tkinter as tk
import tkinter.scrolledtext as tkst
import font_manager as fonts
import track_library as lib  # Use the functions from the original track_library.py

class UpdateTracks:
    def __init__(self, window):
        """
        Initializes the UpdateTracksApp class and sets up the GUI elements.
        Parameters:
        window (tk.Tk): The main window where the GUI is displayed.
        """
        self.window = window
        self.window.geometry("750x300")
        self.window.title("Update Track Rating")

        # Entry for track number
        tk.Label(self.window, text="Enter Track Number:").grid(row=0, column=0, padx=10, pady=10)
        self.track_number_entry = tk.Entry(self.window)
        self.track_number_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entry for new rating
        tk.Label(self.window, text="Enter New Rating:").grid(row=1, column=0, padx=10, pady=10)
        self.new_rating_entry = tk.Entry(self.window)
        self.new_rating_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button to update track rating
        tk.Button(self.window, text="Update Rating", command=self.update_rating).grid(row=2, column=0, padx=10, pady=10)

        # Scrolled text area to display results
        self.text_area = tkst.ScrolledText(self.window, width=85, height=10)
        self.text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def update_rating(self):
        """
        Updates the rating for the specified track.
        """
        track_number = self.track_number_entry.get()
        new_rating = self.new_rating_entry.get()

        # Validate the rating input (must be between 1 and 5)
        if not new_rating.isdigit() or not (1 <= int(new_rating) <= 5):
            self.display_message("Error: Rating must be a number between 1 and 5.")
            return

        # Check if the track exists
        if lib.get_name(track_number) is not None:
            lib.set_rating(track_number, int(new_rating))  # Update the track's rating
            play_count = lib.get_play_count(track_number) # Get the updated play count
            content = f"Updated Track:\nName: {lib.get_name(track_number)}\nNew Rating: {new_rating} stars\nPlay Count: {play_count}\n"
            self.display_message(content)
        else:
            self.display_message("Error: Invalid track number.")

    def display_message(self, message):
        """
        Displays a message in the text area.
        """
        self.text_area.delete(1.0, tk.END) # Clear previous messages
        self.text_area.insert(tk.END, f"{message}\n") # Insert the new message

# Main code to run the application
if __name__ == "__main__":
    window = tk.Tk()
    app = UpdateTracks(window)
    window.mainloop()
