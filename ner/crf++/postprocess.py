#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from icwb import ICWBData


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e',
        '--estimate',
        type=str,
        required=True,
        help='The estimated test data, in crf++ format')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=True,
        help='Estimated data in ICWB required format')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    ICWBData.format_est(args.estimate, args.output)
