#!/usr/bin/env python3
import sys
from random import randrange
import json
from urllib.request import urlopen
import datetime

hashesNum = 10
bandNum = 5
randomnum1 = [randrange(3000) for _ in range(0, hashesNum)]
randomnum2 = [randrange(3000) for _ in range(0, hashesNum)]
word_ids = dict()

keywordlist = ''
keyword = list()
listtemp = list()

# Min-Hashing
def min_hash(a, b, sig):
    hashes = list()
    for x in list(sig):
        hashes.append(((a * x) + b) % len(word_ids))
    return min(hashes)

def minhashSign(sig):
    hashes = list()
    for a, b in list(zip(randomnum1, randomnum2)):
        hashes.append(min_hash(a, b, sig))
    return hashes

def banding(l, n):
    for i in range(0, len(l), n):
        yield frozenset(l[i:i + n])

for word, word_id in map(lambda x: x.split(), urlopen('https://s3-ap-southeast-1.amazonaws.com/turtco/keyword_uk.txt').readlines()):
    word_ids[word.decode()] = int(word_id.decode())
    keyword.append(word.decode())

for line in sys.stdin:
    
    jsoninfo = json.loads(line)
    comment = jsoninfo['body']
    time = jsoninfo['created_utc']
    time = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    comment = ' '.join(comment.split('\t'))
    comment = ' '.join(comment.split('\n'))
    comment = ' '.join(comment.split('\r'))

    comment1 = ' '.join(comment.split('.'))
    comment1 = ' '.join(comment1.split(','))
    words = comment1.strip().lower().split()
    words = list(set(words))

    signature = map(lambda x: word_ids.get(x), words)
    signature = filter(lambda x: x is not None, signature)
    T = list(signature)

    if len(T)> 1:
        del listtemp[:]
        listtemp.append('Keywordlist')
        for num in T:
            listtemp.append(''.join(keyword[num - 1]))

        min_hash_row = minhashSign(T)
        band = banding(min_hash_row, bandNum)

        for band_id, band in enumerate(band):
            print('%d%d\t>>%s%s[%s]' % (band_id, hash(band),listtemp, comment.encode('utf-8'),time))
