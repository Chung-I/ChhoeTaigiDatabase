import argparse
import re
import tqdm

import opencc
import cn2an

converter = opencc.OpenCC('s2tw.json')

from tsm.util import write_lines_to_file, read_file_to_lines, dict_seg

def parse_lexicon(lexicon_path):
    import pandas as pd
    df = pd.read_csv(lexicon_path)
    return list(df['詞目'])

#def convert_arabic_number_to_chinese(sent):
#    match = re.match("(\d+)年", sent)
#    if match:
#        import pdb
#        pdb.set_trace()
#        arabic = match.group(1)
#        start, end = match.span
#        chinese = cn2an.an2cn(arabic)
#        chinese = converter.convert(chinese)
#        new_sent = sent[:start] + chinese + sent[:end]
#        return convert_arabic_number_to_chinese(new_sent)
#    else:
#        return sent

parser = argparse.ArgumentParser()
parser.add_argument('--lexicon-path')
parser.add_argument('--input-path')
parser.add_argument('--output-path')
parser.add_argument('--filtered-output-path')
args = parser.parse_args()

lexicon = parse_lexicon(args.lexicon_path)

lines = read_file_to_lines(args.input_path)
texts = [" ".join(line.split()[2:]) for line in lines]

cnt = 0
cutted_sents = []
valid_line_nums = []
for idx, text in enumerate(texts):
    sents = re.split("\s+", text)
    words = []
    segmentable = True
    for sent in sents:
        sent = re.sub("[^\u4e00-\u9fa5A-Za-z0-9]", "", sent)
        sent = cn2an.transform(sent, "an2cn")
        sent = converter.convert(sent)
        maybe_words = dict_seg(sent, lexicon)
        if not maybe_words:
            segmentable = False
            cnt += 1
            break
        words += maybe_words
    if segmentable:
        valid_line_nums.append(idx)
    cutted_sents.append(" ".join(words))

if args.filtered_output_path is not None:
    write_lines_to_file(args.filtered_output_path, [lines[idx] for idx in valid_line_nums])
if args.output_path is not None:
    write_lines_to_file(args.output_path, cutted_sents)
print(f"{cnt} out of {len(lines)} lines has no proper segmentation")
