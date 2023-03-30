"""
A file to store plotting functions
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils import get_alliteration_by_phoneme

"""
Plot bar graph for all books.
"""


def plot_freq_bar(
    most_freq,
    title="Most Popular Words Across All Books",
    ylabel="Number of Occurences Across Texts",
    xlabel="Most Popular Words Across Texts",
):
    fig, ax = plt.subplots()
    words = list(most_freq.keys())
    frequencies = list(most_freq.values())
    plt.bar(range(len(most_freq)), frequencies, tick_label=words)
    fig.set_figheight(7)
    fig.set_figwidth(20)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(fontsize=10)


"""
Plot bar graph for all books.
"""


def plot_freq_bar_one_book(
    most_freq,
    title,
    ylabel="Number of Occurences Across Texts",
    xlabel="Most Popular Words Across Texts",
):
    fig, ax = plt.subplots()
    words = list(most_freq.keys())
    frequencies = list(most_freq.values())
    plt.bar(range(len(most_freq)), frequencies, tick_label=words)
    fig.set_figheight(7)
    fig.set_figwidth(20)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(fontsize=10)


"""
Plot the average sentence length graph

Args:
    list_of_urls: A list of tuples with indices
    that represent the url (str) and title (str)
    of each text.
"""


def plot_avg_sentence_lengths_all_books(sentence_lengths):
    fig, ax = plt.subplots()
    books = list(sentence_lengths.keys())
    avg_sentence_lengths = list(sentence_lengths.values())
    fig.set_figheight(10)
    fig.set_figwidth(10)
    ax.set_title("Average Sentence Length of Work Over Time")
    ax.set_xlabel("Book Title")
    ax.set_ylabel("Average Sentence Length")
    # spacing = 0.6
    plt.xticks(fontsize=10, rotation=90)
    ax.bar(
        range(len(sentence_lengths)),
        avg_sentence_lengths,
        tick_label=books,
        color="orange",
    )


"""
For each book in the list of urls, call
the function that plots the number of times a
particular phoneme is used in an alliterative sequence.

Args: 
    list_of_urls: A list of tuples where the first parameter
    is a string representing the txt file url and the second
    is the name (str) of the local text file on the machine.
"""


def get_all_alliteration_by_phoneme(list_of_urls):
    for book in list_of_urls:
        phonemes, words, pairs = get_alliteration_by_phoneme(book[1])
        plot_alliteration(phonemes, words, pairs, book[1])


"""
Plot the alliteration plots
"""


def plot_alliteration(phoneme_dict, word_dict, pairs, book_title):
    phonemes = list(phoneme_dict.keys())
    num_occurences = list(phoneme_dict.values())
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax1.title.set_text(f"Phoneme Usage in {book_title}")
    ax2.title.set_text("Most Frequently Alliterated words")
    ax3.title.set_text("Sample Alliterative Pairings")

    fig.set_figheight(15)
    fig.set_figwidth(20)
    ax1.set_xlabel("Phoneme")
    ax1.set_ylabel(
        "Number of Occurences of Alliteration by Phoneme in All Sentences"
    )
    # spacing = 0.6
    plt.xticks(fontsize=10)
    # fig.subplots_adjust(top=spacing + 0.1)
    # fig.subplots_adjust(bottom=spacing)
    ax1.bar(
        range(len(phoneme_dict)),
        num_occurences,
        tick_label=phonemes,
        color="orange",
    )

    wc = WordCloud(
        background_color="black",
        width=1000,
        height=1000,
        max_words=10,
        relative_scaling=0.5,
        normalize_plurals=True,
    ).generate_from_frequencies(word_dict)
    ax2.imshow(wc)

    wc = WordCloud(
        background_color="black",
        width=1000,
        height=1000,
        max_words=10,
        relative_scaling=0.5,
        normalize_plurals=True,
    ).generate(str(pairs))
    ax3.imshow(wc)


def plot_tf_idf(tf_list, tfidf_cuttoff):
    """Creates a scatter plot of TFIDF scores of different words mapped to their frequency.

    Args:
        tf_list (list): list of dictionaries containing words mapped to TFIDF scores.
        tfidf_cuttoff (float): for
    """
