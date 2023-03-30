"""
Test the text analysis functions in utils.py
"""

from utils import (
    plot_most_freq_words_texts,
    split_into_lowered_sentences,
    get_alliteration_by_phoneme,
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
]


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
