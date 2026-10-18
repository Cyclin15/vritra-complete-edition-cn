# -*- coding: utf-8 -*-
"""Repaint English text frames inside sp_ui_1.png / sp_ending.png with zpix Chinese.

Frames are TexturePacker-trimmed; the json keeps spriteSourceSize, so repainting
pixels inside each frame rect preserves the game's sprite geometry untouched.

Usage:
  python patch_sprites.py analyze   # print plan, change nothing
  python patch_sprites.py apply     # backup + repaint + save
  python patch_sprites.py verify    # OCR the patched frames
"""
import os
import sys
import json
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPR = os.path.join(ROOT, 'Resources', 'asset', 'sprites')
BAK = os.path.join(ROOT, '_cn_work', 'ui_backup')
FONT = os.path.join(ROOT, 'Resources', 'MatryoshkaXS.ttf')  # zpix

UI = {
    # 22-31 button guide labels (white + black shadow)
    22: '确定', 23: '关闭', 24: '返回', 25: '查看回放', 26: '删除回放',
    27: '开始游戏', 28: '选择', 29: '保存回放', 30: '跳过', 31: '删除设置',
    # 37-43 boss names (plain white, decorative latin; kept centered)
    37: '天蝎', 38: '魔蛛', 39: 'VRITRA复制体', 40: '迦楼罗',
    41: '魔蜓', 42: 'VRITRA', 43: '诅咒VRITRA',
    # 32-36 stage titles (plain white, big)
    32: '第1关 序章',
    33: '第2关 钢铁守护者',
    34: '第3关 不祥的预感',
    35: '第4关 森林中的古代遗迹',
    36: '第5关 被封印的古代帝国',
    # 48-51 difficulty descriptions (white + black shadow, multi-line)
    48: [(0, 19, '基础难度，适合射击游戏的新手玩家。'),
         (20, 43, '初始残机 x 5')],
    49: [(0, 19, '街机难度，适合擅长射击游戏的玩家。'),
         (20, 43, '2000000 / 7000000 分追加残机')],
    50: [(0, 19, '专家难度，适合熟悉VRITRA的玩家。'),
         (20, 38, '玩家将挑战本作的真Boss。'),
         (39, 64, '4000000 / 12000000 分追加残机')],
    51: [(0, 19, '这是为弹幕高手准备的最高难度。'),
         (20, 38, '玩家将挑战本作的真Boss。'),
         (39, 64, '6000000 / 15000000 分追加残机')],
    # 67-110 story lines (plain white)
    67: '因陀罗翱翔于天际。民众的悲鸣、',
    68: '以及笼罩天空的黑暗，都是魔物复苏的征兆。',
    69: '因陀罗存在的唯一使命，就是消灭那股',
    70: '妄图吞噬整个世界的邪恶',
    71: 'GOLIATH是曾保护人们免受魔物入侵的战舰之名。',
    72: '那曾被誉为钢铁守护者的英雄，如今',
    73: '已沦为魔物盘踞的巢穴。在其深处，能感觉到VRITRA的气息。',
    74: '因陀罗必须设法潜入这座巢穴',
    75: '察觉到VRITRA强烈的气息，因陀罗进入了GOLIATH的内部。',
    76: '舰体内部布满了疑似属于VRITRA的细胞纤维，',
    77: '使其内部宛如活物的体内一般。',
    78: '他一定就藏身于此。但总觉得有些不对劲',
    79: '森林遗迹突然发起了攻击，仿佛早已埋伏多时，专候因陀罗前来。',
    80: '这难道也是VRITRA复苏的征兆之一？',
    81: '但时间紧迫。夜幕即将降临',
    82: '古代文明的武器泛着不祥的光芒，伺机消灭一切来犯者。',
    83: '一场场恶战下来，因陀罗的力量不断被消耗。',
    84: '但他已无路可退。必须在日落之前击败VRITRA。',
    85: '蝎子外形的魔物，因VRITRA的复苏而觉醒',
    86: '被诅咒的魔物自大地深处的沉眠中苏醒，向因陀罗袭来。',
    87: '它那硬过钢铁的尾巴，刺穿并粉碎挡路的一切。',
    88: '这是GOLIATH防卫系统与蜘蛛魔物的融合体。',
    89: '它沿蛛网爬行，能在空中自由移动，捕食入侵者。',
    90: '它那炽热的蛛丝能瞬间熔化猎物、将其化为灰烬',
    91: '而不只是单纯地将其捕获。',
    92: 'VRITRA亲手制造的VRITRA复制体。它通过增殖自身的',
    93: '腐朽血肉，正在吞噬庇护其本体的GOLIATH。',
    94: '尽管它的躯体不过是骸骨与少量的',
    95: '腐肉所构成，其实力却丝毫不逊于VRITRA本体。',
    96: '守护古代遗迹的蜜蜂外形魔物。',
    97: '这只机动性极高的魔物能从各个角度射出弹幕，',
    98: '将目标打得千疮百孔。它不时释放的强力雷电',
    99: '会吞噬一切，连影子都不留。',
    100: '统治古代遗迹的蜻蜓外形魔物。',
    101: '它凭借众多眼睛组成的监视网络，',
    102: '清除古代遗迹中一切入侵者的残迹',
    103: '想从它手中逃脱绝非易事。',
    104: '因陀罗终于抵达了宿敌VRITRA的面前。',
    105: '但他必须抓紧。一旦夜幕降临，VRITRA将获得无可匹敌的力量。',
    106: '“邪龙VRITRA啊。我存在的唯一意义，就是消灭你。”',
    107: '这是VRITRA挣脱太阳的枷锁、',
    108: '解放黑暗之力后的真正形态。击败他的希望',
    109: '几近于零。而这正是因陀罗必须直面他的理由。',
    110: '“现在就做个了结吧……终结这场永远纠缠着我们的战争。”',
}

