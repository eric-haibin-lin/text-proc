from multiprocessing import Pool
import argparse
import glob
import os
import io
import time
import logging
import collections
import tokenizer as tokenization

parser = argparse.ArgumentParser(description='BERT tokenizer')
parser.add_argument('--input_files', type=str, default='*.txt',
                    help='Input files. Default is "*.txt"')
parser.add_argument('--nworker', type=int, default=8,
                    help='Number of workers for parallel processing.')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.input_files)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.debug("Number of input files to process = %d"%(num_files))

hashes = collections.defaultdict(list)

def get_hash(filename):
    import hashlib
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1048576)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()

def compare(fa, fb):
    with open(fa, 'rb') as fain:
        with open(fb, 'rb') as fbin:
            if fain.read() != fbin.read():
                return False
    return True

def f1(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        assert input_file.endswith('.txt'), 'Expects .txt suffix for input files'
        h = get_hash(input_file)
    return h, input_file

def f2(files):
    if len(files) < 2:
        return
    for i in range(len(files)):
        for j in range(i, len(files)):
            if compare(files[i], files[j]):
                logging.info('%s %s', files[i], files[j])

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    results = p.map(f1, input_files)
    for h, input_file in results:
        hashes[h].append(input_file)
    toc = time.time()
    logging.debug("Processed %s in %.2f sec"%(args.input_files, toc-tic))
    logging.debug('number of unique files = %d', len(hashes))
    tic = time.time()
    p.map(f2, hashes.values())
    toc = time.time()
    logging.debug("Deduplicated %s in %.2f sec"%(args.input_files, toc-tic))
