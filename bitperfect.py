#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile
import argparse

parser = argparse.ArgumentParser(description="Compare two WAV files for bit-perfect equality.")
parser.add_argument("source_file", help="Path to the source WAV file")
parser.add_argument("output_file", help="Path to the output WAV file")
args = parser.parse_args()

try:
    rate1, source = wavfile.read(args.source_file)
except Exception as e:
    print(f"Error reading source file: {e}")
    exit(e.errno)

try:
    rate2, output = wavfile.read(args.output_file)
except Exception as e:
    print(f"Error reading output file: {e}")
    exit(e.errno)

if rate1 != rate2:
    print("Sample rates differ")
    exit(1)

if source.size == 0:
    print(args.source_file + " is empty")
    exit(1)

if output.size == 0:
    print(args.output_file + " is empty")
    exit(1)

nz_source = source.nonzero()
nz_output = output.nonzero()

if nz_source[0].size == 0:
    print(args.source_file + " is completely silent")
    exit(1)
    
if nz_output[0].size == 0:
    print(args.output_file + " is completely silent")
    exit(1)

fnz_source = nz_source[0][0]
fnz_output = nz_output[0][0]

len = source.shape[0] - fnz_source 

equal = np.array_equal(source[fnz_source:fnz_source + len],output[fnz_output:fnz_output + len]);
if not equal:
    print("WAV files are not bit-perfect equal")
    exit(1)