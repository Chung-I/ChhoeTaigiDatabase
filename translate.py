from typing import NamedTuple, List, Union
import re
import json
from collections.abc import Iterable
from itertools import product
from functools import partial, reduce
from operator import add
import time
import logging
import tqdm
import numpy as np

from local.util import read_file_to_lines, dict_seg, flatten, write_lines_to_file
from local.sentence import Sentence
from local.clients import MosesConfig, MosesClient, AllennlpClient, UnkTranslator
from local.lexicon import Lexicon, LexiconEntry
from local.ckip_wrapper import CKIPWordSegWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('message')

def dfs(tree):
    for el in tree:
        #if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
        if isinstance(el, list):
                yield from dfs(el)
        else:
            yield el

def maybe_process_unk_factory(translator):
    def maybe_process_unk(entry, is_unks, n_best=1):
        if not any(is_unks):
            return [entry]
        lattice = [translator.translate(char, n_best) if unk else [LexiconEntry(char, 0.0, syl)]
                   for unk, char, syl in zip(is_unks, entry.grapheme, entry.phonemes.split())]
        # dummy character for multiplying unk prob with original entry prob
        lattice.append([LexiconEntry("", entry.prob, "")])
        hyp_entries = sorted(map(lambda path: reduce(add, path), product(*lattice)), key=lambda e: -e.prob)[:n_best]
        return hyp_entries
    return maybe_process_unk
    
def get_all_possible_translations(possible_cuts, lexicon):
    return flatten([product(*[[entry.phonemes for entry in lexicon[word]] for word in cut]) for cut in possible_cuts])

def hyp_to_line(src_text, hyp):
    text = " ".join(hyp['text'])
    return f"{src_text} {hyp['prob']} {text}"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--word-seg-model-path', default="/home/nlpmaster/ssd-1t/weights/data")
    parser.add_argument('--with-prob', action='store_true')
    parser.add_argument('--n-best', type=int, default=3)
    parser.add_argument('--min-prob', type=float, default=0.1)
    parser.add_argument('prob_lexicon_path')
    parser.add_argument('dict_lexicon_path')
    parser.add_argument('moedict_path')
    parser.add_argument('src_path')
    parser.add_argument('dest_path')
    parser.add_argument('--oov-path')
    parser.add_argument('--mosesserver-port', default=8080)
    parser.add_argument('--model-types', nargs='+', default=['seq2seq', 'char'])
    parser.add_argument('--unk-consult-order', nargs='+', default=['prob', 'dict', 'bpmf', 'seq2seq'])
    parser.add_argument('--form', choices=['char', 'word', 'sent'])
    args = parser.parse_args()
    model_types = args.model_types

    prob_lexicon = Lexicon.from_kaldi(args.prob_lexicon_path, args.with_prob)
    dict_lexicon = Lexicon.from_kaldi(args.dict_lexicon_path, args.with_prob)
    taibun_lexicon = Lexicon.from_moedict(args.moedict_path)
    moses_config = MosesConfig(True, True, args.n_best)
    moses_client = MosesClient(port=args.mosesserver_port, config=moses_config)
    word_seg = None
    if "word" in model_types:
        word_seg = CKIPWordSegWrapper(args.word_seg_model_path)

    seq2seq_translator = None
    seq2seq_translator = AllennlpClient()
    unk_translator = UnkTranslator(prob_lexicon, dict_lexicon, taibun_lexicon, args.unk_consult_order, seq2seq_translator)
    maybe_process_unk = maybe_process_unk_factory(unk_translator)

    lines = read_file_to_lines(args.src_path)
    src_sents = [Sentence.from_line(line, remove_punct=True, form=args.form) for line in lines]
    outf = open(args.dest_path, 'w')

    oovs = []
    for src_sent in tqdm.tqdm(src_sents):
        if not src_sent:
            continue
        if "dict" in model_types:
            maybe_sents = dict_seg("".join(src_sent), prob_lexicon)
            tgt_hyps = get_all_possible_translations(maybe_sents, prob_lexicon)
            if not tgt_hyps:
                #fall back to char-based SMT if src_sent can't be segmented using lexicon
                model_types.append("char")

        all_entries = []
        if "seq2seq" in model_types:
            all_entries += seq2seq_translator.translate(src_sent)

        if "char" in model_types or "word" in model_types:
            if "word" in model_types:
                src_sent = word_seg.cut("".join(src_sent))
            tgt_hyps = moses_client.translate(src_sent)['nbest']
            entries, is_unks = zip(*[MosesClient.parse_hyp("".join(src_sent), hyp) for hyp in tgt_hyps])
            maybe_process_unk_nbest = partial(maybe_process_unk, n_best=max(args.n_best // len(entries), 1))
            no_unk_entries = flatten(map(maybe_process_unk_nbest, entries, is_unks))
            merged_entries = Lexicon.merge_duplicated_prons(no_unk_entries)
            all_entries += Lexicon.normalize_prob_of_prons(merged_entries)

        merged_entries = Lexicon.merge_duplicated_prons(all_entries)
        nbest_entries = sorted(merged_entries, key=lambda e: -e.prob)[:args.n_best]
        filtered_entries = list(filter(lambda e: e.prob >= np.log(args.min_prob) and e.grapheme.strip() and e.phonemes.strip(), nbest_entries))
        src_text = "".join(src_sent)
        hyp_texts = list(map(str, filtered_entries))
        if not hyp_texts:
            oovs.append("".join(src_sent))
            logger.warning(f"{src_sent} doesn't have any valid tranlations; skipping")

        for hyp_text in hyp_texts:
            outf.write(hyp_text + "\n")
        time.sleep(0.005)
    outf.close()

    if args.oov_path:
        write_lines_to_file(args.oov_path, oovs)
            

