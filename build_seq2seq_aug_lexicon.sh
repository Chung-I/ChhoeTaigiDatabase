#python3 translate.py lexicons/moses.lexiconp.txt lexicons/dict_lexiconp.txt ../moedict-data-twblg/uni/詞目總檔.csv oov.txt lexicons/oov_seq2seqg2p_lexicon.txt --form sent --with-prob --mosesserver-port 8081 --model-types seq2seq char --oov-path lexicons/seq2seq_oov.txt
cat lexicons/dict_lexiconp.txt lexicons/oov_seq2seqg2p_lexicon.txt | sort -k1,1 -k2,2nr > lexicons/raw_seq2seq_aug_lexiconp.txt
python3 merge_duplicated_prons.py lexicons/raw_seq2seq_aug_lexiconp.txt lexicons/seq2seq_aug_lexiconp.txt --no-sum-probs
python3 syl2phone.py lexicons/seq2seq_aug_lexiconp.txt syl2phone.txt lexicons/seq2seq_aug_phn_lexiconp.txt --col 2
