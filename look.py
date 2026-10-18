# -*- coding: utf-8 -*-
import os, sys
from PIL import Image
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))
BAK = os.path.join(ROOT, 'ui_backup')

def region_colors(fname, box, label):
    im = Image.open(os.path.join(BAK, fname)).convert('RGBA')
    px = im.load()
    cnt = Counter()
    for y in range(box[1], box[3]+1):
        for x in range(box[0], box[2]+1):
            cnt[px[x,y]] += 1
    print(f'{fname} {label} {box}:')
    for c, n in cnt.most_common(8):
        print(f'   {c} x{n}')

region_colors('weponset_btn_a_off.png', (180, 18, 325, 66), 'header Type-A')
region_colors('weponset_btn_a_on.png', (180, 18, 325, 66), 'header Type-A on')
region_colors('weponset_btn_a_off.png', (58, 128, 112, 155), 'name BLUE off')
region_colors('weponset_btn_a_on.png', (58, 128, 112, 155), 'name BLUE on')
region_colors('practice_tab.png', (18, 283, 106, 307), 'tab5 STAGE-5')
