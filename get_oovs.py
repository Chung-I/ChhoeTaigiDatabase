import argparse
from tsm.lexicon import Lexicon
from tsm.util import read_file_to_lines, write_lines_to_file

parser = argparse.ArgumentParser()
parser.add_argument('lexicon_path')
parser.add_argument('src_path')
parser.add_argument('dest_path')
parser.add_argument('--with-prob', action='store_true')
args = parser.parse_args()

lexicon = Lexicon.from_kaldi(args.lexicon_path, args.with_prob)

lines = read_file_to_lines(args.src_path)
oovs = lexicon.get_oovs(lines)
write_lines_to_file(args.dest_path, oovs)
