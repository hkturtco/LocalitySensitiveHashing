#!/usr/bin/env python3
import sys


prev_band_id = None

gpid = 0
commentgp = []

for line in sys.stdin:
    cur_bandID, comment = line.strip().split('\t', 1)

    if prev_band_id is None:
        prev_band_id = cur_bandID

    if prev_band_id == cur_bandID:
        commentgp.append(comment)
    else:
        print(gpid, commentgp)
        commentgp = [comment]
        gpid += 1

    prev_band_id = cur_bandID

if prev_band_id == cur_bandID:
    print(gpid, commentgp)
