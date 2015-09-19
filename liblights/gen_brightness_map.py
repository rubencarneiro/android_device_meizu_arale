#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import math
import functools

import six

OUTPUT_FILENAME = 'brightness_map_generated.h'
NUM_PER_ROW = 8
NUM_ROWS = 256 / NUM_PER_ROW

E_INV = math.e ** -1


def _log_curve(x):
    return ((math.log(E_INV + (math.e - E_INV) * x / 255.0)) + 1) / 2.0


def _exp_curve(x, k=1.0):
    return (math.exp(x / 256.0 * k) - 1) / (math.e ** k - 1)


def brightness_fn(x):
    return min(int(_log_curve(x) * 1280 + 768), 2047)


def output_header(fp):
    fp.write(b'/* generated by gen_brightness_map.py, do not modify */\n')
    fp.write(b'\n')
    fp.write(b'#ifndef _GENERATED_BRIGHTNESS_MAP_H_\n')
    fp.write(b'#define _GENERATED_BRIGHTNESS_MAP_H_\n')
    fp.write(b'\n')
    fp.write(b'static int BRIGHTNESS_MAP[256] = {\n')


def _do_output_row(fp, fn, num_per_row, idx):
    row_x_start = num_per_row * idx
    row_x_end = row_x_start + num_per_row

    row_y = [fn(x) for x in six.moves.range(row_x_start, row_x_end)]
    row_values = ', '.join('%4d' % y for y in row_y)
    row_str = '    %s,  /* %d - %d */\n' % (row_values, row_x_start, row_x_end - 1, )

    fp.write(row_str)


def output_tail(fp):
    fp.write(b'};\n')
    fp.write(b'\n')
    fp.write(b'#endif\n')


def main():
    with open(OUTPUT_FILENAME, 'wb') as fp:
        output_row = functools.partial(_do_output_row, fp, brightness_fn, NUM_PER_ROW)
        output_header(fp)

        for i in six.moves.range(NUM_ROWS):
            output_row(i)

        output_tail(fp)


if __name__ == '__main__':
    sys.exit(main())


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: