"""Script for sentence segmentation."""
import argparse
import glob
import os
import io
import time
import logging
import nltk

from nltk.tokenize import sent_tokenize
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='Sentence tokenizer for BERT documents.')
parser.add_argument('--input_files', type=str, default='wiki_*.txt',
                    help='Input files. Default is "wiki_*.txt"')
parser.add_argument('--nworker', type=int, default=8,
                    help='Number of workers for parallel processing.')
args = parser.parse_args()

# download package
nltk.download('punkt')

# arguments
input_files = sorted(glob.glob(os.path.expanduser(args.input_files)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info("Number of input files to process = %d"%(num_files))

def f(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        assert input_file.endswith('.txt'), 'Expects .txt suffix for input files'
        with io.open(input_file.replace('.txt', '.doc'), 'w', encoding="utf-8") as fout:
            documents = fin.read().split('\n\n')
            for document in documents:
                sents = sent_tokenize(document)
                for sent in sents:
                    sent_str = sent.strip()
                    if sent_str:
                        fout.write('%s\n'%sent_str)
                fout.write(u'\n')

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info("Processed %s in %.2f sec"%(args.input_files, toc-tic))
