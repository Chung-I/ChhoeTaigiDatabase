import argparse
import pandas as pd
from collections import defaultdict
import re
import numpy as np
from POJ_TL import poj_tl

flatten = lambda l: [item for sublist in l for item in sublist]

def recursively_retrieve_string_in_parenthesis(string):
    substrings = []
    try:
        span = re.search(r'\((.*?)\)', string).span()
        substrings.append(string[span[0]+1:span[1]-1])
        substrings_left = recursively_retrieve_string_in_parenthesis(string[:span[0]] + string[span[1]:])
        substrings += substrings_left
    except AttributeError:
        substrings.append(string.strip())

    return substrings

class Dictionary:

    @staticmethod
    def from_file(dictionary_path, grapheme_key, phoneme_key):
        df = pd.read_csv(dictionary_path, dtype={grapheme_key: str, phoneme_key: str})
        df = df.replace(np.nan, "", regex=True)
        grapheme_phoneme_pairs = list(zip(df[grapheme_key], df[phoneme_key]))
        dictionary = defaultdict(set)
        for raw_graph, raw_pron in grapheme_phoneme_pairs: # prons = pronunciations
            raw_graph = re.sub("\(.*\)", "", raw_graph).strip() # get rid of comments in grapheme
            raw_pron = raw_pron.strip()
            if not raw_pron or not raw_graph:
                continue
            graphs = [graph.strip() for graph in re.split("、", raw_graph)]
            prons = re.split(r'\/', raw_pron) # some word has multiple pronunciations separated by '/'
            prons = flatten([recursively_retrieve_string_in_parenthesis(pron.strip()) for pron in prons])
            for graph in graphs:
                dictionary[graph].update(prons)
        return dictionary

    @staticmethod
    def merge_dictionaries(dictionaries):
        merged_dictionary = defaultdict(set)
        for dictionary in dictionaries:
            for graph, prons in dictionary.items():
                merged_dictionary[graph].update(prons)
        return merged_dictionary

    @staticmethod
    def write_to_lexicon(dictionary, syllable_phoneme_mapping, lexicon_path,
                         with_tone=False):
        def syl2phns(syl_tone):
            # parse syllable to syllable and tone
            try:
                tone = int(syl_tone[-1])
                syl = syl_tone[:-1]
            except ValueError:
                syl = syl_tone
                tone = 0

            syl.encode("ascii")
            phns = syllable_phoneme_mapping[syl.lower()]
            #except KeyError:
            #    try:
            #        syl.encode('ascii')
            #        raise KeyError
            #    except UnicodeEncodeError:
            #        tlt_syl = syl
            #        phns = syl2phns(poj_tl(tlt_syl).tlt_tls())

            if with_tone:
                final = phns[-1] + str(tone)
                phns = phns[:-1] + [final]
            return phns
            
        fp = open(lexicon_path, 'w')
        for graph, prons in dictionary.items():
            for pron in prons:
                syls = filter(lambda syl: syl, re.split('[\W\-]+', pron.strip()))
                try:
                    phns = flatten(map(syl2phns, syls))
                    fp.write(f"{graph} {' '.join(phns)}\n")
                except KeyError as e:
                    print(f"skipping pronunciation {pron} of {graph} since phone not in syl-phn-mapping: {e}")
                except UnicodeEncodeError:
                    continue
        fp.close()

    @staticmethod
    def parse_lexicon(lexicon_path):
        with open(lexicon_path) as fp:
            entries = fp.read().splitlines()
        graph_phns_mapping = {}
        for entry in entries:
            graph_phns = re.split("\W", entry)
            graph, phns = graph_phns[0], graph_phns[1:]
            graph_phns_mapping[graph] = phns
        return graph_phns_mapping
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dictionary-grapheme-phoneme-mapping')
    parser.add_argument('--output-lexicon-path')
    parser.add_argument('--syllable-phoneme-mapping-file')
    parser.add_argument('--with-tone', action='store_true')
    args = parser.parse_args()

    df = pd.read_csv(args.dictionary_grapheme_phoneme_mapping)
    dictionaries = [Dictionary.from_file(*triple)
                    for triple in list(zip(df["file"], df["grapheme"], df["phoneme"]))]
    merged_dict = Dictionary.merge_dictionaries(dictionaries)
    syl_phn_mapping = Dictionary.parse_lexicon(args.syllable_phoneme_mapping_file)
    Dictionary.write_to_lexicon(merged_dict, syl_phn_mapping, args.output_lexicon_path,
                                args.with_tone)
