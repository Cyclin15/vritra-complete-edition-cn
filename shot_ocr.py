# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
im = Image.open('game_shot.png').convert('RGB')
for tag, arr in [('raw', np.array(im)),
                 ('boost', np.clip((np.array(im).astype(int)-30)*2.0, 0, 255).astype(np.uint8))]:
    res, _ = ocr(arr)
    print(f'-- {tag} --')
    if res:
        for b, txt, s in res:
            xs=[int(p[0]) for p in b]; ys=[int(p[1]) for p in b]
            print(f'{txt!r} ({float(s):.2f}) x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}')
    else:
        print('(none)')
