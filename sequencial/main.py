import re
import time
import argparse
import collections
import unicodedata


def parseArgs():
  parser = argparse.ArgumentParser()
  egroup = parser.add_mutually_exclusive_group(required=True)
  egroup.add_argument('-C', '--counting-words', action='store_true',
                      help='outputs the total number of words in FILE')
  egroup.add_argument('-W', '--word-count', action='store_true',
                      help='outputs the occurrences of each word in FILE')
  parser.add_argument('-b', '--benchmark', action='store_true',
                      help='logs the execution time')
  parser.add_argument('FILE', help='input file', type=argparse.FileType('r'))
  return parser.parse_args()


def timing(func):
  def wrapper(*arg, **kw):
    ts = time.time()
    res = func(*arg, **kw)
    te = time.time()
    return (te - ts), res
  return wrapper


@timing
def countingWords(text):
  text = text.lower()
  text = text.decode('unicode-escape')
  text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')
  words = re.findall('\w+', str(text))
  return len(words)


@timing
def wordCount(text):
  text = text.lower()
  text = text.decode('unicode-escape')
  text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')
  words = re.findall('\w+', str(text))
  return collections.Counter(words)


if __name__ == '__main__':
  args = parseArgs()
  text = args.FILE.read()
  args.FILE.close()

  if args.counting_words:
    time_taken, res = countingWords(text)
    print('{} words'.format(res))

  if args.word_count:
    time_taken, res = wordCount(text)
    res = [[key, value] for key, value in res.items()]
    res.sort(key=lambda x: x[1], reverse=True)
    print('; '.join([e[0] + ', ' + str(e[1]) for e in res]))

  if args.benchmark:
    print('Time taken {:.2f}s'.format(time_taken))
