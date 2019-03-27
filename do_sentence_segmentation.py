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
parser.add_argument('--data', type=str, default='./*/*.compact',
                    help='Input files. Default is "./*/*.compact"')
parser.add_argument('--suffix', type=str, default='.stn',
                    help='Suffix for output files. Default is .stn')
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
    logging.info('Processing %s', input_file)
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        with io.open(input_file + args.suffix, 'w', encoding="utf-8") as fout:
            for line in fin:
                sents = sent_tokenize(line)
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
    logging.info('Processed %s in %.2f sec', args.data, toc-tic)
