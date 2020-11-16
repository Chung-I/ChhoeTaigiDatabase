# ChhoeTaigi 找台語：台語字詞資料庫
## 把辭典轉成lexicon

### Usage
```
bash dicts2lexicon.sh
```
把辭典轉成lexicon的形式，也就是grapheme到phoneme的對應。

`local/util.py`會生成syllable到phoneme的mapping。不過現在的code嚴格來說並不是生成到phoneme的mapping，而是到initial+final的mapping。

`dictionary_graph_phn_mapping.csv`是每個database的grapheme與phoneme的field name。想要grapheme跟phoneme分別是那一欄，可以在這邊configure。

`local/dicts2lexicon.py`吃syllable到initial+final的mapping (`--syllable-phoneme-mapping-file`)與每個辭典grapheme與phoneme的mapping(`--dictionary-grapheme-phoneme-mapping`)，輸出grapheme到phoneme(實際上是initial+final)的mapping。

現在的`dictionary_graph_phn_mapping.csv`裡面寫的是中文到台語羅馬字的configuration。

如果想要台文到台語羅馬字的對應的話，可以把grapheme中的hoabun改成`hanlo_taibun`之類的（每個辭典的field name都不大一樣，可以自己看一下）。
