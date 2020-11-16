python3 local/util.py syl2phone.txt
python3 local/dicts2lexicon.py \
  --dictionary-grapheme-phoneme-mapping dictionary_graph_phn_mapping.csv \
  --output-lexicon-path lexicon.txt \
  --syllable-phoneme-mapping-file syl2phone.txt \
  --with-tone

