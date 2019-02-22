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
parser.add_argument('--input_files', type=str, default='wiki_*.doc',
                    help='Input files. Default is "wiki_*.doc"')
parser.add_argument('--nworker', type=int, default=8,
                    help='Number of workers for parallel processing.')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.input_files)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info("Number of input files to process = %d"%(num_files))

# TODO(haibin) tokenize with vocab
exclude_patterns = [
  '< no ##in ##cl ##ude >\n'
]

def in_pattern(x):
    for pattern in exclude_patterns:
        if len(x) == len(pattern) and x == pattern:
            return True
    return False

def f(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        assert input_file.endswith('.tokens'), 'Expects .doc suffix for input files'
        with io.open(input_file.replace('.tokens', '.tks'), 'w', encoding="utf-8") as fout:
            new_doc = True
            with io.open(input_file, 'r', encoding="utf-8") as fin:
                lines = fin.readlines()
                for line in lines:
                    if new_doc:
                        new_doc = False
                    elif len(line) == 1 and line[0] == '\n':
                        new_doc = True
                        fout.write(u'\n')
                    elif in_pattern(line):
                        pass
                    else:
                        fout.write(line)

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info("Processed %s in %.2f sec"%(args.input_files, toc-tic))
