# -*- coding: utf-8 -*-
import os, sys
from PIL import Image
from view import view
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
def cv(fname, box, w=None):
    p = os.path.join(UI, fname)
    im = Image.open(p).convert('RGBA')
    crop = im.crop(box)
    tmp = os.path.join(ROOT, '_crop.png')
    crop.save(tmp)
    print(f'== {fname} {box} ({crop.width}x{crop.height})')
    view(tmp, w or crop.width)
cv('ranking_tab.png', (30, 26, 110, 64))
cv('replaylist_tab.png', (16, 32, 96, 68))
cv('weponset_btn_a_off.png', (175, 15, 330, 70), 155)
