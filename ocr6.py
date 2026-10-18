# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
ocr = RapidOCR()
for f in ['howtoimg_mugen_en.png', 'howtoimg_setsuna_en.png']:
    im = Image.open(os.path.join(UI, f)).convert('RGB').crop((700, 0, 1280, 140))
    res, _ = ocr(np.array(im))
    print(f, 'top-right:')
    if res:
        for b, txt, s in res:
            xs = [int(p[0])+700 for p in b]; ys = [int(p[1]) for p in b]
            print(f'  {txt!r} x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}')
    else:
        print('  (none)')
