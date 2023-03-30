"""
Plot literary analysis data from text files scraped from Project Gutenberg
"""


# Imports
import re
import itertools
import nltk
from polyglot.text import Text
import matplotlib.pyplot as plt
from wordcloud import WordCloud


phoneme_dictionary = nltk.corpus.cmudict.dict()
ALPHABETS = "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He's|She's|It's|They' \
|Their's|Ours|We's|But's|However's|That's|This's|Wherever)"
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
20 most common words in the text and the number of times
they appear. Generate a bar graph for each text.

Args:
    list_of_urls: A list of tuples where the first parameter
    is a string representing the txt file url and the second
    is the name (str) of the local text file on the machine.
    
    num_data_pts: An int representing the number of most
    frequent words to plot on the bar graph.

Returns:
    lists_most_freq: A dictionary where the keys are the 20
    most frequently used words (strs) in the book and the values
    are the number of times (ints) they appeared in the text.
"""


def plot_most_freq_words_texts(list_of_urls, num_data_pts):
    word_dict = {}
    print(list_of_urls)
    for book in list_of_urls:
        print(book)
        sentences = get_sentences_from_txt(book[1])
        lowered_sentences = split_sentences_into_lists_of_words(sentences)
        word_dict = {}
        for sentence in lowered_sentences:
            for word in sentence:
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        sorted(word_dict, key=word_dict.get, reverse=True)
        lists_most_freq = dict(itertools.islice(word_dict.items(), num_data_pts))
        words = list(lists_most_freq.keys())
        freqs = list(lists_most_freq.values())
    return lists_most_freq


def plot_freq_bar(lists_most_freq, words, freqs, book):
    fig, ax = plt.subplots()
    plt.bar(range(len(lists_most_freq)), freqs, tick_label=words)
    fig.set_figheight(7)
    fig.set_figwidth(20)
    ax.set_title(book[1])
    plt.xticks(fontsize=10)


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
    for word in text:
        lowered.append(word.lower())
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
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "Hon." in text:
        text = text.replace("Hon.", "Hon<prd>")
    if "Rev." in text:
        text = text.replace("Rev.", "Rev<prd>")
    if "D.D.:" in text:
        text = text.replace("D.D.:", "D<prd>D<prd>")
    text = re.sub("\s" + ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(ACRONYMS + " " + STARTERS, "\\1<stop> \\2", text)
    text = re.sub(
        ALPHABETS + "[.]" + ALPHABETS + "[.]" + ALPHABETS + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(ALPHABETS + "[.]" + ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text)
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
For each book in the list of urls, call
the function that plots the number of times a
particular phoneme is used in an alliterative sequence.
"""


def get_all_alliteration_by_phoneme():
    for book in list_of_urls:
        get_alliteration_by_phoneme(book[1])


"""
Retrieve the first phoneme associated with a
given word.

Look up and return the first phoneme associated
with the given word to 

Args:
    word: A string representing a word in a text.

Returns:
    A string representing the first phoneme
    associated with the word.
"""


def get_phonemes(word):
    if word in phoneme_dictionary:
        return phoneme_dictionary[word][0]  # return first entry by convention
    else:
        return ["NONE"]  # no entries found for input word


"""
Create 3 plots: 1 of the number of times an
alliterative sequence occurs with a particular
phoneme in a text, one of the most popular words
to alliterate with in a text, and 1 of some
sample alliterative word pairs in the text.

Args:
    book_title: A string representing the title of a book. 

Returns:
    phoneme_dict: A dict mapping phonemes (str) to the
    number of times it was used (int) in an alliterative
    sequence in a given text.
"""


def get_alliteration_by_phoneme(book_title):
    sentences = get_sentences_from_txt(book_title)
    sentences = split_sentences_into_lists_of_words(sentences)
    # for sentence in sentences[0]:
    phonemes_in_sentence = []
    phoneme_dict = {}
    word_dict = {}
    pairs = []
    for sentence in sentences:
        phonemes_in_sentence = []
        for word in sentence:
            phonemes_in_sentence.append((get_phonemes(word)[0], word))
        for word_index in range(0, len(phonemes_in_sentence) - 2):
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
                    and (not phonemes_in_sentence[word_index][1] in common_words)
                    and (not phonemes_in_sentence[word_index + 1][1] in common_words)
                ):
                    if phonemes_in_sentence[word_index][0] not in phoneme_dict:
                        phoneme_dict[phonemes_in_sentence[word_index][0]] = 1
                        pairs.append(
                            (
                                f"({str(phonemes_in_sentence[word_index][1])}_{str(phonemes_in_sentence[word_index + 1][1])})"
                            )
                        )
                    else:
                        phoneme_dict[phonemes_in_sentence[word_index][0]] += 1

                    if phonemes_in_sentence[word_index][1] not in word_dict:
                        word_dict[phonemes_in_sentence[word_index][1]] = 1
                    else:
                        word_dict[phonemes_in_sentence[word_index][1]] += 1
    print(word_dict)
    if "NONE" in phoneme_dict:
        del phoneme_dict["NONE"]
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
    ax1.set_ylabel("Number of Occurences of Alliteration by Phoneme in All Sentences")
    # spacing = 0.6
    plt.xticks(fontsize=10)
    # fig.subplots_adjust(top=spacing + 0.1)
    # fig.subplots_adjust(bottom=spacing)
    ax1.bar(
        range(len(phoneme_dict)), num_occurences, tick_label=phonemes, color="orange"
    )

    # print(word_dict)
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
    return phoneme_dict


"""
Create a pie chart representing the number of
words in a given text with a positive, negative,
and neutral association.

Args:
    text_file: A text file representing the name of text.

Returns:
    A tuple representing the number of postively, negatively,
    and neutrally (ints) associated words in a text.
"""


def get_polarity_whole_text(text_file):
    f_text = ""
    with open(f"{text_file}.txt", "r") as f:
        for line in f:
            f_text += line
    text = Text(f_text)
    print("{:<16}{}".format("Word", "Polarity") + "\n" + "-" * 30)
    num_negative = 0
    num_positive = 0
    num_neutral = 0
    for w in text.words:
        if w.polarity == 1:
            num_positive += 1
        elif w.polarity == -1:
            num_negative += 1
        else:
            num_neutral += 1
    labels = "Positive", "Negative", "Neutral"
    sizes = [num_positive, num_negative, num_neutral]
    plt.rcParams["text.color"] = "r"
    fig, ax = plt.subplots()
    plt.title(f"{text_file.upper()}")
    ax.pie(
        sizes,
        labels=labels,
        colors=["violet", "paleturquoise", "rosybrown"],
        autopct="%1.1f%%",
    )
    return (num_positive, num_negative, num_neutral)


"""
Generate a word polarity pie chart for every text.
"""


def get_polarity_all_texts():
    for book in list_of_urls:
        get_polarity_whole_text(book[1])


"""
Given a list of texts, create a bar graph
representing the average sentence length
for each text.

Returns: 
    sentence_lengths: A dictionary mapping
    texts (string) to their average sentence
    length (int).
"""


def get_avg_sentence_length_all_books():
    sentence_lengths = {}
    for book in list_of_urls:
        sentences = get_sentences_from_txt(book[1])
        total = 0
        for sentence in sentences:
            total += len(sentence)
        num_sentences = len(sentences)
        sentence_lengths[book[1]] = total / num_sentences
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
    return sentence_lengths
