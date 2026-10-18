# -*- coding: utf-8 -*-
import os
from PIL import Image
from view import view
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
im = Image.open(os.path.join(UI, 'howtoimg_mugen_en.png')).convert('RGB')
im.crop((330, 334, 560, 372)).save('_crop.png')
view('_crop.png', 150)
