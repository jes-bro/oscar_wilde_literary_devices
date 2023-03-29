import requests


def get_data_from_book(url, book_title):
    """Retrieves text of a Project Gutenberg txt file. Creates list of words
    and stores data in a .txt file.

    Args:
        url (string): url of a Project Gutenburg txt file.
        book_title (string): Title of the book being retrieved.

    Returns:
        lowered: a list of words in book, written as strings in lowercase
    """
    response = requests.get(url, timeout=30)
    response.encoding = "UTF-8"
    response_text = response.text
    response_words = response_text.replace("\ufeff", "")
    words = response_words.split(" ")

    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.txt", "w") as f:
        for i in lowered:
            f.write(f"{i} ")
    return lowered


def remove_extra_text(lowered, start_word):
    new_lowered = lowered[lowered.index(start_word) : lowered.index("***end")]
    commons = []
    with open("commons.csv", "r") as f:
        for line in f:
            commons.append(line.strip("\n"))
    for words in enumerate(commons):
        for _ in range(new_lowered.count(words)):
            new_lowered.remove(words)
    return new_lowered
