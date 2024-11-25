from library_item import LibraryItem
import json
import os

class LibraryItem:
    def __init__(self, name, artist, rating):
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = 0  # Default play count is 0

    def info(self):
        stars = "*" * self.rating
        return f"{self.name} - {self.artist} {stars}"


# Initialize an empty library
library = {}


def load_library_from_json(file_path=None):
    """
    Load the library data from a JSON file.
    :param file_path: Optional file path for the library JSON file. If not provided, uses default paths.
    """
    global library
    # Default relative path
    default_file_path = os.path.join(os.path.dirname(__file__), "library.json")
    # Fallback to the absolute path
   
    
    # Determine the file to load
    if file_path:
        chosen_path = file_path
    elif os.path.exists(default_file_path):
        chosen_path = default_file_path
    else:
        raise FileNotFoundError("JSON file not found in the provided, default, or fallback locations.")

    # Load data from the chosen file
    with open(chosen_path, 'r') as file:
        data = json.load(file)
    
    # Populate the library dictionary
    library.clear()
    for key, value in data.items():
        library[key] = LibraryItem(value["title"], value["artist"], value["rating"])

def list_all():
    """List all items in the library."""
    output = ""
    for key, item in library.items():
        output += f"{key} {item.info()}\n"
    return output.strip()


def get_name(key):
    """Retrieve the name of a track by its key."""
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None


def get_artist(key):
    """Retrieve the artist of a track by its key."""
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None


def get_rating(key):
    """Retrieve the rating of a track by its key."""
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1


def set_rating(key, rating):
    """Set a new rating for a track."""
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        pass


def get_play_count(key):
    """Retrieve the play count of a track."""
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1


def increment_play_count(key):
    """Increment the play count of a track."""
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        pass