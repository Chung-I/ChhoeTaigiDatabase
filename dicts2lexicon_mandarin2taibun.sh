#python3 make_lexicon.py syl2phone.txt
python3 dicts2lexicon.py \
  --dictionary-grapheme-phoneme-mapping dictionary_graph_phn_mapping_mandarin2taibun.csv \
  --output-lexicon-path $1 \
  --with-tone --write-raw

gzip $1/dict_mandarin.txt
gzip $1/dict_taibun.txt
