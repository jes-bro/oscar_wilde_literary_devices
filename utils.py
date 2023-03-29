import requests
import re
import matplotlib.pyplot as plt
import nltk
import polyglot
from polyglot.text import Text, Word
from polyglot.downloader import downloader
from polyglot.detect import Detector
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He's|She's|It's|They's|Their's|Ours|We's|But's|However's|That's|This's|Wherever)"
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
            f.write(f"{i}")
    return lowered


def remove_extra_text(lowered, start_word):
    new_lowered = lowered[lowered.index(start_word) : lowered.index("***end")]

    common_words = []
    with open("commons.csv", "r") as f:
        for line in f:
            common_words.append(line.strip("\n"))

    for index, words in enumerate(common_words):
        for _ in range(new_lowered.count(words)):
            new_lowered.remove(words)

    return new_lowered


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


def get_lowered_from_txt(book_title):
    f_text = ""
    with open(f"{book_title}.txt", "r") as f:
        for line in f:
            f_text += line
    words = re.findall("\w+", f_text)
    lowered = []
    for word in words:
        lowered.append(word.lower())
    return lowered


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


# nltk.download("cmudict")
# nltk.download("stopwords")
phoneme_dictionary = nltk.corpus.cmudict.dict()
stress_symbols = [
    "0",
    "1",
    "2",
    "3...",
    "-",
    "!",
    "+",
    "/",
    "#",
    ":",
    ":1",
    ".",
    ":2",
    "?",
    ":3",
]
# nltk.download('stopwords') ## download stopwords (the, a, of, ...)
# nltk.download("cmudict")
# nltk.corpus.reader.cmudict
# Get stopwords that will be discarded in comparison
stopwords = nltk.corpus.stopwords.words("english")
# Function for removing all punctuation marks (. , ! * etc.)
no_punct = lambda x: re.sub(r"[^\w\s]", "", x)


def get_phonemes(word):
    if word in phoneme_dictionary:
        return phoneme_dictionary[word][0]  # return first entry by convention
    else:
        return ["NONE"]  # no entries found for input word


def get_alliteration_by_phoneme(sentences, book_title, sentence_num):
    count, total_words = 0, 0
    proximity = 2
    i = 0
    sentences = split_sentences_into_lists_of_words(sentences)
    # for sentence in sentences[0]:
    phonemes_in_sentence = []
    phoneme_dict = {}
    sentence = sentences[sentence_num]
    word_dict = {}
    pairs = []
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
    # print(sentence)
    for sentence in sentences:
        phonemes_in_sentence = []
        for word in sentence:
            # print(f"{no_punct(word)}, {get_phonemes(word)[0]}")
            # word = word.replace(word, get_phonemes(word)[0])
            phonemes_in_sentence.append((get_phonemes(word)[0], word))
            # print(word)
        # print(phonemes_in_sentence)
        for word_index in range(0, len(phonemes_in_sentence) - 2):
            if (
                phonemes_in_sentence[word_index][0]
                == phonemes_in_sentence[word_index + 1][0]
            ) and (
                phonemes_in_sentence[word_index][1]
                != phonemes_in_sentence[word_index + 1][1]
            ):
                if (
                    not phonemes_in_sentence[word_index][0] == "NONE"
                    and not phonemes_in_sentence[word_index][1] in common_words
                ):
                    if phonemes_in_sentence[word_index][0] not in phoneme_dict:
                        print(
                            f"word 1: {phonemes_in_sentence[word_index]}, word 2: {phonemes_in_sentence[word_index + 1]}"
                        )
                        phoneme_dict[phonemes_in_sentence[word_index][0]] = 1
                        pairs.append(
                            (
                                f"({str(phonemes_in_sentence[word_index][1])}_{str(phonemes_in_sentence[word_index + 1][1])})"
                            )
                        )
                    else:
                        print(
                            f"word 1: {phonemes_in_sentence[word_index]}, word 2: {phonemes_in_sentence[word_index + 1]}"
                        )
                        phoneme_dict[phonemes_in_sentence[word_index][0]] += 1
                if (
                    (
                        (not phonemes_in_sentence[word_index][0] == "NONE")
                        and (not phonemes_in_sentence[word_index + 1][0] == "NONE")
                    )
                    and (not phonemes_in_sentence[word_index][1] in common_words)
                    and (not phonemes_in_sentence[word_index + 1][1] in common_words)
                ):
                    if phonemes_in_sentence[word_index][1] not in word_dict:
                        # print(
                        #    f"word 1: {phonemes_in_sentence[word_index]}, word 2: {phonemes_in_sentence[word_index + 1]}"
                        # )
                        word_dict[phonemes_in_sentence[word_index][1]] = 1
                    else:
                        # print(
                        #   f"word 1: {phonemes_in_sentence[word_index]}, word 2: {phonemes_in_sentence[word_index + 1]}"
                        # )
                        word_dict[phonemes_in_sentence[word_index][1]] += 1

                # or phonemes_in_sentence[word_index][0]
                # == phonemes_in_sentence[word_index + 2][0]
                #   and phonemes_in_sentence[word_index][1]
                #!= phonemes_in_sentence[word_index + 2][1]
    # print(phoneme_dict)
    if "NONE" in phoneme_dict:
        del phoneme_dict["NONE"]
    phonemes = list(phoneme_dict.keys())
    num_occurences = list(phoneme_dict.values())
    fig = plt.figure()
    fig.tight_layout()
    fig, (ax2, ax3) = plt.subplots(1, 2)
    ax1 = fig.add_subplot(222)
    ax2.title.set_text(f"Phoneme Usage in {book_title}")
    ax1.title.set_text("Most Frequently Alliterated words")
    ax3.title.set_text("Sample Alliterative Pairings")

    fig.set_figheight(15)
    fig.set_figwidth(20)
    ax1.set_xlabel("Phoneme")
    ax1.set_ylabel("Number of Occurences of Alliteration by Phoneme in All Sentences")
    # spacing = 0.6
    plt.xticks(fontsize=10)
    # fig.subplots_adjust(top=spacing + 0.1)
    # fig.subplots_adjust(bottom=spacing)
    ax2.bar(range(len(phoneme_dict)), num_occurences, tick_label=phonemes)

    # print(word_dict)
    wc = WordCloud(
        background_color="black",
        width=1000,
        height=1000,
        max_words=10,
        relative_scaling=0.5,
        normalize_plurals=True,
    ).generate_from_frequencies(word_dict)
    ax1.imshow(wc)

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
    # downloader.download("embeddings2.un")
    # downloader.download("embeddings2.en")
    f_text = ""
    with open(f"{text_file}.txt", "r") as f:
        for line in f:
            f_text += line
    detector = Detector(f_text)
    text = Text(f_text)
    print("{:<16}{}".format("Word", "POS Tag") + "\n" + "-" * 30)
    for word, tag in text.pos_tags:
        print("{:<16}{:>2}".format(word, tag))


def get_polarity_whole_text(text_file):
    f_text = ""
    with open(f"{text_file}.txt", "r") as f:
        for line in f:
            f_text += line
    detector = Detector(f_text)
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
        sizes, labels=labels, colors=["violet", "paleturquoise"], autopct="%1.1f%%",
    )


def get_sentiment_analysis_one_book():
    pass


def word_uniqueness_against_all_books(first_book, all_books):
    pass


def use_of_phallic_symbols(all_books):
    pass
