import json, re
out = json.load(open('_cn_work/all_strings.json', encoding='utf-8'))
files = ['lib.gshoot.content.config_pc.lu','lib.gshoot.content.pausedisplay_pc.lu',
         'lib.gshoot.content.setsunafinish.lu','lib.gshoot.content.gameover_pc.lu',
         'lib.gshoot.content.replaylist.lu','lib.gshoot.content.leaderboards.leaderboardslist.lu',
         'lib.gshoot.content.keyconfigdisplay.lu','lib.gshoot.content.mainmenu_pc.lu',
         'lib.gshoot.content.howto_pc.lu','lib.gshoot.base.display.wavedisplay.lu',
         'lib.gshoot.content.stagecleardisplay.lu']
pat = re.compile(r"^[ -~\s]+$")
for k in files:
    if k not in out:
        print('MISSING', k); continue
    print(f'===== {k}')
    for pos, s in out[k]:
        if not s: continue
        if len(s) >= 3 and pat.match(s) and not s.startswith('lib.') and not s.startswith('asset'):
            if re.search(r'[A-Za-z]{3}', s) and not re.match(r'^[a-z_]+$', s.replace(' ','')):
                print(f'{pos}\t{s!r}')
