import argparse
from pathlib import Path
from tsm.util import parse_args_and_preprocess

def get_paths(data_dir: Path):
    paths = []
    for json_path in data_dir.rglob("*.json"):
        paths.append(json_path)

    return paths

def get_tuple_from_path(json_file):
    import json

    with open(json_file) as fp:
        raw_sent = json.load(fp)

    return (raw_sent['漢羅台文'], raw_sent['台羅數字調'])

if __name__ == '__main__':
    help_str = 'the root directory of TAT(Taiwanese Across Taiwan) Corpus'
    langs = ['漢羅台文', '台羅數字調', '白話字'] 
    metadata_fields = []
    parse_args_and_preprocess(get_paths, get_tuple_from_path, help_str)
