#python3 dicts2lexicon.py \
#  --dictionary-grapheme-phoneme-mapping dictionary_graph_phn_mapping_taibun_other.csv \
#  --output-lexicon-path lexicons/taibun_other_lexiconp.txt \
#  --with-tone
#python3 make_tailo_dict.py lexicons/tlt_tls_lexiconp.txt
#cat lexicons/taibun_other_lexiconp.txt lexicons/tlt_tls_lexiconp.txt > lexicons/raw_hanlo_taibun_other_lexiconp.txt
#python3 merge_duplicated_prons.py lexicons/raw_hanlo_taibun_other_lexiconp.txt lexicons/hanlo_taibun_other_lexiconp.txt --no-sum-probs
#python3 syl2phone.py lexicons/hanlo_taibun_other_lexiconp.txt syl2phone.txt lexicons/hanlo_taibun_other_phn_lexiconp.txt --col 2
#python3 apply_ts.py lexicons/hanlo_taibun_other_lexiconp.txt lexicons/hanlo_taibun_other_ts_prefix_lexiconp.txt --include-prefix --no-new-entry
python3 syl2phone.py lexicons/hanlo_taibun_other_ts_prefix_lexiconp.txt syl2phone.txt lexicons/hanlo_taibun_other_ts_prefix_phn_lexiconp.txt --col 2
#cp lexicons/hanlo_taibun_phn_lexiconp.txt ~/ssd-1t/Taiwanese-Speech-Recognition-Recipe/ntut-tat-baseline/s5-taibun-aug/language/taibun_other_lexiconp.txt
