import json, re
d = json.load(open('Resources/lib/data/texts_en.json', encoding='utf-8'))
print('texts_en.json keys:', len(d))
for k,v in list(d.items())[:15]:
    print(repr(k), '=>', repr(v[:80] if isinstance(v,str) else v))
print()
out = json.load(open('_cn_work/all_strings.json', encoding='utf-8'))
pat = re.compile(r"^[A-Za-z0-9 !?'\"().:%-]+$")
for k in ['lib.gshoot.content.gameover_pc.lu','lib.gshoot.content.howto_pc.lu','lib.gshoot.content.config_pc.lu']:
    if k not in out:
        print('MISSING', k); continue
    print(f'=== {k}')
    seen=set()
    for pos, s in out[k]:
        if s in seen or not s: continue
        seen.add(s)
        if pat.match(s) and len(s)>2 and not s.startswith('lib.') and not s.startswith('asset'):
            print(f'  {pos} {s!r}')
