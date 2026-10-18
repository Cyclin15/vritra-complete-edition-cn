# -*- coding: utf-8 -*-
import os
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')

def colruns(fname, thr, y0=0, y1=None, mode='alpha'):
    im = Image.open(os.path.join(UI, fname)).convert('RGBA')
    px = im.load()
    y1 = y1 or im.height - 1
    def ok(x, y):
        r, g, b, a = px[x, y]
        if mode == 'alpha':
            return a > thr
        # color-luminance contrast vs (16,24,40) assumed? use max channel
        return a > 40 and (r + g + b) > thr
    cols = [sum(1 for y in range(y0, y1 + 1) if ok(x, y)) for x in range(im.width)]
    runs, s = [], None
    for x, c in enumerate(cols):
        if c > 0 and s is None: s = x
        elif c == 0 and s is not None: runs.append((s, x - 1)); s = None
    if s is not None: runs.append((s, im.width - 1))
    # merge runs separated by <6px
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 6:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r) if False else r)
    print(f'{fname} thr={thr} y{y0}-{y1} mode={mode}: {merged}')
    return merged

colruns('ranking_tab.png', 200)
colruns('replaylist_tab.png', 200)
colruns('practice_tab.png', 200, 0, 60)   # tab1 region, opaque bg? check
colruns('practice_tab.png', 450, 0, 60, 'lum')
colruns('practice_tab.png', 450, 70, 115, 'lum')
colruns('practice_tab.png', 450, 140, 185, 'lum')
colruns('practice_tab.png', 450, 205, 250, 'lum')
colruns('practice_tab.png', 450, 275, 325, 'lum')
