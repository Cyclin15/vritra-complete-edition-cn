import json
out = json.load(open('_cn_work/all_strings.json', encoding='utf-8'))
for k in ['lib.gshoot.base.display.storydisplay_textver.lu','lib.gshoot.content.ending_pc.lu','lib.gshoot.content.ending.staffrollitem.lu','lib.gshoot.content.corporate.lu']:
    print(f'===== {k}')
    seen = set()
    for pos, s in out[k]:
        if s in seen or not s: continue
        seen.add(s)
        if len(s) >= 10:
            print(f'--- {pos}')
            print(s)
