# -*- coding: utf-8 -*-
"""In-place text replacement: inpaint old text via median filter, then render
Chinese text with the same style family as render_ui.py onto the tile."""
import os
from PIL import Image, ImageFilter

from render_ui import render, measure_core, PAD

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, 'Resources', 'asset_ui')
BAK = os.path.join(ROOT, '_cn_work', 'ui_backup')


def inpaint(im, box, win=13):
    x0, y0, x1, y1 = box
    pad = win
    cx0, cy0 = max(0, x0 - pad), max(0, y0 - pad)
    cx1, cy1 = min(im.width, x1 + pad + 1), min(im.height, y1 + pad + 1)
    crop = im.crop((cx0, cy0, cx1, cy1))
    im.paste(crop.filter(ImageFilter.MedianFilter(win)), (cx0, cy0))


def clamp_core(core, cap):
    if core and cap and (core[3] - core[1] + 1) > cap:
        cy = (core[1] + core[3]) // 2
        core = (core[0], cy - (cap - 1) // 2, core[2], cy + cap // 2)
    return core


def replace(fname, items):
    """items: (box, text, style, cap_h_or_None)"""
    path = os.path.join(UI, fname)
    im = Image.open(path).convert('RGBA')
    os.makedirs(BAK, exist_ok=True)
    bp = os.path.join(BAK, fname)
    if not os.path.exists(bp):
        Image.open(path).convert('RGBA').save(bp)
    for box, text, style, cap in items:
        pad = PAD[style] + 3
        tx0 = max(0, box[0] - pad); ty0 = max(0, box[1] - pad)
        tx1 = min(im.width, box[2] + pad + 1); ty1 = min(im.height, box[3] + pad + 1)
        tile = im.crop((tx0, ty0, tx1, ty1))
        core = measure_core(tile, style)
        core = clamp_core(core, cap)
        inpaint(im, box)
        tile = im.crop((tx0, ty0, tx1, ty1))
        new = render(text, style, tile.size, core)
        im.alpha_composite(new, (tx0, ty0))
        print(f'{fname}: {text} [{style}] core={core}')
    im.save(path)


def main():
    # ranking_tab: RANK | SCORE | USER NAME (column headers)
    replace('ranking_tab.png', [
        ((36, 30, 101, 60), '排名', 'blue', 18),
        ((194, 30, 270, 60), '分数', 'blue', 18),
        ((407, 30, 538, 60), '用户名', 'blue', 18),
    ])
    # replaylist_tab: DATE | SCORE | INFO
    replace('replaylist_tab.png', [
        ((21, 36, 86, 64), '日期', 'blue', 17),
        ((196, 36, 272, 64), '分数', 'blue', 17),
        ((539, 36, 595, 64), '信息', 'blue', 17),
    ])
    # practice_tab: STAGE-1..5 (white text on dark tabs)
    items = []
    ys = [(22, 39), (88, 105), (154, 172), (221, 236), (287, 303)]
    for i, (a, b) in enumerate(ys):
        items.append(((18, a - 4, 106, b + 4), f'第{i+1}关', 'white_off', 18))
    replace('practice_tab.png', items)
    # weponset buttons (Type header + weapon names)
    for suffix in ['_off', '_on']:
        hstyle = 'blue' if suffix == '_off' else 'orange_on'
        nstyle = 'white_off' if suffix == '_off' else 'orange_on'
        replace(f'weponset_btn_a{suffix}.png', [
            ((180, 18, 325, 66), '类型A', hstyle, None),
            ((58, 128, 112, 155), '蓝色', nstyle, 19),
            ((170, 128, 215, 155), '红色', nstyle, 19),
            ((268, 128, 335, 155), '绿色', nstyle, 19),
            ((371, 128, 451, 155), '黄色', nstyle, 19),
        ])
        replace(f'weponset_btn_b{suffix}.png', [
            ((180, 18, 325, 66), '类型B', hstyle, None),
            ((52, 128, 124, 155), '蓝色-S', nstyle, 19),
            ((150, 128, 230, 155), '橙色', nstyle, 19),
            ((258, 128, 348, 155), '翠绿', nstyle, 19),
            ((376, 128, 450, 155), '紫色', nstyle, 19),
        ])
    # config_controller: action labels
    replace('config_controller.png', [
        ((0, 0, 166, 36), '连射', 'blue', None),
        ((0, 82, 96, 118), '冲刺', 'blue', None),
        ((0, 156, 141, 194), '提速', 'blue', None),
        ((0, 236, 181, 278), '减速', 'blue', None),
        ((0, 320, 91, 348), '暂停', 'blue', None),
    ])
    print('done')


if __name__ == '__main__':
    main()
