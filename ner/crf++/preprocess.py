#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from icwb import ICWBData


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
