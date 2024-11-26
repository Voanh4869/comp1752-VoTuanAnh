import tkinter as tk
from tkinter import ttk, messagebox
import pygame  # Library for sound playback
from PIL import Image, ImageTk  # For image manipulation
from mutagen.mp3 import MP3  # For getting metadata like song length
import os  # To handle file paths and directories
import time  # For tracking playtime and formatting time


class MusicPlayer:
    def __init__(self, window):
        """
        Initializes the Music Player application, including its GUI and core functionality.
        Sets up the window properties, state variables, folder paths, and audio system.
        """
        self.window = window
        self.window.title("MP3 Player")  # Sets the title of the main window
        self.window.geometry("1000x600")  # Sets the initial size of the window

        # Initializes the Pygame mixer, which handles audio playback
        pygame.mixer.init()

        # Paths for required resources such as music files and control button icons
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory of the script
        self.PICTURES_FOLDER = os.path.join(self.BASE_DIR, "Icon buttons")  # Folder for button images
        self.MUSIC_FOLDER = os.path.join(self.BASE_DIR, "MusicPlayer")  # Folder for MP3 files

        # State variables for player status
        self.stopped = False  # Indicates if playback has been stopped
        self.paused = False  # Indicates if playback is currently paused
        self.song_length = 0  # Total length of the currently loaded song in seconds
        self.start_time = None  # Tracks the time when the song started playing

        # Variables for the GUI sliders
        self.slider_value = tk.DoubleVar()  # Controls the song playback position
        self.volume_value = tk.DoubleVar(value=50)  # Default volume set to 50%

        # Mapping of song display names (shown to the user) to their respective file names
        self.song_mapping = {}

        # Build the graphical user interface (GUI)
        self.create_widgets()

        # Populate the folder playlist with available MP3 files
        self.load_songs()

    def create_widgets(self):
        """
        Creates and arranges all GUI components, including playlists, control buttons, sliders, 
        and the status bar.
        """
        # Main layout frame for organizing the left and right panels
        main_frame = tk.Frame(self.window)
        main_frame.pack(pady=20, fill="both", expand=True)

        # Left frame: Contains the folder playlist and search bar
        left_frame = tk.Frame(main_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill="y", padx=10)

        # Search bar for filtering songs
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill="x", pady=5)

        search_label = tk.Label(search_frame, text="Search Song:")  # Label for the search bar
        search_label.pack(side=tk.LEFT, padx=5)

        # Text entry for user search queries
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        # Button to trigger the search functionality
        search_button = tk.Button(search_frame, text="Search", command=self.search_songs)
        search_button.pack(side=tk.LEFT, padx=5)

        # Label and Listbox to display the folder playlist (available songs)
        folder_playlist_label = tk.Label(left_frame, text="Playlist")
        folder_playlist_label.pack(pady=5)

        self.folder_playlist = tk.Listbox(
            left_frame, bg="black", fg="white", width=50,
            selectbackground="blue", selectforeground="white"
        )
        self.folder_playlist.pack(fill="y", expand=True)

        # Button to add selected songs to the added playlist
        add_button = tk.Button(left_frame, text="Add", command=self.add_to_playlist)
        add_button.pack(pady=5)

        # Right frame: Contains the added playlist and playback controls
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)

        # Label and Listbox to display the added playlist (songs selected for playback)
        added_playlist_label = tk.Label(right_frame, text="Added Playlist")
        added_playlist_label.pack(pady=5)

        self.added_playlist = tk.Listbox(
            right_frame, bg="black", fg="white", width=50, height=15,
            selectbackground="blue", selectforeground="white"
        )
        self.added_playlist.pack(fill="y", expand=True)

        # Button to reset playlist
        reset_playlist_button = tk.Button(right_frame, text="Reset Playlist", command=self.reset_playlist)
        reset_playlist_button.pack(pady=5)

        # Control buttons frame for playback controls
        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(pady=20)

        # Load control button images and resize them for consistency
        back_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(self.PICTURES_FOLDER, "back-button.png")).resize((50, 50)))
        forward_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(self.PICTURES_FOLDER, "next-button.png")).resize((50, 50)))
        play_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(self.PICTURES_FOLDER, "play-button.png")).resize((50, 50)))
        pause_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(self.PICTURES_FOLDER, "pause-button.png")).resize((50, 50)))
        stop_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(self.PICTURES_FOLDER, "stop-button.png")).resize((50, 50)))

        # Create playback control buttons with their respective commands
        back_button = tk.Button(controls_frame, image=back_btn_img, borderwidth=0, command=self.previous_song)
        forward_button = tk.Button(controls_frame, image=forward_btn_img, borderwidth=0, command=self.next_song)
        play_button = tk.Button(controls_frame, image=play_btn_img, borderwidth=0, command=self.play)
        pause_button = tk.Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: self.pause(self.paused))
        stop_button = tk.Button(controls_frame, image=stop_btn_img, borderwidth=0, command=self.stop)

        # Prevent images from being garbage collected by storing references
        back_button.image = back_btn_img
        forward_button.image = forward_btn_img
        play_button.image = play_btn_img
        pause_button.image = pause_btn_img
        stop_button.image = stop_btn_img

        # Arrange the playback buttons in a row
        back_button.grid(row=0, column=0, padx=10)
        forward_button.grid(row=0, column=1, padx=10)
        play_button.grid(row=0, column=2, padx=10)
        pause_button.grid(row=0, column=3, padx=10)
        stop_button.grid(row=0, column=4, padx=10)

        # Slider for controlling the current song position
        self.song_slider = ttk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, value=0, command=self.slide, length=360)
        self.song_slider.pack(pady=10)

        # Volume control slider and label
        volume_frame = tk.Frame(right_frame)
        volume_frame.pack(pady=10)

        # Add the "Volume:" label to the left of the slider
        volume_label = tk.Label(volume_frame, text="Volume:")
        volume_label.pack(side=tk.LEFT, padx=5)  # Place it to the left of the slider with padding

        self.volume_slider = ttk.Scale(
            volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, value=50,
            length=360, command=self.set_volume
        )
        self.volume_slider.pack(side=tk.LEFT)

        self.volume_label = tk.Label(volume_frame, text="50%")  # Shows the current volume percentage
        self.volume_label.pack(side=tk.LEFT, padx=10)


        # Status bar for displaying the current playback time
        self.status_bar = tk.Label(self.window, text='', bd=1, relief=tk.GROOVE, anchor=tk.E)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=5)

    def set_volume(self, x):
        """
        Adjusts the playback volume based on the value of the volume slider.
        Updates the volume label to show the percentage value.
        """
        pygame.mixer.music.set_volume(self.volume_slider.get() / 100)  # Scale volume (0.0 to 1.0)
        self.volume_label.config(text=f"{int(self.volume_slider.get())}%")  # Update label text

    def load_songs(self):
        """
        Loads all MP3 files from the designated music folder into the folder playlist.
        Resets and refreshes the song mapping and playlist display.
        """
        self.folder_playlist.delete(0, tk.END)  # Clear the current playlist display
        self.song_mapping = {}  # Reset the mapping of song display names to file paths

        # Iterate through all files in the music folder
        for index, file in enumerate(os.listdir(self.MUSIC_FOLDER), start=1):
            if file.endswith(".mp3"):  # Only process MP3 files
                track_number = f"Track {index:02d}"  # Assign a track number
                song_title = os.path.splitext(file)[0]  # Extract the song title (without extension)
                display_name = f"{track_number} {song_title}"  # Combine track number and title
                self.folder_playlist.insert(tk.END, display_name)  # Add to the playlist display
                self.song_mapping[display_name] = file  # Map the display name to the actual file

    def search_songs(self):
        """
        Filters the songs in the folder playlist based on the user's search query.
        Displays only matching songs.
        """
        query = self.search_entry.get().lower()  # Get the search query in lowercase
        self.folder_playlist.delete(0, tk.END)  # Clear the playlist display

        # Iterate through all songs and match against the query
        for display_name, file in self.song_mapping.items():
            if query in display_name.lower():  # Case-insensitive match
                self.folder_playlist.insert(tk.END, display_name)  # Display matching songs

    def add_to_playlist(self):
        """
        Adds the currently selected song from the folder playlist to the added playlist.
        Prevents duplicate additions.
        """
        selected_song = self.folder_playlist.get(tk.ACTIVE)  # Get the selected song from the folder playlist
        if selected_song in self.added_playlist.get(0, tk.END):  # Check for duplicates
            messagebox.showwarning("Duplicate Song", f"'{selected_song}' is already in the playlist.")
        else:
            self.added_playlist.insert(tk.END, selected_song)  # Add the song to the added playlist

    def reset_playlist(self):
        """
        Clears the added playlist and resets playback.
        Mimics the behavior of the stop button.
        """
        self.stop()  # Stop playback and reset all playback-related states
        self.added_playlist.delete(0, tk.END)  # Clear the added playlist


    def play(self):
        """
        Plays the currently selected song from the added playlist.
        Initializes and synchronizes the slider and status bar for the song's duration.
        Handles errors if no song is selected or the file is missing.
        """
        # Get the song selected by the user in the "Added Playlist"
        selected_song = self.added_playlist.get(tk.ACTIVE)
        if not selected_song:
            messagebox.showwarning("No Song Selected", "Please select a song to play.")
            return

        # Map the song's display name to its file path
        original_file_name = self.song_mapping.get(selected_song)
        if not original_file_name:
            messagebox.showerror("File Error", "Could not find the original file.")
            return

        # Construct the full path to the song file
        song_path = os.path.join(self.MUSIC_FOLDER, original_file_name)

        # Load the song into the mixer and start playback
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)

        # Retrieve and store the song's total duration in seconds
        self.song_length = MP3(song_path).info.length

        # Record the playback start time
        self.start_time = time.time()

        # Reset the stopped state and enable the slider
        self.stopped = False
        self.song_slider.config(to=self.song_length, value=0, state='normal')

        # Start updating the playback time on the slider and status bar
        self.play_time(song_path)

    def play_time(self, song_path):
        """
        Tracks and updates the current playback time of the song.
        Synchronizes the slider and status bar with the song's current position and duration.
        Stops playback and resets states when the song ends.
            song_path (str): The path of the currently playing song.
        """
        if self.stopped:  # Exit if playback has been stopped
            return

        # Calculate the elapsed time since the song started playing
        current_time = time.time() - self.start_time

        # If the song is paused, skip updates but continue checking periodically
        if self.paused:
            self.status_bar.after(500, lambda: self.play_time(song_path))
            return

        # Update the slider and status bar if the song is still within its duration
        if current_time <= self.song_length:
            self.song_slider.config(value=current_time)  # Update the slider to match current time
            self.status_bar.config(
                text=f"{self.format_time(current_time)} / {self.format_time(self.song_length)}"
            )  # Update the playback time display

            # Schedule the next update in 500 milliseconds
            self.status_bar.after(500, lambda: self.play_time(song_path))
        else:
            # Stop playback when the song finishes
            self.stop()



    def format_time(self, seconds):
        """
        Converts a time value in seconds to a formatted MM:SS string.
        """
        return time.strftime('%M:%S', time.gmtime(seconds))  # Use gmtime to handle time formatting

    def slide(self, x):
        """
        Allows the user to adjust the song's playback position using the slider.
        Seeks to the specified position in the song and resumes playback.
            x (float): The current value of the slider.
        """
        if self.stopped:  # Ignore slider adjustments if playback has been stopped
            return

        # Retrieve the currently selected song in the playlist
        selected_song = self.added_playlist.get(tk.ACTIVE)
        if not selected_song:
            return  # Exit if no song is selected

        # Map the song's display name to its file path
        original_file_name = self.song_mapping.get(selected_song)
        if not original_file_name:
            return  # Exit if the song file is missing

        # Construct the full file path of the song
        song_path = os.path.join(self.MUSIC_FOLDER, original_file_name)

        # Retrieve the new playback position from the slider
        new_position = int(self.song_slider.get())

        # Reload and play the song from the new position
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0, start=new_position)

        # Adjust the start time to account for the new playback position
        self.start_time = time.time() - new_position

    def stop(self):
        """
        Stops the current song playback and resets playback-related states.
        Clears the slider and duration display.
        """
        # Stop the music playback
        pygame.mixer.music.stop()

        # Set the stopped state to True
        self.stopped = True

        # Reset the slider to its initial state and disable it
        self.song_slider.config(value=0, state='disabled')

        # Clear the status bar to remove duration display
        self.status_bar.config(text="")

        # Reset the playback start time to None
        self.start_time = None

    def pause(self, is_paused):
        """
        Pauses or resumes playback based on the current state.
        Toggles the pause state each time it is called.
        """
        if is_paused:
            pygame.mixer.music.unpause()  # Resume playback
            self.paused = False  # Update state
            # Update start_time to account for the paused duration
            self.start_time += time.time() - self.pause_time  
        else:
            pygame.mixer.music.pause()  # Pause playback
            self.paused = True  # Update state
            self.pause_time = time.time()  # Record when the pause happened


    def next_song(self):
        """
        Skips to the next song in the added playlist.
        Loops back to the first song if at the end of the playlist.
        """
        self.song_slider.config(value=0)  # Reset the slider position
        current_index = self.added_playlist.curselection()[0]  # Get the current song index
        next_index = (current_index + 1) % self.added_playlist.size()  # Calculate the next index
        self.added_playlist.selection_clear(0, tk.END)  # Clear the current selection
        self.added_playlist.activate(next_index)  # Highlight the next song
        self.added_playlist.selection_set(next_index)  # Select the next song
        self.play()  # Play the next song

    def previous_song(self):
        """
        Goes back to the previous song in the added playlist.
        Loops to the last song if at the beginning of the playlist.
        """
        self.song_slider.config(value=0)  # Reset the slider position
        current_index = self.added_playlist.curselection()[0]  # Get the current song index
        prev_index = (current_index - 1) % self.added_playlist.size()  # Calculate the previous index
        self.added_playlist.selection_clear(0, tk.END)  # Clear the current selection
        self.added_playlist.activate(prev_index)  # Highlight the previous song
        self.added_playlist.selection_set(prev_index)  # Select the previous song
        self.play()  # Play the previous song


if __name__ == "__main__":
    """
    Entry point for the application.
    Creates the main window and initializes the MusicPlayer class.
    """
    window = tk.Tk()  # Create the main application window
    app = MusicPlayer(window)  # Initialize the MusicPlayer app
    window.mainloop()  # Start the Tkinter event loop
