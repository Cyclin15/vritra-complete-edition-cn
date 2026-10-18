# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
ocr = RapidOCR()

def check(fname, scale=3):
    im = Image.open(os.path.join(UI, fname)).convert('RGBA')
    w, h = im.size
    big = Image.new('RGBA', (w*scale, h*scale), (16, 24, 40, 255))
    big.alpha_composite(im.resize((w*scale, h*scale), Image.LANCZOS))
    res, _ = ocr(np.array(big.convert('RGB')))
    out = []
    if res:
        for box, txt, score in res:
            xs = [int(p[0]/scale) for p in box]; ys = [int(p[1]/scale) for p in box]
            out.append(f'{txt}({score})@x{min(xs)}-{max(xs)},y{min(ys)}-{max(ys)}')
    print(f'{fname}: ' + (' | '.join(out) if out else '(none)'))

for f in ['ranking_tab.png', 'replaylist_tab.png', 'practice_tab.png',
          'weponset_btn_a_off.png', 'weponset_btn_a_on.png',
          'weponset_btn_b_off.png', 'weponset_btn_b_on.png',
          'config_controller.png']:
    check(f)
