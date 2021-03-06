from tsm.util import read_file_to_lines, write_lines_to_file
from tsm.tsm_g2p import init, translate
init()
# You need to wait until the docker is ready.
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('output_path')
parser.add_argument('--seg', action='store_true')
args = parser.parse_args()

sents = read_file_to_lines(args.input_path)
sent_of_phonemes = []
fp = open(args.output_path, 'w')
for sent in sents:
    phonemes = translate(sent, args.seg)[1].看音()
    print(sent, phonemes)
    fp.write(sent + "\t" + phonemes + '\n')
fp.close()
#write_lines_to_file(args.output_path, sent_of_phonemes)

