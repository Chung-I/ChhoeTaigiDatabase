python3 collect_syllable_tone_sandhi_examples.py lexicons/hanlo_taibun_lexiconp.txt lexicons/hanlo_only_ts_lexiconp.txt --include-prefix --include-non-boundary
python3 syl2phone.py lexicons/hanlo_only_ts_lexiconp.txt syl2phone.txt lexicons/hanlo_only_ts_phn_lexiconp.txt --col 2
cp lexicons/hanlo_only_ts_phn_lexiconp.txt /home/nlpmaster/ssd-1t/Taiwanese-Speech-Recognition-Recipe/ntut-tat-baseline/s5-basephn-ts/language/lexiconp.txt
