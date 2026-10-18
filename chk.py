# -*- coding: utf-8 -*-
import os
from PIL import Image
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
for f, box in [('ranking_tab.png', (36, 28, 101, 62)), ('replaylist_tab.png', (21, 34, 86, 66))]:
    im = Image.open(os.path.join(UI, f)).convert('RGBA')
    px = im.load()
    cnt = Counter()
    for y in range(box[1], box[3]+1):
        for x in range(box[0], box[2]+1):
            cnt[px[x, y]] += 1
    print(f, box, ':')
    for c, n in cnt.most_common(8):
        print('   ', c, 'x', n)
    # bright pixels bbox
    xs, ys = [], []
    for y in range(box[1], box[3]+1):
        for x in range(box[0], box[2]+1):
            r, g, b, a = px[x, y]
            if a > 150 and r > 180 and g > 180 and b > 180:
                xs.append(x); ys.append(y)
    if xs:
        print('    bright bbox', min(xs), min(ys), max(xs), max(ys), 'h=', max(ys)-min(ys)+1)
