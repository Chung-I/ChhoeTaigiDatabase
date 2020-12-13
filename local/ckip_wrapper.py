from typing import List
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

class CKIPWordSegWrapper:
    def __init__(self, root_dir):
        self.ws = WS(root_dir)

    def cut_some(self, sents: List[str]):
        cutted_sents = self.ws(sents)
        return cutted_sents

    def cut(self, sent: str):
        cutted_sent = self.ws([sent])[0]
        return cutted_sent
