# coding=utf-8
"""
Build vocab with a set max vocab size.
Build token ids given the vocab.
Do get_data.py first.
"""
# from __future__ import unicode_literals, print_function, division
import argparse
import os
import subprocess
import re
from unidecode import unidecode
from nltk import word_tokenize

from model import CACHE_DIR
from model.translate.data_utils import create_vocabulary, data_to_token_ids
from model.get_data import MODERN_FILENAME, ORIGINAL_FILENAME, TRAIN_SUFFIX, DEV_SUFFIX

# from model.get_data import MODERN_PATH, ORIGINAL_PATH, MODERN_TRAIN_PATH, MODERN_DEV_PATH, ORIGINAL_TRAIN_PATH, \
# ORIGINAL_DEV_PATH

# TODO: integrate all this in translate.py
# MODERN_VOCAB_FILENAME = "all_modern.vocab"
# ORIGINAL_VOCAB_FILENAME = "all_original.vocab"
ORIGINAL_VOCAB_FILENAME = "original.vocab"
EDITED_VOCAB_FILENAME = "edited.vocab"

MODERN_VOCAB_MAX = 10000
ORIGINAL_VOCAB_MAX = 10000

IDS_SUFFIX = ".ids"

ORIGINAL_VOCAB_PATH = os.path.join(CACHE_DIR, ORIGINAL_VOCAB_FILENAME)
EDITED_VOCAB_PATH = os.path.join(CACHE_DIR, EDITED_VOCAB_FILENAME)

ORIGINAL_TRAIN_IDS_PATH = os.path.join(CACHE_DIR, "original" + TRAIN_SUFFIX + IDS_SUFFIX)
ORIGINAL_DEV_IDS_PATH = os.path.join(CACHE_DIR, "original" + DEV_SUFFIX + IDS_SUFFIX)

EDITED_TRAIN_IDS_PATH = os.path.join(CACHE_DIR, "edited" + TRAIN_SUFFIX + IDS_SUFFIX)
EDITED_DEV_IDS_PATH = os.path.join(CACHE_DIR, "edited" + DEV_SUFFIX + IDS_SUFFIX)

_WORD_SPLIT = re.compile("([.,!?\"':;)(])")
PATH = ''
ORIGINAL_PATH = None
EDITED_PATH = None
ORIGINAL_TRAIN_PATH = None
ORIGINAL_DEV_PATH = None
EDITED_TRAIN_PATH = None
EDITED_DEV_PATH = None


def _tokenizer(sentence):
    """Very basic tokenizer: split the sentence into a list of tokens + lower()."""
    words = []
    for space_separated_fragment in sentence.lower().strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    return [w for w in words if w]


def tokenizer(sentence):  # TODO: not working for apostrophes
    sentence = sentence.strip().lower()
    if type(sentence) != unicode:
        sentence = unicode(sentence, encoding='utf-8', errors='replace')
    sentence = unidecode(sentence)
    sentence = sentence.replace("' ", "'")
    return word_tokenize(sentence)


def build_vocab():
    create_vocabulary(ORIGINAL_VOCAB_PATH, ORIGINAL_PATH, MODERN_VOCAB_MAX, tokenizer=tokenizer)
    create_vocabulary(EDITED_VOCAB_PATH, EDITED_PATH, ORIGINAL_VOCAB_MAX, tokenizer=tokenizer)

    print(subprocess.check_output(['wc', '-l', ORIGINAL_VOCAB_PATH]))
    print(subprocess.check_output(['wc', '-l', EDITED_VOCAB_PATH]))


def build_ids():
    data_to_token_ids(ORIGINAL_TRAIN_PATH, ORIGINAL_TRAIN_IDS_PATH, ORIGINAL_VOCAB_PATH, tokenizer=tokenizer)
    data_to_token_ids(ORIGINAL_DEV_PATH, ORIGINAL_TRAIN_IDS_PATH, ORIGINAL_VOCAB_PATH, tokenizer=tokenizer)
    data_to_token_ids(EDITED_TRAIN_PATH, EDITED_TRAIN_IDS_PATH, EDITED_VOCAB_PATH, tokenizer=tokenizer)
    data_to_token_ids(EDITED_DEV_PATH, EDITED_DEV_IDS_PATH, EDITED_VOCAB_PATH, tokenizer=tokenizer)

    print(subprocess.check_output(['wc', '-l', ORIGINAL_TRAIN_IDS_PATH]))
    print(subprocess.check_output(['wc', '-l', ORIGINAL_TRAIN_IDS_PATH]))
    print(subprocess.check_output(['wc', '-l', EDITED_TRAIN_IDS_PATH]))
    print(subprocess.check_output(['wc', '-l', EDITED_DEV_IDS_PATH]))


def divide_data():

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Relative/Absolute path to the data folder")
    args = parser.parse_args()
    print args.folder
    global PATH
    PATH = args.folder
    divide_data()
    build_vocab()
    build_ids()
