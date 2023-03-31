from text_processing import (
    remove_encoding_marks,
    remove_extra_text,
    remove_commons,
    remove_punctuation,
    remove_titles,
    remove_character_names,
    initial_text_processing,
)


import pytest
import os

remove_encoding_marks_test_cases = [
    # Check that the function removes empty strings.
    (["", "hi", "", "bye"], ["bye"]),
    # Check that it removes encoding marks.
    (["halloween", "\r\n\r\nfall", "autumn"], ["fall", "autumn"]),
    # Check that an element with encoding marks in the middle is split
    # by that string and added as two separate elements.
    (["find\r\n\r\nreplace", "ctrlh"], ["replace", "ctrlh"]),
    # Check that a list with both encoding marks and empty strings returns
    # a list without these elements.
    (["up", "\r\n\r\nleft", "", "right"], ["left", "right"]),
]

remove_extra_text_test_cases = [
    # Check that it removes starting and ending text, as well as
    # common words.
    (
        ["reach", "for", "the", "stars", "even", "if", "you", "miss"],
        "for",
        "you",
        ["stars"],
    ),
    # Check that it indexes at the first instance of starting string when
    # multiple instances are present.
    (
        [
            "retrospective",
            "renegade",
            "reconfigure",
            "renegade",
            "renew",
            "respawn",
        ],
        "renegade",
        "respawn",
        ["renegade", "reconfigure", "renegade", "renew"],
    ),
    # Check that it successfully removes all common words, even when multiple
    # instances of that word are present.
    (
        [
            "wastrel",
            "the",
            "whimsical",
            "if",
            "the",
            "even",
            "woodwind",
            "wasteland",
        ],
        "wastrel",
        "wasteland",
        ["wastrel", "whimsical", "woodwind"],
    ),
    # Check that it recognizes special characters in start/end words.
    (
        ["alabaster", "mahogany,", "ivory", "seminola"],
        "mahogany,",
        "seminola",
        ["mahogany,", "ivory"],
    ),
]

remove_punctuation_test_cases = [
    # Check that punctuation in the middle of a word doesn't create more
    # than one resulting element.
    (["hasn't", "wasn't", "are"], ["hasnt", "wasnt", "are"]),
    # Check that if there is more than one special special character in an
    # element that both are removed.
    (['"don\'t!"', "no?!"], ["dont", "no"]),
    # Check that punctuation at the end of a word doesn't create more than one
    # resulting element.
    (["me,", "you,", "what?"], ["me", "you", "what"]),
    # Check that all given punctuation marks are removed.
    (["me!", "us?", '"what"', "but,", "alas."], ["me", "us", "what", "but", "alas"]),
]

remove_titles_test_cases = [
    # Check that list of mixed titles and not titles doesn't has titles removed.
    (["lord", "seven", "lady", "nine", "ma'am"], ["seven", "nine"]),
    # Check that a list of non-titles remains unchanged.
    (["twelve", "nine", "one"], ["twelve", "nine", "one"]),
    # Check that list of all titles returns an empty list.
    (["lord", "lady", "mr", "mrs"], []),
]

remove_character_names_test_cases = [
    # Check that an empty tuple of character names leaves the list unchanged.
    (["susan", "mark", "tom"], (), ["susan", "mark", "tom"]),
    # Check that a list with no character names remains unchanged.
    (
        ["biking", "hiking", "snowboarding"],
        ("mark", "susan"),
        ["biking", "hiking", "snowboarding"],
    ),
]


@pytest.mark.parametrize("input_list, output_list", remove_encoding_marks_test_cases)
def test_remove_encoding_marks(input_list, output_list):
    assert remove_encoding_marks(input_list) == output_list


@pytest.mark.parametrize("input, start, end, output", remove_extra_text_test_cases)
def test_remove_extra_test(input, start, end, output):
    assert remove_extra_text(input, start, end) == output


@pytest.mark.parametrize("input, output", remove_punctuation_test_cases)
def test_remove_punctuation(input, output):
    assert remove_punctuation(input) == output


@pytest.mark.parametrize("input, output", remove_titles_test_cases)
def test_remove_titles(input, output):
    assert remove_titles(input) == output


@pytest.mark.parametrize("input, characters, output", remove_character_names_test_cases)
def test_remove_character_names(input, characters, output):
    assert remove_character_names(input, characters) == output
