"""
Plot literary analysis data from text files scraped from Project Gutenberg
"""


# Imports
import re
import itertools
import nltk
from polyglot.text import Text
import math

phoneme_dictionary = nltk.corpus.cmudict.dict()
ALPHABETS = "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = (
    "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He's|She's|It's|They'"
    " |Their's|Ours|We's|But's|However's|That's|This's|Wherever)"
)
ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
WEBSITES = "[.](com|net|org|io|gov|edu|me)"
DIGITS = "([0-9])"

list_of_urls = [
    ("https://www.gutenberg.org/files/885/885-0.txt", "ideal_husband"),
    ("https://www.gutenberg.org/cache/epub/42704/pg42704.txt", "salome"),
    ("https://www.gutenberg.org/files/844/844-0.txt", "importance_earnest"),
    ("https://www.gutenberg.org/cache/epub/921/pg921.txt", "de_profundis"),
    ("https://www.gutenberg.org/cache/epub/30120/pg30120.txt", "happy_prince"),
]

list_of_test_urls = [""]

common_words = [
    "is",
    "it",
    "when",
    "what",
    "was",
    "his",
    "who",
    "to",
    "that",
    "we",
    "and",
    "had",
    "he",
    "an",
    "of",
    "be",
    "some",
    "which",
    "than",
    "so",
    "made",
    "makes",
    "how",
    "with",
    "me",
    "one",
    "about",
    "can",
    "have",
    "or",
    "not",
    "then",
    "upon",
    "been",
    "you",
    "your",
    "see",
    "has",
    "her",
    "but",
    "much",
    "never",
    "them",
    "something",
    "in",
    "world",
    "women",
    "will",
    "by",
    "man",
    "could",
    "know",
    "fell",
    "make",
    "such",
    "long",
    "through",
    "certainly",
    "knows",
    "came",
    "though",
    "henry's",
    "can't",
    "work",
    "as",
    "an",
    "anyone",
    "anywhere",
]

"""
Split a list of strings representing sentences
into lists of lists of strings, where the
elements at each index in the inner lists are
words and the list containing the words is a
sentence

Args:
    sentences: A list of strings representing
    the sentences in a given text.

Returns:
    sentences: A list of lists of strings
    representing lists of the words in every
    sentence.
"""


def split_sentences_into_lists_of_words(sentences):
    for sentence_index, sentence in enumerate(sentences):
        sentences[sentence_index] = sentence.split(" ")
    return sentences


"""
Create sentences by reading a text file. 

Split the text from a single text in
the corpus into a list of strings of
sentences.

Args:
    book_title: A string representing
    the title of the book. 

Returns:
    sentences: A list of strings representing each
    sentence in the given text.
"""


def get_sentences_from_txt(book_title):
    f_text = ""
    with open(f"{book_title}.txt", "r") as f:
        for line in f:
            f_text += line
    sentences = split_into_lowered_sentences(f_text)
    return sentences


"""
Plot the most frequent words appearing in a text in a plot,
for all texts in the corpus.

For each text in the corpus, generate a dictionary of the
num_data_pts most common words in the text and the number of times
they appear. 

Args:
    list_of_urls: A list of tuples where the first parameter
    is a string representing the txt file url and the second
    is the name (str) of the local text file on the machine.
    
    num_data_pts: An int representing the number of most
    frequent words to include in the most_freq dictionary

Returns:
    most_freq: A dictionary where the keys are the num_data_pts
    most frequently used words (strs) in the book and the values
    are the number of times (ints) they appeared in the texts.
"""


def plot_most_freq_words_texts(list_of_urls, num_data_pts):
    word_dict = {}
    for book in list_of_urls:
        sentences = get_sentences_from_txt(book[1])
        lowered_sentences = split_sentences_into_lists_of_words(sentences)
        for sentence in lowered_sentences:
            for word in sentence:
                if "." in word:
                    word = word.replace(".", "")
                if "?" in word:
                    word = word.replace("?", "")
                if "'" in word:
                    word = word.replace("'", "")
                word = word.lower()
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
    sorted_dict = sorted(word_dict, key=word_dict.get, reverse=True)
    sorted_keys = sorted(word_dict, key=word_dict.get, reverse=True)
    values = []
    for key in sorted_keys:
        values.append(word_dict[key])
    most_freq = dict(zip(sorted_keys, values))
    most_freq = dict(itertools.islice(most_freq.items(), num_data_pts))

    return most_freq


"""
Split a string of text into a list of sentences,
accounting for special cases where periods
occur that do not mean that a sentence is ending.

Args:
    text: A string representing text read from
    a text file.

Returns:
    sentences: A list of strings representing each
    sentence in the given text.
"""


