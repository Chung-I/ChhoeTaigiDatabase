import argparse
import pandas as pd
from collections import defaultdict
from itertools import chain
import re
import numpy as np
from local.POJ_TL import poj_tl
from local.lexicon import Lexicon

parser = argparse.ArgumentParser()
parser.add_argument('--dictionary-grapheme-phoneme-mapping')
parser.add_argument('--output-lexicon-path')
parser.add_argument('--syllable-phoneme-mapping-file')
parser.add_argument('--with-tone', action='store_true')
args = parser.parse_args()

df = pd.read_csv(args.dictionary_grapheme_phoneme_mapping)
dictionaries = [Lexicon.from_dictionary_to_entries(*triple)
                for triple in list(zip(df["file"], df["grapheme"], df["phoneme"]))]
lexicon = Lexicon(chain(*dictionaries))
lexicon.write(args.output_lexicon_path)
