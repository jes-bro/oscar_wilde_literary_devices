import re
import itertools
import requests
import nltk
from polyglot.text import Text
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import text_processing

phoneme_dictionary = nltk.corpus.cmudict.dict()
ALPHABETS = "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He's|She's|It's|They's|Their's|Ours|We's|But's|However's|That's|This's|Wherever)"
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


def plot_most_freq_words_texts():
    word_dict = {}
    for book in list_of_urls:
        sentences = get_sentences_from_txt(book[1])
        lowered_sentences = split_sentences_into_lists_of_words(sentences)
        word_dict = {}
        for sentence in lowered_sentences:
            for word in sentence:
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
        lists_most_freq = dict(itertools.islice(word_dict.items(), 20))
        print(lists_most_freq)
        words = list(lists_most_freq.keys())
        freqs = list(lists_most_freq.values())
        fig, ax = plt.subplots()
        plt.bar(range(len(lists_most_freq)), freqs, tick_label=words)
        fig.set_figheight(7)
        fig.set_figwidth(20)
        ax.set_title(book[1])
        plt.xticks(fontsize=10)


def plot_most_freq_words_all_texts_at_once():
    num_data_pts = 30
    sentences = []
    lowered_sentences = []
    for book in list_of_urls:
        sentences = get_sentences_from_txt(book[1])
        lowered_sentences.append(split_sentences_into_lists_of_words(sentences))
    f_dist = nltk.FreqDist(lowered_sentences)
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


def get_sentences_from_txt(book_title):
    f_text = ""
    with open(f"{book_title}.txt", "r") as f:
        for line in f:
            f_text += line
    sentences = split_into_lowered_sentences(f_text)
    return sentences


# Maybe figure out how to get rid of extra \
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


def split_sentences_into_lists_of_words(sentences):
    for sentence_index, sentence in enumerate(sentences):
        sentences[sentence_index] = sentence.split(" ")
    return sentences


def get_all_alliteration_by_phoneme():
    for book in list_of_urls:
        get_alliteration_by_phoneme(book[1])


def get_phonemes(word):
    if word in phoneme_dictionary:
        return phoneme_dictionary[word][0]  # return first entry by convention
    else:
        return ["NONE"]  # no entries found for input word


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


def get_part_of_speech_usage_one_book(text_file):
    f_text = ""
    with open(f"{text_file}.txt", "r") as f:
        for line in f:
            f_text += line
    text = Text(f_text)
    print("{:<16}{}".format("Word", "POS Tag") + "\n" + "-" * 30)
    for word, tag in text.pos_tags:
        print("{:<16}{:>2}".format(word, tag))


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
        # print("{:<16}{:>2}".format(w, w.polarity))
    print(
        f"Num positive: {num_positive}, Num negative: {num_negative}, Num neutral: {num_neutral}"
    )
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


def get_polarity_all_texts():
    for book in list_of_urls:
        get_polarity_whole_text(book[1])


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


def get_polarity_character(text_file, main_character):
    sentences = get_sentences_from_txt(text_file)
    main_character = main_character.lower()
    sentences_with_main_present = []
    for sentence in sentences:
        if main_character in sentence:
            sentences_with_main_present.append(sentence)
    all_main_together = " ".join(sentences_with_main_present)
    all_main_together = all_main_together.replace(".", " ")
    all_main_together = all_main_together.replace("oscar", "")
    all_main_together = all_main_together.replace("wilde", "")
    all_main_together = all_main_together.replace("gutenberg", "")
    all_main_together = all_main_together.replace("alfred", "")
    all_main_together = all_main_together.replace("drake", "")
    print(all_main_together)
    text = Text(all_main_together)
    one_sentence = text.sentences[0]
    # print(one_sentence)
    main_entity = one_sentence.entities[0]
    print(main_entity)
    positive_score = main_entity.positive_sentiment
    negative_score = main_entity.negative_sentiment
    labels = "Positive", "Negative"
    sizes = [positive_score, negative_score]
    plt.rcParams["text.color"] = "r"
    fig, ax = plt.subplots()
    plt.title(f"{main_character.upper()}")
    ax.pie(
        sizes,
        labels=labels,
        colors=["violet", "paleturquoise"],
        autopct="%1.1f%%",
    )


def use_of_phallic_symbols(all_books):
    pass
