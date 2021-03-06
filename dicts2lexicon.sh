#python3 local/util.py syl2phone.txt
python3 dicts2lexicon.py \
  --dictionary-grapheme-phoneme-mapping taihoasuannteng_graph_phn_mapping.csv \
  --output-lexicon-path $1 \
  --with-tone
  #--output-lexicon-path lexicons/dict_lexicon.txt \
#  --syllable-phoneme-mapping-file syl2phone.txt \

