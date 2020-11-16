from itertools import product
from symbols import 臺灣閩南語羅馬字拼音聲母表
from symbols import 臺灣閩南語羅馬字拼音韻母表

iNULL = "iNULL"  # dummy symbol if no initial
entering_tones = [4, 8]
TONES = list(range(1, 9))
entering_tone_suffix = "h"
is_phn = lambda final, tone: tone == "" or not (final.endswith(entering_tone_suffix) and tone not in entering_tones)
def generate_tsm_lexicon(lexicon_path: str,
                         grapheme_with_tone: bool = False,
                         phoneme_with_tone: bool = False):
    r"""Generate `lexicon.txt` through cartesian product of initials and finals.

    Arguments:
    lexicon_path (str): the path to write lexicon to.
    grapheme_with_tone (bool): set to True if grapheme needs tone.
    phoneme_with_tone (bool): set to True if phoneme needs tone.

    Returns:
        None
    """
    def generate_g2p_pair(initial, final, graph_tone, phn_tone):
        grapheme = f"{initial}{final}{graph_tone}"
        if initial:
            phoneme = f"{initial} {final}{phn_tone}"
        else:
            phoneme = f"{iNULL} {final}{phn_tone}"
        return grapheme, phoneme

    fp = open(lexicon_path, 'w')
    tones = TONES if grapheme_with_tone else [""]
    phonemes = product(臺灣閩南語羅馬字拼音聲母表,
                       臺灣閩南語羅馬字拼音韻母表,
                       tones)
    phonemes = filter(lambda triple: is_phn(triple[1], triple[2]),
                      phonemes)
    g2p_pairs = [generate_g2p_pair(initial, final, tone, tone if phoneme_with_tone else "")
                 for initial, final, tone in phonemes]

    for grapheme, phoneme in g2p_pairs:
        fp.write(f"{grapheme} {phoneme}\n")
    fp.close()

def generate_initials(initial_path):
    initials = list(map(lambda ini: ini if ini else iNULL, 臺灣閩南語羅馬字拼音聲母表))
    with open(initial_path, 'w') as fp:
        for initial in initials:
            fp.write(f"{initial}\n")

def generate_finals(final_path, phoneme_with_tone):
    finals = []
    tones = TONES if phoneme_with_tone else [""]
    finals = [(final, tone) for final, tone in product(臺灣閩南語羅馬字拼音韻母表, tones)
              if is_phn(final, tone)]
    with open(final_path, 'w') as fp:
        for final, tone in finals:
            fp.write(f"{final}{tone}\n")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('lexicon_path', type=str, help="")
    parser.add_argument('--grapheme-with-tone', action='store_true')
    parser.add_argument('--phoneme-with-tone', action='store_true')
    parser.add_argument('--initial-path', type=str)
    parser.add_argument('--final-path', type=str)
    args = parser.parse_args()
    generate_tsm_lexicon(args.lexicon_path, args.grapheme_with_tone, args.phoneme_with_tone)
    if args.initial_path:
        generate_initials(args.initial_path)
    if args.final_path:
        generate_finals(args.final_path, args.phoneme_with_tone)
