# -*- coding: utf-8 -*-
import os
from PIL import Image
from view import view
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
for f, box in [('howtoimg_mugen_en.png', (1000, 20, 1280, 130)),
               ('howtoimg_setsuna_en.png', (930, 20, 1280, 130))]:
    im = Image.open(os.path.join(UI, f)).convert('RGB')
    im.crop(box).save('_crop.png')
    print(f'== {f} {box}')
    view('_crop.png', 140)
    print()
