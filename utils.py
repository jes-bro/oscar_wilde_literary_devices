import requests
import re
import matplotlib.pyplot as plt
import nltk

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


def remove_extra_text(lowered):
    new_lowered = lowered[lowered.index("chapter") : lowered.index("***end")]

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


def word_uniqueness_against_all_books(first_book, all_books):
    pass


def use_of_phallic_symbols(all_books):
    pass
