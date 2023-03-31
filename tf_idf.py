"""
Computes TF_IDF of text compared to a corpus.
"""
import itertools
import math
import text_processing


def calc_word_freq(text_list, num_data_pts):
    word_dict = {}
    for word in text_list:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1
    sorted_keys = sorted(word_dict, key=word_dict.get, reverse=True)
    values = []
    for key in sorted_keys:
        values.append(word_dict[key])
    most_freq = {}
    most_freq = dict(zip(sorted_keys, values))
    most_freq = dict(itertools.islice(most_freq.items(), num_data_pts))

    return most_freq


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
    for term, frequency in tf_dict.items():
        novel_occurences = 0
        for novel in corpus:
            if term in novel:
                novel_occurences += 1
        tf_idf_dict[term] = frequency * math.log10(len(corpus) / novel_occurences)
    return tf_idf_dict
