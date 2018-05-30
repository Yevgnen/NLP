#! /bin/bash

DATASET=pku
DATADIR=data

mkdir -p {$DATADIR}
python3 ./make_data.py -d ${DATASET} -o ${DATADIR}
echo ${DATADIR}/${DATASET}_training.utf8
echo ${DATADIR}/$DATASET.crf++.model
crf_learn -f 3 -c 1.5 template.txt ${DATADIR}/${DATASET}_training.utf8 ${DATADIR}/$DATASET.crf++.model
