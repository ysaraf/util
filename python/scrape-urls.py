#!/usr/bin/python

import os, argparse, fileinput
import urllib, hashlib

parser = argparse.ArgumentParser(description='Scrape a set of URLs from an input file. Also appends to a file called "url_map.txt" in output directory that maps output file to url.')
parser.add_argument('-f', action="store", dest="inputFile", required=True, help="Input file")
parser.add_argument('-o', action="store", dest="outputDir", required=True, help="Output directory")
parser.add_argument('-c', action="store", dest="columnIndex", type=int, default=0, help="Column number containing URLs (default 0)")
parser.add_argument('-n', action="store", dest="numUrls", type=int, default=0, help="Number of urls to download from file (default is all)")
args = parser.parse_args()

URL_MAP_FILE = 'url_map.txt'

def main():
  urlHashMap = {}
  urlMapFile = '{0}/{1}'.format(args.outputDir, URL_MAP_FILE) 
  if not os.path.exists(args.outputDir):
    os.makedirs(args.outputDir)
  if os.path.exists(urlMapFile):
    with open(urlMapFile, 'r') as f:
      for line in f:
        parts = line.rstrip().split('\t')
        if len(parts) != 2:
          print "Invalid line in url map file: {0}".format(line)
          continue
        urlHashMap[parts[0]] = parts[1]
      
  urlsScraped = 0

  for line in fileinput.input(args.inputFile, mode='r'):
    if args.numUrls > 0 and fileinput.filelineno() >= args.numUrls:
      break
    parts = line.rstrip().split('\t')
    if len(parts) < args.columnIndex:
      print "Invalid line, column index beyond total number of columns: line no {0}: {1}".format(fileinput.filelineno(), line)
      continue
    url = parts[args.columnIndex]
    if len(url) == 0:
      print "Empty URL: line no {0}: {1}".format(fileinput.filelineno(), line)
      continue
    print "Downloading {0} at line {1}".format(url, fileinput.filelineno())
    urlHash = hashlib.sha1(url).hexdigest()
    if urlHash not in urlHashMap:
      urlHashMap[urlHash] = url
    outFilepath = "{0}/{1}.html".format(args.outputDir, urlHash)
    if os.path.exists(outFilepath):
      print "File already exists for {0}: {1}".format(url, outFilepath)
      continue
    try:
      page = urllib.urlopen(url).read()
    except IOError as e:
      print "Unable to download URL: {0}, exception: {1}".format(url, e)
      continue
    with open(outFilepath, 'w') as outFile:
      outFile.write(page)
      urlsScraped += 1
 
  print "Downloaded {0} URLs".format(urlsScraped)
  
  with open(urlMapFile, 'w') as f:
    [ f.write("{0}\t{1}\n".format(urlHash, url)) for urlHash, url in urlHashMap.iteritems() ]
  
if __name__ == '__main__':
  main()

