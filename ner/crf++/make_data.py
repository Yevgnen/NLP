#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import itertools
import os
import re
import tarfile
import zipfile

import requests


def split(regexp, text):
    pieces = []
    while True:
        match = re.search(regexp, text)
        if not match:
            break
        pieces += [match.group(0)]
        text = text[match.end():]

    if text:
        pieces += [text]

    return pieces


def download(url, root):
    filename = os.path.basename(url)

    zpath = os.path.join(root, filename)
    if not os.path.isfile(zpath):
        if not os.path.exists(os.path.dirname(zpath)):
            os.makedirs(os.path.dirname(zpath))

        print('downloading {url}'.format(url=url))
        r = requests.get(url)
        with open(os.path.join(zpath), mode='wb') as f:
            f.write(r.content)

    ext = os.path.splitext(filename)[-1]
    if ext == '.zip':
        with zipfile.ZipFile(zpath) as zfile:
            zfile.extractall(root)
    elif ext in ['.gz', '.tgz']:
        with tarfile.open(zpath, 'r:gz') as tar:
            tar.extractall(root)


class ICWBData(object):

    url = 'http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip'

    def __init__(self, root):
        os.makedirs(root, exist_ok=True)
        self.root = root
        self.fetch()
        self.train_tpl = os.path.join(root, 'icwb2-data', 'training',
                                      '{}_training.utf8')
        self.test_tpl = os.path.join(root, 'icwb2-data', 'testing',
                                     '{}_test.utf8')

    def fetch(self):
        download(ICWBData.url, self.root)

    def tag_word(self, word):
        if len(word) == 1:
            return ['S']

        return ['B'] + ['M'] * (len(word) - 2) + ['E']

    def tag_sentence(self, sen):
        return list(
            itertools.chain(*[zip(w, self.tag_word(w)) for w in sen.split()]))

    def tag_line(self, line):
        re_sentences = re.compile(r'.*?[。？！]')
        sens = split(re_sentences, line)

        if not sens:
            sens = line

        return list(self.tag_sentence(s) for s in sens)

    def tag_file(self, infile, outfile):
        with open(infile) as f:
            with open(outfile, mode='w') as g:
                for line in f:
                    tagged_sens = self.tag_line(line.strip())
                    g.writelines('\n\n'.join(
                        '\n'.join(' '.join(l) for l in s) for s in tagged_sens))
                    g.writelines('\n\n')

    def make_dataset(self, key, outdir):
        os.makedirs(outdir, exist_ok=True)

        train_input = self.train_tpl.format(key)
        test_input = self.test_tpl.format(key)

        train_output = os.path.join(outdir, os.path.basename(train_input))
        test_output = os.path.join(outdir, os.path.basename(test_input))

        self.tag_file(train_input, train_output)
        self.tag_file(test_input, test_output)


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dataset',
        type=str,
        default='pku',
        help='Dataset (default: \'pku\')')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='data/',
        help='Output directory (default: \'data/\')')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    ICWBData(args.output).make_dataset(args.dataset, args.output)
