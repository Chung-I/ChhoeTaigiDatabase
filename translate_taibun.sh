~/Works/mosesdecoder/bin/mosesserver -f /home/nlpmaster/Works/tsm_corpus/taibun_to_tsm/mandarin2taibun_char_reorder_goodturing_gooating_numeral/model/moses.ini --server-port 8081
python3 translate.py lexicons/lexicon_taibun.txt lexicons/lexicon_taibun.txt ../moedict-data-twblg/uni/詞目總檔.csv $1 $2 --form sent --with-prob --mosesserver-port 8081 --model-types dict char --unk-consult-order prob dict, bpmf --oov-path $3