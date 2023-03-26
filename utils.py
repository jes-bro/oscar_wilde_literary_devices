import requests
import re
import matplotlib.pyplot as plt
import nltk


def get_data_from_book(url, book_title):
    response = requests.get(url)
    response.encoding = "UTF-8"
    response_text = response.text
    response_words = response_text.replace("\ufeff", "")
    words = response_words.split()

    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.txt", "w") as f:
        for i in lowered:
            f.write(f"{i} ")
    return lowered


def plot_most_freq_words(lowered, num_data_pts):
    f_dist = nltk.FreqDist(lowered)
    f_dist.plot(num_data_pts)
