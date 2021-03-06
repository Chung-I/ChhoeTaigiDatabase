#bash dicts2lexicon_taibun.sh lexicons/taibun_lexiconp.txt
#python3 make_tailo_dict.py lexicons/tlt_tls_lexiconp.txt
#cat lexicons/taibun_lexiconp.txt lexicons/tlt_tls_lexiconp.txt > lexicons/raw_hanlo_taibun_lexiconp.txt
#python3 merge_duplicated_prons.py lexicons/raw_hanlo_taibun_lexiconp.txt lexicons/hanlo_taibun_lexiconp.txt --no-sum-probs
python3 syl2phone.py lexicons/hanlo_taibun_lexiconp.txt syl2phone.txt lexicons/hanlo_taibun_phn_lexiconp.txt --col 2
cp lexicons/hanlo_taibun_phn_lexiconp.txt ~/ssd-1t/Taiwanese-Speech-Recognition-Recipe/ntut-tat-baseline/s5-taibun/language/lexiconp.txt
