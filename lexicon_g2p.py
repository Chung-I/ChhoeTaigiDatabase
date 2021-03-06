import argparse

from tsm.lexicon import Lexicon
from tsm.util import read_file_to_lines, write_lines_to_file
from tsm.sentence import Sentence

parser = argparse.ArgumentParser()
parser.add_argument('lexicon_path')
parser.add_argument('src_path')
parser.add_argument('dest_path')
parser.add_argument('--with-prob', action='store_true')
parser.add_argument('--pos-tagged', action='store_true')
parser.add_argument('--remove-punct', action='store_true')
parser.add_argument('--segmented', action='store_true')
args = parser.parse_args()

if args.with_prob is None:
    args.with_prob = args.lexicon_path.endswith('lexiconp.txt')
lexicon = Lexicon.from_kaldi(args.lexicon_path, args.with_prob)
lines = read_file_to_lines(args.src_path)
sents = [Sentence.from_line(line, remove_punct=args.remove_punct,
                            segmented=args.segmented,
                            pos_tagged=args.pos_tagged)
         for line in lines]

phn_sents = [[lexicon.get_most_probable(word, "NULL") for word in sent] for sent in sents]

phn_lines = [" ".join(phn_sent) for phn_sent in phn_sents]
write_lines_to_file(args.dest_path, phn_lines)
