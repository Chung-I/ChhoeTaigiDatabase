import argparse
import re

from tsm.util import read_file_to_lines, write_lines_to_file

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('map_file')
parser.add_argument('output_file')
parser.add_argument('--col', type=int, help="starting from which column")
parser.add_argument('--delimiter', default="\s+")

args = parser.parse_args()
def line2word_syls(line):
    cols = re.split(args.delimiter, line)
    return cols[:args.col], list(filter(lambda col: col, cols[args.col:]))

syl_lines = read_file_to_lines(args.input_file)
syl_lexicon = list(map(line2word_syls, syl_lines))

def line2syl_phn(line):
    idx = line.index(" ")
    return line[:idx], line[idx+1:]

map_lines = read_file_to_lines(args.map_file)
mapping = dict(map(line2syl_phn, map_lines))

def map_syltone(syl):
    tone = int(syl[-1])
    phns = mapping[syl[:-1]]
    return f"{phns}{tone}"

phn_lexicon = []
for before_syls, syls in syl_lexicon:
    try:
        tup = (" ".join(before_syls), " ".join([map_syltone(syl) for syl in syls]))
        phn_lexicon.append(tup)
    except KeyError:
        continue

phn_lines = [f"{word} {phns}" for word, phns in phn_lexicon]
write_lines_to_file(args.output_file, phn_lines)
