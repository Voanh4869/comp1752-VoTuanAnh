import pytest
import os
import Track_library1 as lib


def setup_module(module):
    """
    Setup function to load the library from a JSON file.
    It will use the default or fallback path if no specific path is provided.
    """
    # Default relative path
    default_file_path = os.path.join(os.path.dirname(__file__), "library.json")
    # Fallback to the known absolute path
   
    # Determine the file to load
    if os.path.exists(default_file_path):
        file_path = default_file_path
    else:
        raise FileNotFoundError("JSON file not found in either the default or fallback locations. "
                                "Please ensure the JSON file is available.")

    # Load the library
    lib.load_library_from_json(file_path)


def test_list_all():
    """Test listing all items in the library."""
    result = lib.list_all()
    assert "01 Another Brick in the Wall - Pink Floyd ****" in result
    assert "02 Stayin' Alive - Bee Gees *****" in result
    assert "05 Someone Like You - Adele ***" in result


def test_get_name():
    """Test retrieving the name of a track by key."""
    assert lib.get_name("01") == "Another Brick in the Wall"
    assert lib.get_name("05") == "Someone Like You"
    assert lib.get_name("10") is None  # Non-existent key


def test_get_artist():
    """Test retrieving the artist of a track by key."""
    assert lib.get_artist("02") == "Bee Gees"
    assert lib.get_artist("03") == "AC/DC"
    assert lib.get_artist("10") is None  # Non-existent key


def test_get_rating():
    """Test retrieving the rating of a track by key."""
    assert lib.get_rating("01") == 4
    assert lib.get_rating("04") == 1
    assert lib.get_rating("10") == -1  # Non-existent key


def test_set_rating():
    """Test setting a new rating for a track."""
    lib.set_rating("01", 5)
    assert lib.get_rating("01") == 5
    lib.set_rating("10", 3)  # Non-existent key; should not change anything
    assert lib.get_rating("10") == -1  # Verify it remains non-existent


def test_get_play_count():
    """Test retrieving the play count of a track."""
    assert lib.get_play_count("02") == 0
    assert lib.get_play_count("05") == 0
    assert lib.get_play_count("10") == -1  # Non-existent key


def test_increment_play_count():
    """Test incrementing the play count of a track."""
    initial_count = lib.get_play_count("03")
    lib.increment_play_count("03")
    assert lib.get_play_count("03") == initial_count + 1
    # Try incrementing for a non-existent key; nothing should change
    lib.increment_play_count("10")
    assert lib.get_play_count("10") == -1  # Still non-existent


if __name__ == "__main__":
    pytest.main()
