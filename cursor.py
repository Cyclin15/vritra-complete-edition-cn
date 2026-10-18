# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
a = np.array(Image.open('game_shot.png').convert('RGB')).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
orange = (r > 180) & (g > 30) & (g < 130) & (b < 60)
rows = np.where(orange.any(axis=1))[0]
if len(rows):
    bands, s, p = [], rows[0], rows[0]
    for y in rows[1:]:
        if y > p + 4:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for s2, p2 in bands:
        cols = np.where(orange[s2:p2+1].any(axis=0))[0]
        print(f'orange y{s2}-{p2} x{cols.min()}-{cols.max()} n={int(orange[s2:p2+1].sum())}')
else:
    print('no orange')
