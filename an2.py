# -*- coding: utf-8 -*-
import os
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
im = Image.open(os.path.join(UI, 'practice_tab.png')).convert('RGBA')
px = im.load()
for a, b in [(0,60),(65,120),(130,185),(195,250),(260,325)]:
    xs, ys = [], []
    for y in range(a, b):
        for x in range(15, 108):
            r,g,bb,al = px[x,y]
            if al > 200 and r > 230 and g > 230 and bb > 230:
                xs.append(x); ys.append(y)
    print(f'y{a}-{b}: white bbox x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)} h={max(ys)-min(ys)+1}')
