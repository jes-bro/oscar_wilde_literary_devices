"""
A file to store plotting functions
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def plot_freq_bar(most_freq):
    fig, ax = plt.subplots()
    words = list(most_freq.keys())
    frequencies = list(most_freq.values())
    plt.bar(range(len(most_freq)), frequencies, tick_label=words)
    fig.set_figheight(7)
    fig.set_figwidth(20)
    ax.set_title("Most Popular Words Across All Books")
    plt.xticks(fontsize=10)
