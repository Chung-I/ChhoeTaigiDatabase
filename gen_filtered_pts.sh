root_dir=/home/nlpmaster/ssd-1t/corpus/PTS_TW-train/text
find -L $root_dir -name  
python3 dict_seg.py --lexicon-path /home/nlpmaster/Works/tsm_corpus/moedict-data-twblg/uni/詞目總檔.csv --input-path $root_dir/G2019432/G20194320002.txt --output-path G20194320002.txt --filtered-output-path G20194320002-filtered.txt
