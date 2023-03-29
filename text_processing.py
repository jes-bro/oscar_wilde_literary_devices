"""
Retrieves data from a .txt file and removes extraneous text.
"""
import requests


def get_data_from_book(url, book_title):
    """
    Retrieve the text of a Project Gutenberg txt file.
    Create a list of words and stores data in a txt file.

    Args:
        url (string): The url of a Project Gutenburg txt file.
        book_title (string): Title of the book being retrieved.

    Returns:
        lowered: A list of words in book, written as strings in lowercase
    """
    response = requests.get(url, timeout=30)
    response.encoding = "UTF-8"
    response_text = response.text
    response_words = response_text.replace("\ufeff", "")
    words = response_words.split(" ")

    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.txt", "w") as file:
        for i in lowered:
            file.write(f"{i} ")
    return lowered


def remove_extra_text(lowered, start_word):
    """
    Remove extra words from a list of words, including project gutenberg
    starting and endings, and common words.

    Args:
        lowered (list): A list of words appearing in a text.
        start_word (string): Word denoting the last word of text to be
        removed from beginning of list.

    Returns:
        new_lowered: A list of words with common words and start/end
        text removed.
    """
    new_lowered = lowered[lowered.index(start_word) : lowered.index("***end")]
    commons = []
    with open("commons.csv", "r") as file:
        for line in file:
            commons.append(line.strip("\n"))
    for words in enumerate(commons):
        for _ in range(new_lowered.count(words)):
            new_lowered.remove(words)
    return new_lowered


def remove_punctuation(new_lowered):
    """
    Remove punctuation marks from a list of words.

    Args:
        new_lowered: A list of words from a given text.

    Returns:
        new_lowered: the input argument with punctuation
        marks removed.
    """
    for word in new_lowered:
        if "." in word:
            word.replace(".", "")
        if "," in word:
            word.replace(",", "")
        if '"' in word:
            word.replace('"', "")
        if "!" in word:
            word.replace("!", "")
        if "?" in word:
            word.replace("?", "")
    return new_lowered


def remove_titles(new_lowered):
    """
    Remove titles from list of words.

    Args:
        new_lowered (list): A list of lowercase words with no punctuation marks.

    Returns:
        new_lowered : A list of words with no titles.
    """
    for _ in range(new_lowered.count("lord")):
        new_lowered.remove("lord")
    for _ in range(new_lowered.count("lady")):
        new_lowered.remove("lady")
    for _ in range(new_lowered.count("mr")):
        new_lowered.remove("mr")
    for _ in range(new_lowered.count("mrs")):
        new_lowered.remove("mrs")
    for _ in range(new_lowered.count("miss")):
        new_lowered.remove("miss")
    return new_lowered


def remove_character_names(new_lowered, characters_in_novel):
    """
    Remove character names from a list of words.

    Args:
        new_lowered (list): A list of lowercase words.
        characters_in_novel (list): A list of characters in a given novel.

    Returns:
        new_lowered: A list of words with given character names removed.
    """
    for character in characters_in_novel:
        for _ in range(new_lowered.count(character)):
            new_lowered.remove(character)
    return new_lowered
