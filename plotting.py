"""
A file to store plotting functions
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils import get_sentences_from_txt


def plot_freq_bar(most_freq):
    fig, ax = plt.subplots()
    words = list(most_freq.keys())
    frequencies = list(most_freq.values())
    plt.bar(range(len(most_freq)), frequencies, tick_label=words)
    fig.set_figheight(7)
    fig.set_figwidth(20)
    ax.set_title("Most Popular Words Across All Books")
    ax.set_ylabel("Number of Occurences Across Texts")
    ax.set_xlabel("Most Popular Words Across Texts")
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
    plt.xticks(fontsize=10)
    ax.bar(
        range(len(sentence_lengths)),
        avg_sentence_lengths,
        tick_label=books,
        color="orange",
    )
