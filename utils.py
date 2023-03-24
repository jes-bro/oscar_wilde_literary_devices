import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import nltk


def get_data_from_book(url, book_title):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    words = re.findall("\w+", text)
    lowered = []
    for word in words:
        lowered.append(word.lower())

    with open(f"{book_title}.csv", "w") as f:
        f.write(" ".join(words))
    # text = nltk.text(lowered)
    # fdist = nltk.FreqDist(text)
    # fdist.plot(n)
