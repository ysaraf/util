#!/usr/bin/python

import argparse
from matplotlib import pyplot as plt
from datetime import date, timedelta

def drawPlot(vals, title, outfile):
  x = range(len(counts))
  #x = [date.today() - timedelta(days=i) for i in reversed(range(len(vals))) ]
  plt.plot(x, vals)
  plt.title(title)
  plt.xlabel("X coords")
  plt.ylabel("Values")
  if outfile == None:
    plt.show()
  else:
    plt.savefig(outfile)

def main():
  parser = argparse.ArgumentParser(description='Plot values from an input string')
  parser.add_argument('--vals', action="store", dest="values", required=True, help="CSV list of values to plot")
  parser.add_argument('--title', action="store", dest="title", required=True, help="Plot title")
  parser.add_argument('-o', action="store", dest="outfile", required=False, help="Output file to store plot in")
  args = parser.parse_args()

  vals = []
  for val in [int(x.strip()) for x in args.values.split(',') if x.strip() != '']:
    vals.append(val)
  
  drawPlot(vals, args.title, args.outfile)
  
if __name__ == '__main__':
  main()
