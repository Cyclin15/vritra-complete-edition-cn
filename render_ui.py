# -*- coding: utf-8 -*-
"""Regenerate English UI images with Chinese pixel-font text (zpix).

Styles replicated from pixel analysis of originals:
  white_off : white core + black shadow offset(1,1) a~0.42 blur0.8   (menu btn off)
  orange_on : black core + orange(249,72,2) rim(dilate1) + soft glow (menu btn on)
  blue      : white(231,253,252) core + light-blue(144,186,231) rim + blue(22,155,248) tight glow
  bluebig   : white core + big blue(15,130,229) glow                 (STAGE CLEAR)
  red       : white core + big red(255,42,0) glow                    (GAME OVER)
  setsuna   : gradient core white->(134,183,233) + dark blue(12,110,210) rim + glow
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, 'Resources', 'asset_ui')
BAK = os.path.join(ROOT, '_cn_work', 'ui_backup')
FONT = os.path.join(ROOT, 'Resources', 'MatryoshkaXS.ttf')  # zpix renamed

GLOWSIGMA = {'white_off': 0.8, 'orange_on': 3.2, 'blue': 1.0,
             'bluebig': 3.0, 'red': 3.0, 'setsuna': 2.0}
PAD = {'white_off': 3, 'orange_on': 9, 'blue': 4, 'bluebig': 8, 'red': 8, 'setsuna': 6}


def measure_core(im, style):
    """bbox of the text core pixels (the crisp glyph body)."""
    px = im.convert('RGBA').load()
    w, h = im.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 200:
                continue
            if style == 'orange_on':
                if r < 80 and g < 80 and b < 80:
                    xs.append(x); ys.append(y)
            else:
                if r > 200 and g > 200 and b > 200:
                    xs.append(x); ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def fit_font(text, target_h, max_w):
    """find zpix size so CJK ink height ~= target_h and width <= max_w."""
    size = max(8, int(target_h))
    for _ in range(6):
        f = ImageFont.truetype(FONT, size)
        d = ImageDraw.Draw(Image.new('L', (8, 8)))
        bb = d.textbbox((0, 0), text, font=f)
        ink_h = bb[3] - bb[1]
        ink_w = bb[2] - bb[0]
        if ink_h <= 0:
            size += 2; continue
        if ink_w > max_w:
            size = max(8, int(size * max_w / ink_w) - 1); continue
        if abs(ink_h - target_h) <= 1:
            return f, bb
        size = max(8, round(size * target_h / ink_h))
    return f, bb


def colorize(mask, rgb, alpha_scale=1.0, max_a=255):
    """L mask -> RGBA layer of solid color."""
    a = mask.point(lambda v: min(max_a, int(v * alpha_scale)))
    layer = Image.new('RGBA', mask.size, rgb + (0,))
    layer.putalpha(a)
    return layer


def render(text, style, canvas, core_bbox):
    cw, ch = canvas
    img = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    if core_bbox:
        cx = (core_bbox[0] + core_bbox[2]) / 2
        cy = (core_bbox[1] + core_bbox[3]) / 2
        target_h = core_bbox[3] - core_bbox[1] + 1
    else:
        cx, cy = cw / 2, ch / 2
        target_h = ch - 6
    pad = PAD[style]
    font, bb = fit_font(text, target_h, cw - 2 * pad)
    ink_w, ink_h = bb[2] - bb[0], bb[3] - bb[1]
    # place text so ink is centered on (cx, cy)
    tx = int(round(cx - ink_w / 2 - bb[0]))
    ty = int(round(cy - ink_h / 2 - bb[1]))
    # keep glow inside canvas
    tx = max(pad - 1, min(cw - pad - ink_w - 1, tx))
    ty = max(pad - 1, min(ch - pad - ink_h - 1, ty))
    # draw mask oversized
    m = Image.new('L', (cw, ch), 0)
    d = ImageDraw.Draw(m)
    d.text((tx, ty), text, font=font, fill=255)

    if style == 'white_off':
        shadow = m.transform(m.size, Image.AFFINE, (1, 0, -1, 0, 1, -1))
        shadow = shadow.filter(ImageFilter.GaussianBlur(0.8))
        img.alpha_composite(colorize(shadow, (0, 0, 0), 0.45))
        img.alpha_composite(colorize(m, (255, 255, 255)))
    elif style == 'orange_on':
        rim = m.filter(ImageFilter.MaxFilter(3))
        glow = rim.filter(ImageFilter.GaussianBlur(GLOWSIGMA[style]))
        img.alpha_composite(colorize(glow, (249, 72, 2), 1.9))
        img.alpha_composite(colorize(rim, (249, 72, 2)))
        core = m.filter(ImageFilter.MinFilter(3))
        img.alpha_composite(colorize(core, (0, 0, 0)))
    elif style == 'blue':
        rim = m.filter(ImageFilter.MaxFilter(3))
        glow = rim.filter(ImageFilter.GaussianBlur(GLOWSIGMA[style]))
        img.alpha_composite(colorize(glow, (22, 155, 248), 0.55))
        img.alpha_composite(colorize(rim, (144, 186, 231)))
        img.alpha_composite(colorize(m, (231, 253, 252)))
    elif style == 'bluebig':
        glow = m.filter(ImageFilter.GaussianBlur(GLOWSIGMA[style]))
        img.alpha_composite(colorize(glow, (15, 130, 229), 1.4))
        img.alpha_composite(colorize(m, (255, 255, 255)))
    elif style == 'red':
        glow = m.filter(ImageFilter.GaussianBlur(GLOWSIGMA[style]))
        img.alpha_composite(colorize(glow, (255, 42, 0), 1.4))
        img.alpha_composite(colorize(m, (255, 255, 255)))
    elif style == 'setsuna':
        rim = m.filter(ImageFilter.MaxFilter(3))
        glow = rim.filter(ImageFilter.GaussianBlur(GLOWSIGMA[style]))
        img.alpha_composite(colorize(glow, (134, 183, 233), 0.9))
        img.alpha_composite(colorize(rim, (12, 110, 210)))
        # vertical gradient core white -> light blue
        core = colorize(m, (255, 255, 255))
        grad = Image.new('L', (1, ch))
        for y in range(ch):
            grad.putpixel((0, y), int(255 - 100 * y / max(1, ch - 1)))
        grad = grad.resize((cw, ch))
        px = core.load()
        g = grad.load()
        for y in range(ch):
            for x in range(cw):
                r, gg, b, a = px[x, y]
                if a:
                    t = g[x, y] / 255
                    px[x, y] = (int(231 + (134 - 231) * (1 - t)),
                                int(253 + (183 - 253) * (1 - t)),
                                int(252 + (233 - 252) * (1 - t)), a)
        img.alpha_composite(core)
    return img


def process(fname, text, style):
    path = os.path.join(UI, fname)
    orig = Image.open(path).convert('RGBA')
    core = measure_core(orig, style)
    img = render(text, style, orig.size, core)
    os.makedirs(BAK, exist_ok=True)
    bp = os.path.join(BAK, fname)
    if not os.path.exists(bp):
        orig.save(bp)
    img.save(path)
    print(f'{fname}: {orig.size} core={core} -> {text}')


def main():
    S = []
    def both(base, text, en=True):
        S.append((f'{base}_off.png', text, 'white_off'))
        S.append((f'{base}_on.png', text, 'orange_on'))
        if en:
            S.append((f'{base}_off_en.png', text, 'white_off'))
            S.append((f'{base}_on_en.png', text, 'orange_on'))
    both('menubtn_gamestart', '开始游戏')
    both('menubtn_ranking', '排行榜')
    both('menubtn_practice', '练习')
    both('menubtn_replay', '回放')
    both('menubtn_config', '设置')
    both('menubtn_quit', '退出')
    both('menubtn_backtotop', '返回标题')
    both('menubtn_go_continue', '继续')
    both('menubtn_go_retry', '重试')
    both('menubtn_pause_resume', '继续')
    both('menubtn_howtoplay', '操作说明', en=False)
    both('menubtn_setsuna', '刹那 VRITRA', en=False)
    both('menubtn_tomugen', '无限 VRITRA', en=False)
    for key, cn in [('easy', '简单'), ('normal', '普通'), ('hard', '困难'),
                    ('arcade', '街机'), ('expert', '专家'), ('insane', '疯狂')]:
        both(f'menubtn_diff_{key}', cn, en=False)
    for key, cn in [('1', '蓝色'), ('2', '红色'), ('3', '绿色'), ('4', '黄色'),
                    ('5', '蓝色-S'), ('6', '橙色'), ('7', '翠绿'), ('8', '紫色')]:
        both(f'wepon_btn_{key}', cn, en=False)

    for f, t in [('config_title', '设置'), ('howto_title', '操作说明'),
                 ('ranking_title', '排行榜'), ('wepon_title', '选择你的武器'),
                 ('weponset_title', '选择武器配置'), ('text_maxrate', '最大倍率'),
                 ('text_stagescore', '关卡得分'),
                 ('windowtitle_pausemenu_en', '暂停菜单'),
                 ('windowtitle_practice_en', '练习'),
                 ('windowtitle_replay_en', '回放列表'),
                 ('windowtitle_selectdiff_en', '选择难度'),
                 ('windowtitle_controller', '控制器设置')]:
        S.append((f + '.png', t, 'blue'))

    diffs = ['普通模式'] * 2 + ['街机模式'] * 2 + ['专家模式'] * 2 + ['疯狂模式'] * 2
    for i in range(1, 9):
        S.append((f'windowtitle_ranking{i}.png', diffs[i - 1], 'blue'))
    wep = ['蓝色', '红色', '绿色', '黄色', '蓝色-S', '橙色', '翠绿', '紫色']
    for i, mode in [(9, '无限'), (17, '刹那')]:
        for j, w in enumerate(wep):
            S.append((f'windowtitle_ranking{i + j}.png', f'{mode} - {w}金刚杵', 'blue'))

    S.append(('title_gameover.png', '游戏结束', 'red'))
    S.append(('title_stageclear.png', '关卡完成', 'bluebig'))
    S.append(('title_stageclear_over.png', '关卡完成', 'bluebig'))

    for f, t in [('setsuna_bonus_1', '宝石奖励！'), ('setsuna_bonus_2', '全灭奖励！'),
                 ('setsuna_bonus_3', '歼灭奖励！'), ('setsuna_bonus_4', '隐藏奖励！'),
                 ('setsuna_challenge_1', '宝石挑战'), ('setsuna_challenge_2', '全灭挑战'),
                 ('setsuna_finish', '刹那结束')]:
        S.append((f + '.png', t, 'setsuna'))

    for fname, text, style in S:
        process(fname, text, style)
    print(f'\n{len(S)} images regenerated (originals backed up to _cn_work/ui_backup)')


if __name__ == '__main__':
    main()
