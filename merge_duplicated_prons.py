import argparse
from tsm.lexicon import Lexicon

parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('output_path')
parser.add_argument('--no-sum-probs', action='store_true')
args = parser.parse_args()

lexicon = Lexicon.from_kaldi(args.input_path, with_prob=True,
                             sum_dup_pron_probs=not args.no_sum_probs)
lexicon.write(args.output_path)