ENDING = {
    # 0-4 ending part 1, 5-10 ending part 2 (plain white)
    0: '邪龙VRITRA消失在了沉落的夕阳之中。',
    1: '然而，和平并没有重返世界。',
    2: '世界各地仍有魔物在肆虐，',
    3: 'VRITRA强大的妖气依然残留不散。',
    4: '因陀罗没有时间休息。',
    5: '邪龙VRITRA终于被封印了。',
    6: '邪恶的古代帝国轰然崩塌，世界得救了。',
    7: '回望在光明中欢庆的人们，',
    8: '英雄之神因陀罗返回了自己的神殿。',
    9: '他在那里休养战伤，并为必将',
    10: '降临世界的下一场灾厄做着准备……',
    # 49 last message (white + black shadow)
    49: '荣耀归于弹幕射击！',
}

SHEETS = {
    'sp_ui_1.png': UI,
    'sp_ending.png': ENDING,
}

# uniform ink height per frame group: original latin frames with descenders
# (y/g/commas) measure taller than the pure cap height, which would make the
# repainted CJK sizes inconsistent within a group.
INK_H = {
    'sp_ui_1.png': {**{i: 26 for i in range(22, 32)},      # guide labels
                    **{i: 30 for i in range(37, 44)},      # boss names
                    **{i: 44 for i in range(32, 37)},      # stage titles
                    **{i: 18 for i in range(67, 111)}},    # story lines
}


def fit_font(text, ink_h, max_w):
    """zpix size so ink height ~= ink_h and width <= max_w."""
    size = max(8, int(ink_h))
    f = bb = None
    for _ in range(12):
        f = ImageFont.truetype(FONT, size)
        d = ImageDraw.Draw(Image.new('L', (4, 4)))
        bb = d.textbbox((0, 0), text, font=f)
        h = bb[3] - bb[1]
        w = bb[2] - bb[0]
        if h <= 0:
            size += 2
            continue
        if w > max_w:
            ns = max(8, int(size * max_w / w))
            if ns == size:
                break
            size = ns
            continue
        if abs(h - ink_h) <= 1 or size <= 8:
            break
        size += 1 if h < ink_h else -1
    return f, bb


