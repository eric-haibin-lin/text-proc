from multiprocessing import Pool
import argparse
import glob
import os
import io
import time
import logging
import gluonnlp as nlp
import tokenizer as tokenization

parser = argparse.ArgumentParser(description='BERT tokenizer')
parser.add_argument('--data', type=str, default='./*/*.doc',
                    help='Input files. Default is "./*/*.doc"')
parser.add_argument('--nworker', type=int, default=72,
                    help='Number of workers for parallel processing.')
parser.add_argument('--suffix', type=str, default='.tks',
                    help='Suffix for the output files. Default is ".tks"')
parser.add_argument('--dataset', type=str, default='book_corpus_wiki_en_uncased',
                    help='Dataset name. Options are book_corpus_wiki_en_uncased, '
                         'book_corpus_wiki_en_cased, wiki_multilingual_uncased, '
                         'wiki_multilingual_cased, wiki_cn_cased')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.data)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info('Number of input files to process = %d', num_files)

vocab = nlp.data.utils._load_pretrained_vocab('book_corpus_wiki_en_uncased', cls=nlp.vocab.BERTVocab)
tokenizer = nlp.data.BERTTokenizer(vocab)

def f(input_file):
    logging.info('Processing %s', input_file)
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        with io.open(input_file + args.suffix, 'w', encoding="utf-8") as fout:
            while True:
                line = fin.readline()
                if not line:
                    break
                line = line.strip()
                # Empty lines are used as document delimiters
                if not line:
                    fout.write(u'\n')
                    continue
                tokens = tokenizer(line)
                if tokens:
                    fout.write(u'%s\n'%(' '.join(tokens)))
    logging.info('Done processing %s, saved in %s', input_file, input_file + args.suffix)

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info('Processed %s in %.2f sec', args.data, toc-tic)
