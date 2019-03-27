"""sentence segmentation script for wikipedia."""
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
parser.add_argument('--data', type=str, default='./*/wiki_*.txt',
                    help='Input files. Default is "./*/wiki_*.txt"')
parser.add_argument('--suffix', type=str, default='.doc',
                    help='Suffix of the produced output files. Default is .doc')
parser.add_argument('--nworker', type=int, default=72,
                    help='Number of workers for parallel processing.')
args = parser.parse_args()

# download package
nltk.download('punkt')

# arguments
input_files = sorted(glob.glob(os.path.expanduser(args.data)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info('Number of input files to process = %d', num_files)

def f(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        assert input_file.endswith('.txt'), 'Expects .txt suffix for input files'
        output = input_file + args.suffix
        with io.open(output, 'w', encoding="utf-8") as fout:
            documents = fin.read().split('\n\n')
            for document in documents:
                if not document:
                    continue
                try:
                    title_pos = document.index('\n')
                except ValueError:
                    logging.info('Warning: ValueError at for document: %s', document)
                    continue
                document = document[title_pos:]
                sents = sent_tokenize(document)
                for sent in sents:
                    sent_str = sent.strip()
                    if sent_str:
                        fout.write('%s\n'%sent_str)
                fout.write(u'\n')
        logging.info('Done with %s, saved in %s', input_file, output)

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info('Processed %s in %.2f sec', args.data, toc-tic)
