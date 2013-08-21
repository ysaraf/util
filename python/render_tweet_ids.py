#!/usr/bin/python

import os, argparse

parser = argparse.ArgumentParser(description='Render tweets from tweet ids.')
parser.add_argument('-f', action="store", dest="inputFile", required=True)
parser.add_argument('-o', action="store", dest="outputFile", required=True)
args = parser.parse_args()

def renderTweet(tweetId):
  return '''
<blockquote class="twitter-tweet" data-cards="hidden"><p><a href="https://twitter.com/dummy/status/{0}"></a></blockquote>
<script async src="http://platform.twitter.com/widgets.js" charset="utf-8"></script>'''.format(tweetId)

def main():
  with open(args.inputFile, mode='r') as infile, open(args.outputFile, mode='w') as outfile:
    outfile.write('<html><body><table border="1" width="100%">')
    for line in infile:
      tweetIds = line.rstrip().split('\t')
      outfile.write('<tr>')
      for tweetId in tweetIds:
        outfile.write('<td>' + renderTweet(tweetId) + '</td>')
      outfile.write('</tr>')
    outfile.write('</table></body></html>')
  
if __name__ == '__main__':
  main()

