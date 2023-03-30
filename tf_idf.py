"""
Computes TF_IDF of text compared to a corpus.
"""

import math
import text_processing

lord_arthur_saviles_crimes = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/773/773-0.txt",
    "Lord Arthur Savile's Crime And Other Short Stories",
)
the_happy_prince = text_processing.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/902/pg902.txt",
    "The Happy Prince and Other Short Stories",
)
the_picture_of_dorian_grey = text_processing.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/174/pg174.txt",
    "The Picture of Dorian Grey",
)
salome = text_processing.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/42704/pg42704.txt", "Salome"
)
a_house_of_pomegranates = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/873/873-0.txt", "A House of Pomegranates"
)
the_ducchess_of_padua = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/875/875-0.txt", "The Ducchess of Padua"
)
the_soul_of_man_under_socialism = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/1017/1017-0.txt",
    "The Soul of Man Under Socialism",
)
lady_windermeres_fan = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/790/790-0.txt", "Lady Windermeres Fan"
)
a_woman_of_no_importance = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/854/854-0.txt", "A Woman of No Importance"
)
the_importance_of_being_earnest = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/844/844-0.txt",
    "The Importance of Being Earnest",
)
the_ballad_of_reading_gaol = text_processing.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/301/pg301.txt",
    "The Ballad of Reading Gaol",
)
an_ideal_husband = text_processing.get_data_from_book(
    "https://www.gutenberg.org/files/885/885-0.txt", "An Ideal Husband"
)

oscar_wilde_corpus = [
    lord_arthur_saviles_crimes,
    the_happy_prince,
    the_picture_of_dorian_grey,
    salome,
    a_house_of_pomegranates,
    the_ducchess_of_padua,
    the_soul_of_man_under_socialism,
    lady_windermeres_fan,
    a_woman_of_no_importance,
    the_importance_of_being_earnest,
    the_ballad_of_reading_gaol,
    an_ideal_husband,
]


def compute_tf(novel):
    """Computes term frequency of all terms in a text.

    Args:
        novel (list): A list of words in the novel, each as a string.

    Returns:
        tf_dict (dictionary): A dictionary where keys are all words appearing
        in the novel and values are number of occurences in novel.
    """
    tf_dict = {}
    num_words = 0
    for word in novel:
        if word in tf_dict:
            tf_dict[word] += 1
        else:
            tf_dict[word] = 1
            num_words += 1
    for term, occurences in tf_dict.items():
        tf_dict[term] = occurences / num_words
    return tf_dict


def compute_tf_idf(tf_dict, corpus):
    """Computes TF-IDF of terms in one text compared to all texts
    in a corpus.

    Args:
        tf_dict (dictionary): a dictionary of words mapping
        corpus (list): a list of lists of words in different texts to
        calculate inverse document frequency from

    Returns:
        tf_idf_dict: a dictionary of words appearing a text mapped to their
        tf-idf value
    """
    tf_idf_dict = {}
    for term, frequency in tf_dict:
        novel_occurences = 0
        for novel in corpus:
            if term in novel:
                novel_occurences += 1
        tf_idf_dict[term] = frequency * math.log10(
            len(corpus) / novel_occurences
        )
    return tf_idf_dict
