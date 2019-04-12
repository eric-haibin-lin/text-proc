"""sentence segmentation script for wikipedia."""
import argparse
import glob
import os
import io
import time
import logging

parser = argparse.ArgumentParser(description='Sentence tokenizer for BERT documents.')
parser.add_argument('--in_files', type=str, default='*.doc',
                    help='Input files suffix')
parser.add_argument('--out_dir', type=str, default='~/enwiki-feb-doc-split/',
                    help='Output dir. Default is "~/enwiki-feb-doc/"')
parser.add_argument('--block-size', type=int, default='13',
                    help='Output size (MB) for the dev/test file')
args = parser.parse_args()

COUNT = 6

# arguments
out_dir = os.path.expanduser(args.out_dir)
input_files = sorted(glob.glob(args.in_files))
num_files = len(input_files)
logging.basicConfig(level=logging.INFO)
logging.info('Number of input files to process = %d', num_files)

def f():
    dev = io.open(os.path.join(out_dir, os.path.basename(input_files[-1]) + '.dev'), 'w', encoding="utf-8")
    test = io.open(os.path.join(out_dir, os.path.basename(input_files[-1]) + '.test'), 'w', encoding="utf-8")
    for input_file in input_files:
        with io.open(input_file, 'r', encoding="utf-8") as fin:
            with io.open(os.path.join(out_dir, os.path.basename(input_file) + '.train'), 'w', encoding="utf-8") as fout:
                documents = fin.read().split('\n\n')
                num_dev = 0
                num_test = 0
                for document in documents:
                    if not document:
                        continue
                    if num_dev < COUNT:
                        dev.write('%s\n\n'%document)
                        num_dev += 1
                        continue
                    if num_test < COUNT:
                        test.write('%s\n\n'%document)
                        num_test += 1
                        continue
                    fout.write('%s\n\n'%document)
            logging.info('Done with %s', input_file)
    dev.write(u'\n')
    test.write(u'\n')

if __name__ == '__main__':
    tic = time.time()
    f()
    toc = time.time()
    logging.info('Processed %s in %.2f sec', args.out_dir, toc-tic)
