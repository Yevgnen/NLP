#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        return itertools.chain(*[zip(w, self.tag_word(w)) for w in sen.split()])

    def tag_line(self, line):
        # NOTE: treat each line a single sentence
        return self.tag_sentence(line)

    def make_train(self, infile, outfile):
        with open(infile) as f:
            with open(outfile, mode='w') as g:
                for line in f:
                    tagged_line = self.tag_line(line.strip())
                    g.writelines('\n'.join(' '.join(l) for l in tagged_line))
                    g.writelines('\n\n')

    def make_test(self, infile, outfile):
        with open(infile) as f:
            with open(outfile, mode='w') as g:
                for line in f:
                    line = line.strip()
                    g.writelines('\n'.join(list(line)))
                    g.writelines('\n\n')

    def make_dataset(self, key, outdir):
        os.makedirs(outdir, exist_ok=True)

        train_in = self.train_tpl.format(key)
        train_out = os.path.join(outdir, os.path.basename(train_in))
        self.make_train(train_in, train_out)

        test_in = self.test_tpl.format(key)
        test_out = os.path.join(outdir, os.path.basename(test_in))
        self.make_test(test_in, test_out)

        return train_out, test_out

    @staticmethod
    def format_est(infile, outfile):
        with open(infile) as f:
            with open(outfile, mode='w') as g:
                sentence = []
                word = []
                for line in f:
                    line = line.strip().split()

                    if not line:
                        g.writelines(' '.join(sentence))
                        g.writelines('\n')
                        sentence = []
                        continue

                    char, tag = line[0], line[-1]
                    if tag == 'S':
                        sentence += [char]
                        continue

                    word += [char]
                    if tag == 'E':
                        sentence += [''.join(word)]
                        word = []
