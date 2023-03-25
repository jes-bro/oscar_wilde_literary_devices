import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import nltk


def get_data_from_book(url, book_title, num_data_pts):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    words = re.findall("\w+", text)
    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.csv", "w") as f:
        f.write(" ".join(lowered))
    return lowered


def plot_most_freq_words(lowered, num_data_pts):
    text = nltk.Text(lowered)
    f_dist = nltk.FreqDist(lowered)
    f_dist.plot(num_data_pts)
