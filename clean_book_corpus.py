import os.path
import codecs
import multiprocessing
import nltk
import sys
import itertools
import re
import time
start=time.time()
sys.path.append('/apollo/env/HoverboardMLLibs/lib/python'+str(sys.version[:3])+'/site-packages')
def newlinebefore(f,n):
    f.seek(n)
    c=f.read(1)
    while c!=b'\n' and n > 0:
        n-=1
        f.seek(n)
        c=f.read(1)
    f.seek(n)
    return n
filename='output.txt'  #your filename goes here.
fsize=os.path.getsize(filename) #size of file (in bytes)
 
nchunks=20
initial_chunks=range(0,fsize,fsize//nchunks)
 
with open(filename,'rb') as f:
    start_byte=sorted(set([newlinebefore(f,i) for i in initial_chunks]))
 
end_byte=[i-1 for i in start_byte][1:] + [None]
def process_piece(filename,start,end):
    newlines = []
    with open(filename,'rb') as f:
        f.seek(start)
        if end is None:
            text=f.read().decode("utf8")
        else:
            nbytes=end-start+1
            text=f.read(nbytes).decode("utf8")
        lines = text.split("\n")
    for line in lines:
        del_pattern = re.compile(r'''(?x)
                                \([^\(\)]*\)             #anything in()
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
                                |:+
                                |,+
                                |^'.*
                                |\.+
                                |\?
                                |!+
                                |–+
                                |\++
                                |•+
                                |”+
                                |“+
                                |"+
                                |_+
                                |@+
                                |&+
                                |`+
                                |\*+
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
                                ''')
        line = re.sub(del_pattern, "", line)
        line = re.sub(r"‘|’", "'", line)
        line = re.sub(post_tok_del, "", line)
        line = re.sub(r"/|…|->|=|-(-)+", " ", line)
        line = line + "\n"
        newlines.append(line)
    return newlines
 
def wrapper(args):
    return process_piece(*args)
 
filename_repeated=[filename]*len(start_byte)
args=zip(filename_repeated,start_byte,end_byte)
 
pool=multiprocessing.Pool(20)
result=pool.map(wrapper,args)
result = list(itertools.chain.from_iterable(result))
with open("new.txt", "w") as fout:
    fout.writelines(result)
end = time.time()
total_time = end - start
h, res = divmod(total_time, 3600)
m, s = divmod(res, 60)
print("In total using time %d h %d m %d s"% (h, m, s))
