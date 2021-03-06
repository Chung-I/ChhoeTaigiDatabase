import argparse

from tsm.util import 判斷變調, 執行變調
from tsm.lexicon import Lexicon, LexiconEntry
from 臺灣言語工具.基本物件.句 import 句
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤 
from 臺灣言語工具.語音合成.閩南語音韻.變調 import 規則變調

parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('output_path')
parser.add_argument('--include-non-boundary', action='store_true')
parser.add_argument('--include-prefix', action='store_true')
parser.add_argument('--no-new-entry', action='store_true',
                    help="when including prefixes, only include prefixes that"
                         "itself is already an entry in the original lexicon.")
args = parser.parse_args()

lexicon = Lexicon.from_kaldi(args.input_path, with_prob=True)
new_lexicon_entries = []

def maybe_parse(hanji, lomaji):
    try:
        return 拆文分析器.建立句物件(hanji, lomaji) 
    except 解析錯誤:
        return None

def run_tone_sandhi(句物件):
    try:
        結果句物件, 判斷陣列 = 判斷變調(句物件)
        return 執行變調(結果句物件, 句物件, 判斷陣列)
    except 解析錯誤:
        return None

def get_syls(form):
    if isinstance(form, 句):
        syls = [字.看音() for 字 in form.篩出字物件()]
    else:
        syls = entry.phonemes.split()
    return syls

for grapheme in lexicon:
    entries = lexicon[grapheme]
    for entry in entries:
        citation_form = maybe_parse(grapheme, entry.phonemes) 
        if citation_form is None:
            continue
        citation_pron = get_syls(citation_form)
        sandhi_form = run_tone_sandhi(citation_form)
        if sandhi_form is None:
            continue
        sandhi_pron = get_syls(sandhi_form)

        if len(citation_pron) != len(sandhi_pron):
            print(f"number of syllables in citation and sandhi form of {grapheme}" +
                  "don't match; skipping")
        for citation_syl, sandhi_syl in zip(citation_pron, sandhi_pron):
            new_bnd_entry = LexiconEntry(citation_syl, entry.prob, sandhi_syl)
            new_lexicon_entries.append(new_bnd_entry)

new_lexicon = Lexicon(new_lexicon_entries, sum_dup_pron_probs=False)
new_lexicon.write(args.output_path)
