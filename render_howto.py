# -*- coding: utf-8 -*-
"""Translate the two howto explainer images (1280x720, text over screenshots):
erase English via cv2.inpaint (mask = white text + black outline), draw
Chinese lines with zpix, white core + black outline, matching original size."""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, 'Resources', 'asset_ui')
BAK = os.path.join(ROOT, '_cn_work', 'ui_backup')
FONT = os.path.join(ROOT, 'Resources', 'MatryoshkaXS.ttf')

SIZE = 24          # glyph height px
PITCH = 35         # line pitch px

# (erase_box, first_line_topleft, [lines])
MUGEN = [
    ((565, 155, 1160, 268), (576, 164), [
        '因陀罗已经没有剩余生命。',
        '在无限模式中，看看你能生存多久，',
        '冲击最高分吧！',
    ]),
    ((395, 298, 1180, 376), (410, 306), [
        '关卡由随机构成的波次组成，每波约 15 秒，',
        '每 10 波会出现一次 Boss！',
    ]),
    ((583, 420, 1235, 600), (594, 429), [
        '拾取关卡中出现的必杀技（MEGACRUSH），',
        '可以恢复冲刺能量，',
        '并对画面中的所有敌人造成巨大伤害。',
        '不要一拿到就用——',
        '留到危急时刻再用吧！',
    ]),
]

SETSUNA = [
    ((640, 178, 1190, 215), (651, 185), [
        '刹那模式（Caravan）限时 150 秒！',
    ]),
    ((474, 252, 1230, 330), (485, 261), [
        '拾取宝石可以恢复冲刺能量。如果运用得当，',
        '冲刺能量几乎可以无限使用！',
    ]),
    ((668, 368, 1205, 478), (679, 376), [
        '受到攻击时，会获得必杀技（MEGACRUSH），',
        '可对画面中的所有敌人',
        '造成巨大伤害！',
    ]),
    ((449, 512, 1145, 592), (460, 521), [
        '还有其他丰富的奖励内容！',
        '迎接各项挑战，冲击最高分吧！',
    ]),
]


def erase(arr, box):
    x0, y0, x1, y1 = box
    region = arr[y0:y1, x0:x1]
    lum = region.mean(axis=2)
    white = (lum > 90).astype(np.uint8) * 255
    # black outline near white text
    near = cv2.dilate(white, np.ones((7, 7), np.uint8))
    outline = ((lum < 60) & (near > 0)).astype(np.uint8) * 255
    mask = cv2.bitwise_or(white, outline)
    region = cv2.inpaint(region, mask, 5, cv2.INPAINT_TELEA)
    arr[y0:y1, x0:x1] = region


def draw_lines(im, origin, lines):
    font = ImageFont.truetype(FONT, SIZE)
    m = Image.new('L', im.size, 0)
    d = ImageDraw.Draw(m)
    x, y = origin
    for line in lines:
        d.text((x, y), line, font=font, fill=255)
        y += PITCH
    ol = m.filter(ImageFilter.MaxFilter(3))

    def layer(mask, rgb):
        l = Image.new('RGBA', im.size, rgb + (0,))
        l.putalpha(mask)
        return l

    im.alpha_composite(layer(ol, (0, 0, 0)))
    im.alpha_composite(layer(m, (255, 255, 255)))


def process(fname, blocks):
    path = os.path.join(UI, fname)
    im = Image.open(path).convert('RGB')
    os.makedirs(BAK, exist_ok=True)
    bp = os.path.join(BAK, fname)
    if not os.path.exists(bp):
        im.save(bp)
    arr = np.array(im)
    for box, origin, lines in blocks:
        erase(arr, box)
    im = Image.fromarray(arr).convert('RGBA')
    for box, origin, lines in blocks:
        draw_lines(im, origin, lines)
    im.convert('RGB').save(path)
    print(f'{fname}: {len(blocks)} blocks done')


def main():
    process('howtoimg_mugen_en.png', MUGEN)
    process('howtoimg_setsuna_en.png', SETSUNA)


if __name__ == '__main__':
    main()
