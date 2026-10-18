# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
ocr = RapidOCR()
def reg(f, box):
    im = Image.open(os.path.join(UI, f)).convert('RGB').crop(box)
    res, _ = ocr(np.array(im))
    print(f'{f} {box}:')
    if res:
        for b, txt, s in res:
            xs = [int(p[0])+box[0] for p in b]; ys = [int(p[1])+box[1] for p in b]
            print(f'  {txt!r} x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}')
    else:
        print('  (none)')
reg('howtoimg_mugen_en.png', (330, 332, 1250, 374))
reg('howtoimg_mugen_en.png', (560, 424, 1250, 600))
reg('howtoimg_setsuna_en.png', (440, 515, 1200, 595))
