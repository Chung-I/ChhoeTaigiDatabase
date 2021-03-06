from tsm.POJ_TL import poj_tl
from tsm.symbols import all_syls

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dest_path')
    args = parser.parse_args()
    tlt_tls_map = dict(map(lambda w: (poj_tl(w).tls_tlt(), w), all_syls))
    with open(args.dest_path, 'w') as fp:
        for tlt, tls in tlt_tls_map.items():
            fp.write(f"{tlt} 1.0 {tls}\n")
