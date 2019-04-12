#!/usr/bin/env bash

corpus=${1}
if [[ ! -d "$corpus" ]]; then
	echo 'first argument should the path to book corpus';
	exit 1
fi
output=${corpus}-cleaned
nproc=8

find ${corpus}/ -type f ! -name '*.txt' -delete
if [[ -d "$output" ]]; then rm -Rf ${output}; fi
mkdir ${output}

find ${corpus}/*.txt -type f -print | xargs -P ${nproc} -n 72 -I{} \
    sh -c "
    path={};
    echo \$path;
    cat \$path \
    | sed 's/===\+//g' \
    | sed 's/----\+//g' \
    | sed 's/###\+//g' \
    | sed 's/\~\~\~\+//g' \
    | sed 's/\*\*\*\*\+//g' > \$path.clean"

find ${corpus}/*.clean -type f -print | xargs -P ${nproc} -n 72 -I{} \
    sh -c "
    echo {};
    cat -s {} \
    | sed '/^$/d' > {}.compact"

python3 do_sentence_segmentation.py --data $corpus'/*.compact'

python3 do_gather.py --data $corpus'/*.stn'  --nworker ${nproc} --out_dir $corpus

python3 split_wiki.py --in_files $corpus'/*.doc' --out_dir $output