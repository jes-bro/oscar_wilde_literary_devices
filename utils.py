import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import nltk

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"


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


# Maybe he was trying to show off
def plot_num_word_lengths_in_single_book(lowered):
    word_lengths = {}
    for word in lowered:
        if len(word) not in word_lengths:
            word_lengths[len(word)] = 1
        else:
            word_lengths[len(word)] += 1
    word_lens = list(sorted(word_lengths.keys()))
    num_occurences = list(word_lengths.values())
    plt.bar(range(len(word_lengths)), num_occurences, tick_label=word_lens)
    plt.show()


def get_lowered_from_csv(book_title):
    f_text = ""
    with open(f"{book_title}.csv", "r") as f:
        for line in f:
            f_text += line
    words = re.findall("\w+", f_text)
    lowered = []
    for word in words:
        lowered.append(word.lower())
    return lowered


def get_sentences_from_csv(book_title):
    f_text = ""
    with open(f"{book_title}.csv", "r") as f:
        for line in f:
            f_text += line
    sentences = split_into_lowered_sentences(f_text)
    return sentences


def split_into_lowered_sentences(text):
    lowered = []
    for word in text:
        lowered.append(word.lower())
    text = "".join(lowered)
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text:
        text = text.replace("...", "<prd><prd><prd>")
    if "www." in text:
        text = text.replace("www.", "www<prd>")
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "Hon." in text:
        text = text.replace("Hon.", "Hon<prd>")
    if "Rev." in text:
        text = text.replace("Rev.", "Rev<prd>")
    if "D.D.:" in text:
        text = text.replace("D.D.:", "D<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(
        alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def split_sentences_into_lists_of_words(sentences):
    for sentence_index, sentence in enumerate(sentences):
        sentences[sentence_index] = sentence.split(" ")
    return sentences

def count_alliteration_by_starting_letter(sentences):
    alliterations_by_first_letter = {}
    split_sentences = split_sentences_into_lists_of_words(sentences)
    for sentence in split_sentences:
        for word_index, word in enumerate(sentence):
            if word_index + 1 < len(sentence):
                first_letter_current_word = word[0]
                first_letter_next_word = sentence[word_index+1]
                if first_letter_current_word == first_letter_next_word:
                    

def word_uniqueness_against_all_books(first_book, all_books):
    pass


def use_of_phallic_symbols(all_books):
    pass