def split_into_lowered_sentences(text):
    lowered = []
    for character in text:
        lowered.append(character.lower())
    text = "".join(lowered)
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(PREFIXES, "\\1<prd>", text)
    text = re.sub(WEBSITES, "<prd>\\1", text)
    text = re.sub(DIGITS + "[.]" + DIGITS, "\\1<prd>\\2", text)
    if "..." in text:
        text = text.replace("...", "<prd><prd><prd>")
    if "www." in text:
        text = text.replace("www.", "www<prd>")
    if "ph.d" in text:
        text = text.replace("ph.d", "ph<prd>D<prd>")
    if "hon." in text:
        text = text.replace("hon.", "hon<prd>")
    if "rev." in text:
        text = text.replace("rev.", "rev<prd>")
    if "d.d.:" in text:
        text = text.replace("d.d.:", "d<prd>d<prd>")
    if "dr." in text:
        text = text.replace("dr.", "dr<prd>")
    if "mr." in text:
        text = text.replace("mr.", "mr<prd>")
    if "mrs." in text:
        text = text.replace("mrs.", "mrs<prd>")

    text = re.sub("\s" + ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(ACRONYMS + " " + STARTERS, "\\1<stop> \\2", text)
    text = re.sub(
        ALPHABETS + "[.]" + ALPHABETS + "[.]" + ALPHABETS + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(
        ALPHABETS + "[.]" + ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text
    )
    text = re.sub(" " + SUFFIXES + "[.] " + STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + ALPHABETS + "[.]", " \\1<prd>", text)
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


"""
Retrieve the phonemes associated with a
given word.

Look up and return the first phoneme associated
with the given word to 

Args:
    word: A string representing a word in a text.

Returns:
    A list of a string representing the phonemes
    associated with the word.
"""


def get_phonemes(word):
    if word in phoneme_dictionary:
        print(phoneme_dictionary[word])
        return phoneme_dictionary[word][0]
    else:
        return ["NONE"]


"""
Create two dictionaries that represent the number of alliterative
sequences with certain starting phonemes, the most frequently
alliterated words, and a list of sample word pairs for a given
text.

Args:
    book_title: A string representing the title of a book. 

Returns:
    phoneme_dict: A dict mapping phonemes (str) to the
    number of times it was used (int) in an alliterative
    sequence in a given text.
    word_dict: A dictionary mapping words (str) to the
    number of times they are used in alliterative
    sequences (int)
    pairs: A list of strings representing sample
    alliterative pairs from a text
"""


def get_alliteration_by_phoneme(book_title):
    sentences = get_sentences_from_txt(book_title)
    sentences = split_sentences_into_lists_of_words(sentences)
    phonemes_in_sentence = []
    phoneme_dict = {}
    word_dict = {}
    pairs = []
    for sentence in sentences:
        phonemes_in_sentence = []
        for word in sentence:
            # Append first phoneme only
            phonemes_in_sentence.append((get_phonemes(word)[0], word))
        for word_index in range(0, len(phonemes_in_sentence) - 1):
            if (
                phonemes_in_sentence[word_index][0]
                == phonemes_in_sentence[word_index + 1][0]
            ) and (
                phonemes_in_sentence[word_index][1]
                != phonemes_in_sentence[word_index + 1][1]
            ):
                if (
                    (not phonemes_in_sentence[word_index][0] == "NONE")
                    and (not phonemes_in_sentence[word_index + 1][0] == "NONE")
                    and (
                        not phonemes_in_sentence[word_index][1] in common_words
                    )
                    and (
                        not phonemes_in_sentence[word_index + 1][1]
                        in common_words
                    )
                ):
                    if phonemes_in_sentence[word_index][0] not in phoneme_dict:
                        phoneme_dict[phonemes_in_sentence[word_index][0]] = 1
                        pairs.append(
                            f"({str(phonemes_in_sentence[word_index][1])}_{str(phonemes_in_sentence[word_index + 1][1])})"
                        )
                    else:
                        phoneme_dict[phonemes_in_sentence[word_index][0]] += 1

                    if phonemes_in_sentence[word_index][1] not in word_dict:
                        word_dict[phonemes_in_sentence[word_index][1]] = 1
                    else:
                        word_dict[phonemes_in_sentence[word_index][1]] += 1

    if "NONE" in phoneme_dict:
        del phoneme_dict["NONE"]
    return phoneme_dict, word_dict, pairs


"""
Given a list of texts, create a dictionary mapping
the text name (str) to its average sentence length
(int)

Args:
    list_of_urls: list_of_urls: A list of tuples where the 
    first parameter is a string representing the txt file
    url and the second is the name (str) of the local text
    file on the machine.

Returns: 
    sentence_lengths: A dictionary mapping
    texts (string) to their average sentence
    length (int).
"""


def get_avg_sentence_length(list_of_urls):
    sentence_lengths = {}
    for book in list_of_urls:
        sentences = get_sentences_from_txt(book[1])
        sentences = split_sentences_into_lists_of_words(sentences)
        total = 0
        for sentence in sentences:
            total += len(sentence)
        num_sentences = len(sentences)
        sentence_lengths[book[1]] = math.floor(total / num_sentences)
    return sentence_lengths
