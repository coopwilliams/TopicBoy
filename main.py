from finder import *
from reader import *

if __name__ == "__main__":
    try:
        unpack_roam(ROAM_DIR_PATH)
        roam = read_roam(ROAM_DIR_PATH)
        poly = one_note_by_title(roam, "polycentrix law", fuzzy=True)
        books = one_note_by_title(roam, "my favorite books")
        containing = contains_string(books, "Top")
        happy = notes_by_string(roam, "happy")
        happy_text = text_by_string(roam, "happy", True, True)
        bau = text_by_string(roam, "Baudrillard", True, True)
    except Exception as e:
        print("couldn't read the test files.")
        raise(e)