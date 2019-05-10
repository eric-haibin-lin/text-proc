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
parser.add_argument('--data', type=str, default='~/book-corpus-feb-stn/*/*.txt',
                    help='Input files. Default is "*.txt"')
parser.add_argument('--nworker', type=int, default=1,
                    help='Number of workers for parallel processing.')
parser.add_argument('--out_dir', type=str, default='~/book-corpus-large-gather/',
                    help='Output dir. Default is ~/book-corpus-large-gather/')
parser.add_argument('--suffix', type=str, default='doc',
                    help='Suffix for outputs')
parser.add_argument('--block-size', type=int, default=32,
                    help='Block size for each output (MB)')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.data)))
out_dir = os.path.expanduser(args.out_dir)
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info('Number of input files to process = %d', num_files)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def f1(x):
    file_split, worker_id = x
    count = 0
    out_file = None
    total_size = 0
    for in_path in file_split:
        in_file = io.open(in_path, 'r', encoding='utf-8-sig')
        curr_size = os.path.getsize(in_path)
        if args.block_size * 1024 * 1024 < total_size + curr_size:
            out_file.close()
            out_file = None
            count += 1
            total_size = 0
        if not out_file:
            out_path = os.path.join(out_dir, 'part-{}.{}'.format(str(count + 1000 * worker_id).zfill(4), args.suffix))
            out_file = io.open(out_path, 'w', encoding="utf-8")
        total_size += curr_size
        content = in_file.read()
        if content[-1] == content[-2] and content[-1] == '\n':
            content = content[:-1]
        out_file.write(content)

if __name__ == '__main__':
    p = Pool(num_workers)

    # calculate the number of splits
    file_splits = []
    split_size = (len(input_files) + num_workers - 1) // num_workers
    for i in range(num_workers - 1):
        file_splits.append((input_files[i*split_size:(i+1)*split_size], i))
    file_splits.append((input_files[(num_workers-1)*split_size:], num_workers - 1))

    tic = time.time()
    p.map(f1, file_splits)
    toc = time.time()
    logging.info('Processed %s in %.2f sec', args.data, toc-tic)
