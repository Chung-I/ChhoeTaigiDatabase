import argparse
from tsm.util import read_file_to_lines, write_lines_to_file, flatten
import re
from collections import namedtuple, defaultdict
from itertools import groupby
import zhon.hanzi
import functools
import operator
from tsm.lexicon import Lexicon

parser = argparse.ArgumentParser()
parser.add_argument('lex_table')
parser.add_argument('lexicon_path')
parser.add_argument('--top-k', type=int, default=3)
parser.add_argument('--min-prob', type=float, default=1e-5)
#parser.add_argument('--delimiter')
#parser.add_argument('--strip-punct', action='store_true')
parser.add_argument('--unicode-escape', action='store_true')
args = parser.parse_args()

lexicon = Lexicon.from_moses(args.lex_table, args.unicode_escape)
lexicon.prune_lexicon(args.top_k, args.min_prob)
lexicon.write(args.lexicon_path)
