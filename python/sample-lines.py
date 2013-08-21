#!/usr/bin/python

import sys, argparse, fileinput
from random import random

parser = argparse.ArgumentParser(description='Generate a random sample of given size from an input file')
parser.add_argument('-f', action="store", dest="inputFile", required=True, help="Input file")
parser.add_argument('-o', action="store", dest="outputFile", required=True, help="Output file containing sampled lines")
parser.add_argument('-s', action="store", dest="sampleSize", type=int, required=True, help="Approx sample size needed")
args = parser.parse_args()

totalLines = 0
with open(args.inputFile, 'r') as f:
  for line in f:
    totalLines += 1

assert totalLines > 0

if args.sampleSize >= totalLines or args.sampleSize == 0:
  print "Error: unexpected sample size"
  sys.exit(1)

sampleProb = float(args.sampleSize)/float(totalLines)
selected = 0
with open(args.outputFile, 'w') as outFile:
  for line in fileinput.input(args.inputFile, mode='r'):
    if random() <= sampleProb:
      selected += 1
      outFile.write(line)
    
print "Randomly selected {0} lines".format(selected)
