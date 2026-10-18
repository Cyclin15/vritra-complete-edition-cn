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
    im = im.resize((im.width*2, im.height*2), Image.LANCZOS)
    res, _ = ocr(np.array(im))
    print(f'{f} {box}:')
    if res:
        for b, txt, s in res:
            xs = [int(p[0]/2)+box[0] for p in b]; ys = [int(p[1]/2)+box[1] for p in b]
            print(f'  {txt!r} x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}')
    else:
        print('  (none)')
reg('howtoimg_mugen_en.png', (300, 330, 1200, 375))
reg('howtoimg_mugen_en.png', (400, 155, 1200, 270))
reg('howtoimg_setsuna_en.png', (400, 175, 1200, 215))
reg('howtoimg_setsuna_en.png', (400, 250, 1240, 330))
reg('howtoimg_setsuna_en.png', (550, 365, 1240, 480))
reg('howtoimg_setsuna_en.png', (380, 510, 1200, 595))
