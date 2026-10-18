import json, re
out = json.load(open('_cn_work/all_strings.json', encoding='utf-8'))
files = ['lib.gshoot.base.pausedisplay_pc.lu','lib.gshoot.base.setsunafinish.lu',
         'lib.gshoot.base.keyconfigdisplay.lu','lib.gshoot.base.keyconfigdisplay_old.lu',
         'lib.gshoot.content.howto.lu','lib.gshoot.content.howto_cover.lu',
         'lib.gshoot.base.stagecleardisplay.lu','lib.gshoot.content.mainmenu_pc.practice.lu',
         'lib.gshoot.content.mainmenu_pc.selectdifficulty.lu',
         'lib.gshoot.content.mainmenu.howto.lu']
pat = re.compile(r"^[ -~\s]+$")
for k in files:
    print(f'===== {k}')
    for pos, s in out[k]:
        if not s: continue
        if len(s) >= 3 and pat.match(s) and not s.startswith('lib.') and not s.startswith('asset'):
            if re.search(r'[A-Za-z]{3}', s) and not re.match(r'^[a-z_]+$', s.replace(' ','')):
                print(f'{pos}\t{s!r}')
