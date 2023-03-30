"""
Test the plotting functions in utils.py
"""

import unittest
from utils import plot_most_freq_words_texts
import pytest


list_of_urls = [("fake_url", "test_txt1")]
get_complement_cases = [
    # Check that the complement of A is T.
    ((("fake_url", "test_txt1"), 2), {"have": 9, "not": 1}),
]


@pytest.mark.parametrize("input_tuple,output_dict", get_complement_cases)
def test_plot_most_freq_words_texts(input_tuple, output_dict):
    """
    Test that each nucleotide is mapped to its correct complement.

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
    assert plot_most_freq_words_texts(input_tuple[0], input_tuple[1]) == output_dict

