"""
Test the text analysis functions in utils.py
"""

from utils import plot_most_freq_words_texts
import pytest


list_of_urls = [("fake_url", "test_txt1")]
plot_most_freq_words_texts_cases = [
    # Check that function correctly counts words
    # in a text file with one sentence and 2 words
    # repeated word is consecutive
    (([("fake_url", "test_txt1")], 2), {"have": 9, "not": 1}),
    # check if repeated word is not consecutive
    # for multiple repeated words
    (
        ([("fake_url", "test_txt2")], 2),
        {"hello": 9, "from": 1, "the": 1, "other": 1, "side": 1},
    ),
]


@pytest.mark.parametrize("input_tuple,output_dict", plot_most_freq_words_texts_cases)
def test_plot_most_freq_words_texts(input_tuple, output_dict):
    """
    Test that each .

    Given a single-character string representing a nucleotide that is "A", "T",
    "G", or "C", check that the get_complement function correctly maps the
    string to a single-character string representing the nucleotide's complement
    (also "A", "T", "G", or "C").

    Args:
        nucleotide: A single-character string equal to "A", "C", "T", or "G"
            representing a nucleotide.t
        complement: A single-character string equal to "A", "C", "T", or "G"
            representing the expected complement of nucleotide.
    """
    print(input_tuple)
    print(output_dict)
    assert plot_most_freq_words_texts(input_tuple[0], input_tuple[1]) == output_dict

