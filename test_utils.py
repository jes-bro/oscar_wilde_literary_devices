"""
Test the text analysis functions in utils.py
"""

from utils import (
    plot_most_freq_words_texts,
    split_into_lowered_sentences,
    get_alliteration_by_phoneme,
    get_avg_sentence_length,
    split_sentences_into_lists_of_words,
    get_phonemes,
    get_sentences_from_txt,
)
import pytest
import os

list_of_urls = [("fake_url", "test_txt1")]
plot_most_freq_words_texts_cases = [
    # Check that function correctly counts 2 most frequent words
    # in a text file with one sentence and 2 words
    # where the highest frequency word is consecutive
    (([("fake_url", "test_txt1")], 2), {"have": 9, "not": 1}),
    # Check that the 2 highest frequency words are counted
    # correctly despite extraneous punctuation
    # tests against periods, exclamation points and
    # question marks
    (([("fake_url", "test_txt2")], 2), {"hello": 6, "side": 5},),
    # check to make sure that mixed capitalization does not
    # affect the count of the 2 highest frequency words
    # and counts the words correctly even though they are not
    # consecutive
    (
        ([("fake_url", "test_txt3")], 5),
        {"hello": 3, "from": 3, "the": 3, "other": 3, "side": 3},
    ),
    # Check that it correctly counts top 3 most frequent words
    (([("fake_url", "test_txt4")], 3), {"from": 5, "hello": 4, "side": 4},),
    # Check that it accounts for apostrophes
    (([("fake_url", "test_txt5")], 3), {"from": 5, "hello": 4, "side": 4},),
    # Check that it works across multiple texts
    (
        ([("fake_url", "test_txt6"), ("fake_url", "test_txt7")], 2),
        {"one": 2, "two": 2},
    ),
]

split_into_lowered_sentences_cases = [
    # Simple case with three normal sentences and a number.
    # This case checks if the function can handle normal sentences
    # with spaces and return a list of sentences in lowercase
    (
        "Hello World. This is a test sentence. Do not panic. 1234.",
        ["hello world.", "this is a test sentence.", "do not panic.", "1234."],
    ),
    # Check to see if it works with exclamation marks
    (
        "Hello World! This is a test sentence. Do not panic! 1234.",
        ["hello world!", "this is a test sentence.", "do not panic!", "1234."],
    ),
    # Check if it works on one sentence
    ("Hello World!", ["hello world!"]),
    # Check if it works with question marks
    (
        "Hello World? This is a test sentence. Do not panic! 1234.",
        ["hello world?", "this is a test sentence.", "do not panic!", "1234."],
    ),
    # Check that it works with urls
    (
        "Visit our website at www.example.com.",
        ["visit our website at www.example.com."],
    ),
    # Check that it works with Dr.
    (
        "Visit our website Dr. www.example.com.",
        ["visit our website dr. www.example.com."],
    ),
    # Check that it works with Mrs.
    (
        "Visit our website Mrs. www.example.com.",
        ["visit our website mrs. www.example.com."],
    ),
    # Check that it works with Mr.
    (
        "Visit our website Mr. www.example.com.",
        ["visit our website mr. www.example.com."],
    ),
    # Check that it works with commas
    (
        "Visit our website Mr, www.example.com.",
        ["visit our website mr, www.example.com."],
    ),
    # Check that it works with Mrs. two sentences
    (
        "Hello World? This is a test Mrs. sentence. Do not panic! 1234.",
        [
            "hello world?",
            "this is a test mrs. sentence.",
            "do not panic!",
            "1234.",
        ],
    ),
]

