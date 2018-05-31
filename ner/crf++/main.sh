#! /bin/bash

DATASET=pku
DATADIR=data

TRAIN=${DATADIR}/${DATASET}_training.utf8
TEST=${DATADIR}/${DATASET}_test.utf8
GOLD=${DATADIR}/icwb2-data/gold/${DATASET}_test_gold.utf8
WORDS=${DATADIR}/icwb2-data/gold/${DATASET}_training_words.utf8

MODEL=${DATADIR}/${DATASET}.crf++.model
CRF_PREDICT=${DATADIR}/${DATASET}.crfpp.predict.utf8
PREDICT=${DATADIR}/${DATASET}.predict.utf8
SCORE=${DATADIR}/${DATASET}_score.txt

mkdir -p {$DATADIR}
python3 preprocess.py -d ${DATASET} -o ${DATADIR}

crf_learn -f 3 -c 1.5 template.txt ${DATADIR}/${DATASET}_training.utf8 $MODEL
crf_test -m ${MODEL} ${TEST} > ${CRF_PREDICT}
python3 postprocess.py -e ${CRF_PREDICT} -o ${PREDICT}
perl $DATADIR/icwb2-data/scripts/score ${WORDS} ${GOLD} ${PREDICT} > ${SCORE}
tail -n 14 ${SCORE}
