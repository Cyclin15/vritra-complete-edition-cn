# -*- coding: utf-8 -*-
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
def run(fname, regions):
    im = Image.open(os.path.join(UI, fname)).convert('RGBA')
    for (x0,y0,x1,y1) in regions:
        crop = im.crop((x0,y0,x1,y1))
        w,h = crop.size
        big = Image.new('RGBA', (w*3, h*3), (16,24,40,255))
        crop = crop.resize((w*3,h*3), Image.LANCZOS)
        big.alpha_composite(crop)
        import numpy as _np; res, _ = ocr(_np.array(big.convert("RGB")))
        print(f'{fname} region {x0,y0,x1,y1}:')
        if res:
            for box, txt, score in res:
                bx = [int((p[0]/3)+x0) for p in box[:2]] + [int((p[0]/3)+x0) for p in box[2:]]
                by = [int((p[1]/3)+y0) for p in box[:1]] + [int((p[1]/3)+y0) for p in box[1:]]
                xs = [int(p[0]/3+x0) for p in box]; ys = [int(p[1]/3+y0) for p in box]
                print(f'   {txt!r} score={score} x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}')
        else:
            print('   (none)')
run('practice_tab.png', [(0,0,123,60),(0,65,123,120),(0,130,123,185),(0,195,123,250),(0,260,123,325)])
