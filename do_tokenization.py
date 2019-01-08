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
parser.add_argument('--vocab_file', type=str, default='/home/ubuntu/.mxnet/models/book_corpus_wiki_en_uncased-c3e2bd00.vocab',
                    help='Input vocab locations. Default is /home/ubuntu/.mxnet/models/book_corpus_wiki_en_uncased-c3e2bd00.vocab')

args = parser.parse_args()
args = parser.parse_args()

input_files = sorted(glob.glob(os.path.expanduser(args.input_files)))
num_files = len(input_files)
num_workers = args.nworker
logging.basicConfig(level=logging.INFO)
logging.info("Number of input files to process = %d"%(num_files))

def f(input_file):
    with io.open(input_file, 'r', encoding="utf-8") as fin:
        assert input_file.endswith('.doc'), 'Expects .doc suffix for input files'
        with io.open(input_file.replace('.doc', '.tokens'), 'w', encoding="utf-8") as fout:
            vocab_obj = nlp.Vocab.from_json(open(args.vocab_file, 'rt').read())
            tokenizer = tokenization.FullTokenizer(
                vocab=vocab_obj, do_lower_case=True)
            while True:
                line = tokenization.convert_to_unicode(fin.readline())
                if not line:
                    break
                line = line.strip()
                # Empty lines are used as document delimiters
                if not line:
                    fout.write(u'\n')
                    continue
                tokens = tokenizer.tokenize(line)
                if tokens:
                    fout.write(u'%s\n'%(' '.join(tokens)))

if __name__ == '__main__':
    tic = time.time()
    p = Pool(num_workers)
    p.map(f, input_files)
    toc = time.time()
    logging.info("Processed %s in %.2f sec"%(args.input_files, toc-tic))
