# -*- coding: utf-8 -*-
import os
from PIL import Image
from view import view
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
im = Image.open(os.path.join(UI, 'howtoimg_mugen_en.png')).convert('RGB')
im.crop((560, 150, 1170, 275)).save('_crop.png')
view('_crop.png', 150)
print()
im.crop((380, 330, 1180, 375)).save('_crop.png')
view('_crop.png', 150)
