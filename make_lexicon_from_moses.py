import argparse
from tsm.util import read_file_to_lines, write_lines_to_file, flatten
import re
from collections import namedtuple, defaultdict
from itertools import groupby
import zhon.hanzi
import functools
import operator

LexEntry = namedtuple('LexEntry', ['src', 'tgt', 'prob'])
def parse_line_to_entry(line, strip_punct=True, row=1, delimiter="\s+"):
    columns = re.split(delimiter, line)
    raw_src, raw_tgt, prob = columns[0].strip(), columns[1].strip(), columns[2]
    if raw_tgt == "NULL":
        return None
    if len(raw_src.split()) > 1:
        return None
    tgt_words = re.split("\s+", raw_tgt)
    tgt = " ".join([re.split("\uff5c", word)[row] for word in tgt_words])
    if strip_punct:
        src = "".join([match.group(0) for match in 
                       re.finditer(f"[{zhon.hanzi.characters}]", raw_src)])
        tgt = " ".join([match.group(0) for match in 
                        re.finditer(f"[A-Za-z]+\d", tgt)])
    if not (src and tgt):
        return None
    prob = functools.reduce(operator.mul, map(float, re.split("\s+", prob.strip())))
    return LexEntry(src, tgt, prob)

def main(args):
    lines = read_file_to_lines(args.lex_table, args.unicode_escape)
    entries = filter(lambda x: x, [parse_line_to_entry(line, delimiter=args.delimiter)
                                   for line in lines])
    raw_lexicon = groupby(sorted(entries), key=(lambda e: (e.src, e.tgt)))
    def merge_duplicate_entry(entries):
        entries = list(entries)
        e = entries[0]
        return LexEntry(e.src, e.tgt, sum(e.prob for e in entries))
    def map_entries(entries):
        entries = sorted(entries, key=lambda e: -e.prob)[:3]
        max_prob = entries[0].prob
        entries = [LexEntry(e.src, e.tgt, e.prob * (1 / max_prob)) for e in entries]
        return filter(lambda e: e.prob > 1e-5, entries)
    merged_lexicon = map(merge_duplicate_entry, map(operator.itemgetter(1), raw_lexicon))
    lexicon = groupby(sorted(merged_lexicon), key=(lambda e: e.src))
    pruned_lexicon = flatten(map(map_entries, map(operator.itemgetter(1), lexicon)))
    out_lines = map(lambda e: f"{e.src} {e.prob} {e.tgt}", pruned_lexicon)
    write_lines_to_file(args.lexicon_path, out_lines)

parser = argparse.ArgumentParser()
parser.add_argument('lex_table')
parser.add_argument('lexicon_path')
parser.add_argument('--delimiter')
parser.add_argument('--strip-punct', action='store_true')
parser.add_argument('--unicode-escape', action='store_true')
args = parser.parse_args()
main(args)