get_avg_sentence_length_cases = [
    # See if it accurately counts the average sentence
    # length of two text files, each containing one
    # sentence of length 3
    (
        [("fake_url", "test_txt8"), ("fake_url", "test_txt9")],
        {"test_txt8": 3, "test_txt9": 3},
    ),
    # Test with a single URL
    ([("fake_url", "test_txt1")], {"test_txt1": 10},),
    # Test with multiple URLs of different lengths, with
    # one file having a non-integer average
    (
        [("fake_url", "test_txt1"), ("fake_url", "test_txt2"),],
        {"test_txt1": 10, "test_txt2": 3},
    ),
    # Test with empty input
    ([], {}),
]

split_sentences_into_lists_of_words_cases = [
    # Test with empty input
    ([], []),
    # Test with a single sentence
    (
        ["This is a sample sentence."],
        [["This", "is", "a", "sample", "sentence."]],
    ),
    # Test with multiple sentences
    (
        ["This is a sample sentence.", "This is another sample sentence."],
        [
            ["This", "is", "a", "sample", "sentence."],
            ["This", "is", "another", "sample", "sentence."],
        ],
    ),
    # Test with sentence containing no space
    (["Thisisasamplesentence."], [["Thisisasamplesentence."]]),
    # Test with the presence of a question mark
    (["Thisisasamplesentence?"], [["Thisisasamplesentence?"]]),
    # Test an upper case letter in the middle of the sentence
    (
        ["This is a Sample sentence.", "This is another Sample sentence."],
        [
            ["This", "is", "a", "Sample", "sentence."],
            ["This", "is", "another", "Sample", "sentence."],
        ],
    ),
    # Test with Mrs. and multiple sentences
    (
        ["This is a Mrs. sentence.", "This is another Sample sentence."],
        [
            ["This", "is", "a", "Mrs.", "sentence."],
            ["This", "is", "another", "Sample", "sentence."],
        ],
    ),
    # Test with Mr. and multiple sentences
    (
        ["This is a Mr. sentence.", "This is another Sample sentence."],
        [
            ["This", "is", "a", "Mr.", "sentence."],
            ["This", "is", "another", "Sample", "sentence."],
        ],
    ),
    # Test with Rev. and multiple sentences
    (
        ["This is a Rev. sentence.", "This is another Sample sentence."],
        [
            ["This", "is", "a", "Rev.", "sentence."],
            ["This", "is", "another", "Sample", "sentence."],
        ],
    ),
    # Test with no punctuation in last sentence
    (
        [
            "This is a Rev. sentence.",
            "This is another Sample sentence.",
            "fragment",
        ],
        [
            ["This", "is", "a", "Rev.", "sentence."],
            ["This", "is", "another", "Sample", "sentence."],
            ["fragment"],
        ],
    ),
]

get_phonemes_cases = [
    # Test with a valid word
    ("hello", ["HH", "AH0", "L", "OW1"]),
    # Test with a word not in the phoneme dictionary
    ("non-existent-word", ["NONE"]),
    # Test with an empty input
    ("", ["NONE"]),
    # Test with a number
    ("1234", ["NONE"]),
    # Test with a th word
    ("though", ["DH", "OW1"]),
    # Test with the
    ("the", ["DH", "AH0"]),
    # Test that it does not work with capital letters
    ("The", ["NONE"]),
]

get_sentences_from_txt_cases = [
    # Test single sentence
    # and test that capitalization is lowered
    ("test_txt1", ["have have have have have have have have have not."]),
    # Test multiple sentences
    # and test that capitalization is lowered
    (
        "test_txt2",
        [
            "hello hello hello?",
            "hello from the other side.",
            "hello from!",
            "the other side.",
            "hello from the other side.",
            "side side.",
        ],
    ),
]


@pytest.mark.parametrize("input_str,output_list", get_phonemes_cases)
def test_get_phonemes(input_str, output_list):
    """
    Retrieve the phonemes associated with a
    given word.

    Look up and return the first phoneme associated
    with the given word to

    Args:
        word: A string representing a word in a text.

    Returns:
        A list of a string representing the phonemes
        associated with the word.
    """

    assert get_phonemes(input_str) == output_list


