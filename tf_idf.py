import pandas as pd
import numpy as np
import utils


lord_arthur_saviles_crimes = utils.get_data_from_book(
    "https://www.gutenberg.org/files/773/773-0.txt",
    "Lord Arthur Savile's Crime And Other Short Stories",
)
the_happy_prince = utils.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/902/pg902.txt",
    "The Happy Prince and Other Short Stories",
)
the_picture_of_dorian_grey = utils.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/174/pg174.txt", "The Picture of Dorian Grey"
)
salome = utils.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/42704/pg42704.txt", "Salome"
)
a_house_of_pomegranates = utils.get_data_from_book(
    "https://www.gutenberg.org/files/873/873-0.txt", "A House of Pomegranates"
)
the_ducchess_of_padua = utils.get_data_from_book(
    "https://www.gutenberg.org/files/875/875-0.txt", "The Ducchess of Padua"
)
the_soul_of_man_under_socialism = utils.get_data_from_book(
    "https://www.gutenberg.org/files/1017/1017-0.txt", "The Soul of Man Under Socialism"
)
lady_windermeres_fan = utils.get_data_from_book(
    "https://www.gutenberg.org/files/790/790-0.txt", "Lady Windermeres Fan"
)
a_woman_of_no_importance = utils.get_data_from_book(
    "https://www.gutenberg.org/files/854/854-0.txt", "A Woman of No Importance"
)
the_importance_of_being_earnest = utils.get_data_from_book(
    "https://www.gutenberg.org/files/844/844-0.txt", "The Importance of Being Earnest"
)
the_ballad_of_reading_gaol = utils.get_data_from_book(
    "https://www.gutenberg.org/cache/epub/301/pg301.txt", "The Ballad of Reading Gaol"
)
an_ideal_husband = utils.get_data_from_book(
    "https://www.gutenberg.org/files/885/885-0.txt", "An Ideal Husband"
)

corpus = [
    lord_arthur_saviles_crimes,
    the_happy_prince,
    the_picture_of_dorian_grey,
    salome,
    a_house_of_pomegranates,
    the_ducchess_of_padua,
    the_soul_of_man_under_socialism,
    lady_windermeres_fan,
    a_woman_of_no_importance,
    the_importance_of_being_earnest,
    the_ballad_of_reading_gaol,
    an_ideal_husband,
]

def compute_tf_idf_ow_corpus 
