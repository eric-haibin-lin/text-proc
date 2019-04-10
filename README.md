# text-proc
Script for Text Processing

## Wikipedia 
### Extract Contents
Retrieved on 20th Feb
```
git clone https://github.com/eric-haibin-lin/wikiextractor
cd wikiextractor; python setup.py install --user
WikiExtractor.py --processes $(nproc) -o enwiki -b 32M enwiki-latest-pages-articles.xml.bz2
```
### Cleanup
```
find . -type f -print | xargs -P $(nproc) -n 1 -I{} \
    sh -c "
    echo {};
    cat {} \
    | grep -v '^<doc [^>]*>$' \
    | grep -vE '\[\[Category:[^][]*\]\]' \
    | sed 's/\[\[\([^]|[]*\)\]\]/\1/g' \
    | sed 's/\[\[\([^]|[]*\)\]\]/\1/g' \
    | sed 's/\[\[[^]|[]*|\([^]|[]*\)\]\]/\1/g' \
    | sed 's/\[\[[^]|[]*|\([^]|[]*\)\]\]/\1/g' \
    | sed 's/\[\[[:]*[Ff]ile:[^][]*\]\]//g' \
    | sed 's/\[\[[Mm]edia:[^][]*\]\]//g' \
    | sed 's/\[\[[Ii]mage:[^][]*\]\]//g' \
    | sed 's/\[\([^]|[]*\)\]/\1/g' \
    | sed 's/\[\[\([^][]*\)\]\]//g' \
    | sed 's/alt=//g' \
    | sed 's/<\/doc>/\r/g' \
    | sed 's/<chem\([^<]*\)<\/chem>/\1/g' \
    | sed 's/<ins\([^<]*\)<\/ins>/\1/g' \
    | sed 's/<\, ref \([^<]*\)<\/ref>//g' \
    | sed 's/<includeonly\([^<]*\)<\/includeonly>//g' \
    | sed 's/<graph\([^<]*\)<\/graph>//g' \
    | sed 's/<section\([^\\]*\)\/>//g' \
    | sed 's/<meta\([^\\]*\)\/>//g' \
    | sed 's/<hr\([^\\]*\)\/>//g' \
    | sed 's/<gallery\([^>]*\)>//g' \
    | sed 's/<ref\([^<]*\)<\/ref>//g' \
    | sed 's/<ref\([^>]*\)>//g' \
    | sed 's/<http\([^>]*\)>//g' \
    | sed 's/<Ref\([^>]*\)>//g' \
    | sed 's/<mapframe \([^\/]*\)\/>//g' \
    | sed 's/<mapframe\([^>]*\)>//g' \
    | sed 's/<\/mapframe>//g' \
    | sed 's/<poem>//g' \
    | sed 's/<\/poem>//g' \
    | sed 's/<math>//g' \
    | sed 's/<\/math>//g' \
    | sed 's/<ref>//g' \
    | sed 's/<\/ref>//g' \
    | sed 's/<div\([^>]*\)>//g' \
    | sed 's/<\/div\([^>]*\)>//g' \
    | sed 's/<\/div style>//g' \
    | sed 's/<\/div>//g' \
    | sed 's/<sup>//g' \
    | sed 's/<\/sup>//g' \
    | sed 's/<br>//g' \
    | sed 's/<\/br>//g' \
    | sed 's/<BR>//g' \
    | sed 's/<\/BR>//g' \
    | sed 's/<Br>//g' \
    | sed 's/<\/Br>//g' \
    | sed 's/<del>//g' \
    | sed 's/<\/del>//g' \
    | sed 's/<nowiki>//g' \
    | sed 's/<\/nowiki>//g' \
    | sed 's/<NOWIKI>//g' \
    | sed 's/<\/NOWIKI>//g' \
    | sed 's/<onlyinclude>//g' \
    | sed 's/<\/onlyinclude>//g' \
    | sed 's/<includeonly>//g' \
    | sed 's/<\/includeonly>//g' \
    | sed 's/<small>//g' \
    | sed 's/<\/small>//g' \
    | sed 's/<chem>//g' \
    | sed 's/<\/chem>//g' \
    | sed 's/<noinclude>//g' \
    | sed 's/<\/noinclude>//g' \
    | sed 's/<gallery>//g' \
    | sed 's/<\/gallery>//g' \
    | sed 's/<graph>{//g' \
    | sed 's/<graph>//g' \
    | sed 's/}<\/graph>//g' \
    | sed 's/<\/graph>//g' \
    | sed 's/<\/references>//g' \
    | sed 's/<poem \([^>]*\)>//g' \
    | grep -v '^[ \t]*$' > {}.txt"
```
### Tokenization
```
python do_tokenization.py --data '~/enwiki-feb-doc/*/*.doc'
```

## Books Corpus

### regex cleanup (books corpus)
```
find . -type f -print | xargs -P $(nproc) -n 72 -I{} \
    sh -c "
    echo {};
    cat {} \
    | sed 's/===\+//g' \
    | sed 's/----\+//g' \
    | sed 's/###\+//g' \
    | sed 's/\~\~\~\+//g' \
    | sed 's/\*\*\*\*\+//g' > {}.clean"
```
### remove multiple newlines
```
find . -type f -print | xargs -P $(nproc) -n 72 -I{} \
    sh -c "
    echo {};
    cat -s {} \
    | sed '/^$/d' > {}.compact"
```
### sentence segmentation
```
python do_sentence_segmentation.py --data '/home/ubuntu/book-corpus-large-clean/*'
```
### Gather files to 32mb blocks
```
python do_gather.py --data '/home/ubuntu/book-corpus-feb-stn-clean/*/*'  --nworker
```
### Renaming files
```
for file in *
do
  mv "$file" "${file#prefix}"
done

for f in *.txt; do 
    mv -- "$f" "${f%.txt}.suffix"
done
```
### Split train dev set
```
python split_wiki.py
```

## Stats
#### book-corpus-feb-split-uncased
* Dataset size: 1.7G
* num sub-words:  380,207,517 (380.2 Million)

#### enwiki-feb-doc-split

* num words = 2,052,479,811 (2.1 Billion)

#### story-feb-split

* Dataset size: 32G
* Number of words:  7,353,924,749 (7.4 Billion)

#### book-corpus-large (raw)

* Dataset size: 5.3 GB
* Number of words: 992,511,482
