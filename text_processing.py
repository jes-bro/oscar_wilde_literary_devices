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
    response_text = response.text
    response.encoding = "UTF-8"
    words = response_text.split(" ")

    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.txt", "w") as file:
        for i in lowered:
            file.write(f"{i} ")
    return lowered


def remove_encoding_marks(lowered):
    """Removes encoding marks containing \r\n from a list of strings."

    Args:
        lowered (list): list of words from a given text

    Returns:
        lowered: give list of words with encoding marks removed.
    """
    new_lowered = []
    for word in lowered:
        if word == "":
            continue
        elif "\r\n\r\n\r\n" in word:
            two_words = word.split("\r\n\r\n\r\n")
            new_lowered.append(two_words[0])
            new_lowered.append(two_words[1])
        elif "\r\n\r\n" in word:
            two_words = word.split("\r\n\r\n")
            new_lowered.append(two_words[0])
            new_lowered.append(two_words[1])
        elif "\r\n" in word:
            two_words = word.split("\r\n")
            new_lowered.append(two_words[0])
            new_lowered.append(two_words[1])
        else:
            new_lowered.append(word)
    return new_lowered[1:]


def remove_extra_text(lowered, start_word, end_word):
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
    new_lowered = lowered[lowered.index(start_word) : lowered.index(end_word)]
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
    for _ in range(new_lowered.count("earl")):
        new_lowered.remove("earl")
    for _ in range(new_lowered.count("sir")):
        new_lowered.remove("sir")
    for _ in range(new_lowered.count("ma'am")):
        new_lowered.remove("ma'am")
    return new_lowered


def remove_character_names(new_lowered, character_tuple):
    """
    Remove character names from a list of words.

    Args:
        new_lowered (list): A list of lowercase words.
        character_tuples (tuple)): A list of characters in a given novel.

    Returns:
        new_lowered: A list of words with given character names removed.
    """
    for character in character_tuple:
        for _ in range(new_lowered.count(character)):
            new_lowered.remove(character)
    return new_lowered


def initial_text_processing(num, corpus, start_end_dict, character_dict):
    """Performs all data processing in this file.

    Args:
        num (integer): An integer representing the index in the corpus of the
        book you are doing the data processing on.
        corpus (list): A list of tuples containing the urls and titles
        of a corpus to import and process
        start_end_dict (dictionary): A dictionary mapping titles to tuples
        of start and end words.
        character_dict (dictionary): A dictionary mapping titles to tuples
        containing a list of main characters.

    Returns:
        processed_words (list): a list of words that appear in the given novel,
        in lowercase, without starting words, ending words, common words,
        punctuation, titles, and main characters.
    """
    title = corpus[num][1]
    url = corpus[num][0]
    start_word = start_end_dict[title][0]
    end_word = start_end_dict[title][1]
    characters = character_dict[title]

    return remove_character_names(
        remove_titles(
            remove_punctuation(
                remove_extra_text(
                    remove_encoding_marks(get_data_from_book(url, title)),
                    start_word,
                    end_word,
                )
            )
        ),
        characters,
    )
