from multiprocessing import Pool
import argparse
import glob
import os
import io
import time
import logging
import re

parser = argparse.ArgumentParser(description='BERT tokenizer')
parser.add_argument('--data', type=str, default='~/book-corpus-large/*.txt',
                    help='Input files. Default is "~/book-corpus-large/*.txt"')
parser.add_argument('--nworker', type=int, default=72,
                    help='Number of workers for parallel processing.')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.data)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info("Number of input files to process = %d"%(num_files))

# including anything in ()
del_pattern = re.compile(r'''(?x)
                        \([^\(\)]*\)
                        |<[^<>]*>.*
                        |\*\*\*
                        |\#\#\#
                        |^\w*\s*\w*[:\-–]+\s*
                        |(http:)*www.*com
                        |\d*(\-\d+)+
                        |.*©.*
                        |(?<=\s)'
                        |'(?=\s)
                        |(?<=\s)\-
                        |\-(?=\s)
                        ''')

post_tok_del = re.compile(r'''(?x)
                        ;
                        |^\d+$
                        |^'.*
                        |–+
                        |\++
                        |•+
                        |_+
                        |@+
                        |&+
                        |`+
                        |\*+
                        |\{\{\{1
                        |\[+
                        |\]+
                        |\{+
                        |\}+
                        |\(+
                        |\)+
                        |\$+
                        |\+
                        |>+
                        |<+
                        |=+
                        |\#+
                        |~+
                        |!\[\]
                        ''')

def f(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        with io.open(input_file.replace('.txt', '.txt.re'), 'w', encoding="utf-8") as fout:
            lines = fin.readlines()
            for line in lines:
                line = line.strip()
                line = re.sub(del_pattern, "", line)
                #line = re.sub(r"‘|’", "'", line)
                line = re.sub(post_tok_del, "", line)
                line = re.sub(r"/|…|->|=|-(-)+", " ", line)
                line = line + "\n"
                fout.write(line)

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info("Processed %s in %.2f sec"%(args.data, toc-tic))
