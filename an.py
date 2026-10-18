# -*- coding: utf-8 -*-
import os
from PIL import Image
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')

im = Image.open(os.path.join(UI, 'practice_tab.png')).convert('RGBA')
px = im.load()
bands = [(18,43),(88,105),(154,171),(217,239),(287,302)]
for i,(a,b) in enumerate(bands):
    cnt = Counter()
    for y in range(max(0,a-4), min(im.height,b+5)):
        for x in range(15, 105):
            r,g,bb,al = px[x,y]
            if al > 200:
                cnt[(r,g,bb)] += 1
    print(f'tab{i+1} y{a}-{b}:', cnt.most_common(6))
    # bg sample left of text
    bgc = Counter()
    for y in range(a, b+1):
        for x in range(0, 15):
            r,g,bb,al = px[x,y]
            if al > 200:
                bgc[(r,g,bb,al)] += 1
    print('   bg left:', bgc.most_common(3))