@pytest.mark.parametrize(
    "input_tuple,output_dict", plot_most_freq_words_texts_cases
)
def test_plot_most_freq_words_texts(input_tuple, output_dict):
    """
    Test that the function returns the correct dictionary for each text file.

    Given a tuple representing url and book title, and an int representing
    the number of frequent words to keep track of, return a dictionary
    mapping the most frequently occuring words in all texts to the number
    of times they occur. The length of the dictionary should be the length
    of num_data_pts

    Args:
        list_of_urls: A list of tuples representing urls (str) and
        book titles (str)
        num_data_pts: an int representing the number of highest frequency
        words to plot.
    """

    assert (
        plot_most_freq_words_texts(input_tuple[0], input_tuple[1])
        == output_dict
    )


@pytest.mark.parametrize(
    "input_str,output_list", split_into_lowered_sentences_cases
)
def test_split_into_lowered_sentences(input_str, output_list):
    """
    Split a string of text into a list of sentences,
    accounting for special cases where periods
    occur that do not mean that a sentence is ending.

    Args:
        text: A string representing text read from
        a text file.

    Returns:
        sentences: A list of strings representing each
        sentence in the given text.
    """

    assert split_into_lowered_sentences(input_str) == output_list


@pytest.mark.parametrize(
    "input_tuple,output_dict", get_avg_sentence_length_cases
)
def test_get_avg_sentence_length(input_tuple, output_dict):
    """
    Given a list of texts, create a bar graph
    representing the average sentence length
    for each text.

    Returns:
        sentence_lengths: A dictionary mapping
        texts (string) to their average sentence
        length (int).
    """
    assert get_avg_sentence_length(input_tuple) == output_dict


"""
Split a list of strings representing sentences
into lists of lists of strings, where the
elements at each index in the inner lists are
words and the list containing the words is a
sentence

Args:
    sentences: A list of strings representing
    the sentences in a given text.

Returns:
    sentences: A list of lists of strings
    representing lists of the words in every
    sentence.
"""


@pytest.mark.parametrize(
    "input_list,output_list", split_sentences_into_lists_of_words_cases
)
def test_get_avg_sentence_length(input_list, output_list):
    """
    Given a list of texts, create a bar graph
    representing the average sentence length
    for each text.

    Returns:
        sentence_lengths: A dictionary mapping
        texts (string) to their average sentence
        length (int).
    """
    assert split_sentences_into_lists_of_words(input_list) == output_list


@pytest.fixture(scope="module")
def test_files_dir():
    return os.path.join(os.path.dirname(__file__), "test_files")


@pytest.mark.parametrize(
    "filename, expected_phoneme_dict, expected_word_dict, expected_pairs",
    [
        # Test that no sequential alliterative sequences get picked up
        # when there aren't any present
        ("example_book_1", {}, {}, [],),
        # Test that peter piper picked a peck of pickled onions returns what we expect
        (
            "example_book_2",
            {"P": 2},
            {"peter": 1, "piper": 1},
            ["(peter_piper)"],
        ),
    ],
)
def test_get_alliteration_by_phoneme(
    test_files_dir,
    filename,
    expected_phoneme_dict,
    expected_word_dict,
    expected_pairs,
):
    filepath = os.path.join(test_files_dir, filename)
    phoneme_dict, word_dict, pairs = get_alliteration_by_phoneme(filepath)
    assert phoneme_dict == expected_phoneme_dict
    assert word_dict == expected_word_dict
    assert pairs == expected_pairs


@pytest.mark.parametrize("input_str,output_list", get_sentences_from_txt_cases)
def test_sentences_from_txt(input_str, output_list):
    """
    Create sentences by reading a text file.

    Split the text from a single text in
    the corpus into a list of strings of
    sentences.

    Args:
        book_title: A string representing
        the title of the book.

    Returns:
        sentences: A list of strings representing each
        sentence in the given text.
    """
    assert get_sentences_from_txt(input_str) == output_list
