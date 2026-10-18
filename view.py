# -*- coding: utf-8 -*-
"""Render images as ASCII art (for reading text content without vision)."""
import sys
from PIL import Image

def view(path, maxw=160):
    im = Image.open(path)
    has_alpha = im.mode in ('RGBA', 'LA', 'PA') or (im.mode == 'P' and 'transparency' in im.info)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    w, h = im.size
    scale = maxw / w
    nw, nh = maxw, max(1, int(h * scale * 0.5))  # 0.5 for char aspect
    im2 = im.resize((nw, nh))
    px = im2.load()
    chars = ' .+#@'  # dark->bright? we'll map brightness
    out = []
    # find bbox of non-transparent content
    for y in range(nh):
        line = ''
        for x in range(nw):
            r, g, b, a = px[x, y]
            if a < 40:
                line += ' '
                continue
            # brightness on black
            lum = (r * 299 + g * 587 + b * 114) // 1000
            if lum < 40: line += '.'
            elif lum < 90: line += '+'
            elif lum < 160: line += '#'
            elif lum < 220: line += '%'
            else: line += '@'
        out.append(line)
    # trim blank lines
    while out and not out[0].strip(): out.pop(0)
    while out and not out[-1].strip(): out.pop()
    if out:
        x0 = min(l.find(next(c for c in l if c != ' ')) for l in out if l.strip())
        x1 = max(l.rstrip().__len__() for l in out)
        out = [l[x0:x1] for l in out]
    print(f'== {path} ({w}x{h})')
    for l in out:
        print(l)
    print()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        view(p)
