from finder import *
from preprocessing import *
from reader import *
from vectors import *

### Outlining the core functionality
# This tool might get a GUI or it might just be a CLI.
# So how do I write an API that works for either frontend?

# the API needs to return:
    # - related documents
    #     - title
    #     - filepath
    #     - page number
    #     - text 
    #     + Perhaps I should just store the filepath and page, then call
    #         + up the doc on demand.


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
        vec = vectorize_note(books)

    except Exception as e:
        print("couldn't read the test files.")
        raise(e)