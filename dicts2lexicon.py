import argparse
import pandas as pd
from collections import defaultdict
from itertools import chain
import regex as re
from pathlib import Path
import numpy as np
from tsm.POJ_TL import poj_tl
from tsm.lexicon import Lexicon
import zhon.hanzi

parser = argparse.ArgumentParser()
parser.add_argument('--dictionary-grapheme-phoneme-mapping')
parser.add_argument('--output-lexicon-path')
parser.add_argument('--syllable-phoneme-mapping-file')
parser.add_argument('--with-tone', action='store_true')
parser.add_argument('--write-raw', action='store_true')
args = parser.parse_args()

def process_sent(sent):
    return [match.group() for match in re.finditer(f"[{zhon.hanzi.characters}]|[^{zhon.hanzi.characters}\W]+", sent)] 

df = pd.read_csv(args.dictionary_grapheme_phoneme_mapping)
if args.write_raw:
    dictionaries = [Lexicon.from_dictionary_to_entries(*triple, raw_entries=True)
                    for triple in list(zip(df["file"], df["grapheme"], df["phoneme"]))]
    src_fp = open(Path(args.output_lexicon_path).joinpath("dict_mandarin.txt"), 'w')
    tgt_fp = open(Path(args.output_lexicon_path).joinpath("dict_taibun.txt"), 'w')
    for graph, pron in chain(*dictionaries):
        graph = " ".join(process_sent(graph))
        pron = " ".join(process_sent(pron))
        if graph.strip() and pron.strip():
            src_fp.write(graph + '\n')
            tgt_fp.write(pron + '\n')
else:
    dictionaries = [Lexicon.from_dictionary_to_entries(*triple)
                    for triple in list(zip(df["file"], df["grapheme"], df["phoneme"]))]
    lexicon = Lexicon(chain(*dictionaries), sum_dup_pron_probs=False)
    lexicon.write(args.output_lexicon_path)