def render_text(text, ink_h, max_w, shadow):
    f, bb = fit_font(text, ink_h, max_w)
    pad = 4
    W = (bb[2] - bb[0]) + 2 * pad + 2
    H = (bb[3] - bb[1]) + 2 * pad + 2
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ox, oy = pad - bb[0], pad - bb[1]
    if shadow:
        d.text((ox + 1, oy + 1), text, font=f, fill=(0, 0, 0, 255))
    d.text((ox, oy), text, font=f, fill=(255, 255, 255, 255))
    return img


def ink_of(img):
    a = np.array(img)
    vis = a[:, :, 3] > 80
    if not vis.any():
        return None
    ys, xs = np.where(vis)
    return xs.min(), xs.max(), ys.min(), ys.max()


def has_shadow(region_img):
    a = np.array(region_img)
    vis = a[:, :, 3] > 80
    if not vis.any():
        return False
    rgb = a[:, :, :3][vis]
    return float(np.sum(rgb.mean(axis=1) < 50)) / vis.sum() > 0.12


def plan_frame(sheet, frames, idx, spec, ink_h_override=None, force_center=False):
    """Return list of paint ops: (text, shadow, paste_xy_in_frame, timg)."""
    f = frames[idx]['frame']
    fx, fy, fw, fh = f['x'], f['y'], f['w'], f['h']
    region = sheet.crop((fx, fy, fx + fw, fy + fh))
    shadow = has_shadow(region)
    lines = spec if isinstance(spec, list) else [(0, fh, spec)]
    ops = []
    for (y0, y1, text) in lines:
        band = region.crop((0, y0, fw, y1))
        ib = ink_of(band)
        if ib:
            bx0, bx1, by0, by1 = ib
            line_cx = (bx0 + bx1) / 2
        else:
            bx0 = 2
            line_cx = fw / 2
            by0 = (y0 + y1) // 2 - 9
            by1 = by0 + 17
        ink_h = ink_h_override or (by1 - by0 + 1)
        centered = force_center or (
            abs(line_cx - fw / 2) < fw * 0.06 and bx0 > fw * 0.08)
        max_w = fw - (2 if centered else bx0) - 2
        timg = render_text(text, ink_h, max_w, shadow)
        tib = ink_of(timg)
        tx0, tx1, ty0, ty1 = tib
        if centered:
            px = fw / 2 - (tx0 + tx1) / 2
        else:
            px = bx0 - tx0
        cy = (by0 + by1) / 2 + y0
        py = cy - (ty0 + ty1) / 2
        ops.append((text, shadow, int(round(px)), int(round(py)), timg))
    return ops


def main(mode):
    for fname, transl in SHEETS.items():
        path = os.path.join(SPR, fname)
        sheet = Image.open(path).convert('RGBA')
        meta = json.load(open(os.path.join(SPR, fname.replace('.png', '.json')),
                              encoding='utf-8-sig'))
        frames = meta['frames']
        print(f'== {fname}: {len(transl)} frames ==')
        if mode == 'apply':
            os.makedirs(BAK, exist_ok=True)
            bp = os.path.join(BAK, fname)
            if not os.path.exists(bp):
                shutil.copy(path, bp)
                print('backup ->', bp)
        for idx in sorted(transl):
            ops = plan_frame(sheet, frames, idx, transl[idx],
                             INK_H.get(fname, {}).get(idx),
                             force_center=(fname == 'sp_ui_1.png' and 37 <= idx <= 43))
            f = frames[idx]['frame']
            for text, shadow, px, py, timg in ops:
                w = timg.size[0]
                print(f'  f{idx:3d} [{f["w"]:4d}x{f["h"]}] {text!r} '
                      f'shadow={int(shadow)} paste=({px},{py}) w={w}')
            if mode == 'apply':
                sheet.paste((0, 0, 0, 0), (f['x'], f['y'],
                                           f['x'] + f['w'], f['y'] + f['h']))
                for text, shadow, px, py, timg in ops:
                    sheet.paste(timg, (f['x'] + px, f['y'] + py), timg)
        if mode == 'apply':
            sheet.save(path)
            print('saved', path)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'analyze')
