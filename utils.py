import requests
import re
import matplotlib.pyplot as plt
import nltk
import polyglot
from polyglot.text import Text, Word
from polyglot.downloader import downloader
from polyglot.detect import Detector

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


def get_alliteration_score(sentences):
    count, total_words = 0, 0
    proximity = 4
    i = 0
    for sentence in sentences:
        current_phonemes = [None] * proximity
        for word in sentence:
            word = no_punct(word)
            total_words += 1
            if word not in stopwords:
                if get_phonemes(word)[0] in current_phonemes:
                    count += 1
                current_phonemes[i] = get_phonemes(word)[0]
                i = 0 if i == 1 else 1

    alliteration_score = count / total_words
    return alliteration_score


def get_alliteration_by_phoneme(sentences):
    count, total_words = 0, 0
    proximity = 4
    i = 0
    phoneme_dict = {}
    for sentence in sentences:
        current_phonemes = [None] * proximity
        for word in sentence:
            word = no_punct(word)
            total_words += 1
            if word not in stopwords:
                phoneme = get_phonemes(word)[0]
                if phoneme in current_phonemes:
                    if phoneme not in phoneme_dict:
                        phoneme_dict[phoneme] = 1
                    else:
                        phoneme_dict[phoneme] += 1
                current_phonemes[i] = get_phonemes(word)[0]
                i = 0 if i == 1 else 1
    phonemes = list(phoneme_dict.keys())
    num_occurences = list(phoneme_dict.values())
    plt.bar(range(len(phoneme_dict)), num_occurences, tick_label=phonemes)
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
    print(main_entity.positive_sentiment)
    print(main_entity.negative_sentiment)


def get_sentiment_analysis_one_book():
    pass


def word_uniqueness_against_all_books(first_book, all_books):
    pass


def use_of_phallic_symbols(all_books):
    pass
