import json, re
def load(p):
    raw = open(p, encoding='utf-8').read()
    fixed = re.sub(r',(\s*[}\]])', r'\1', raw)
    return json.loads(fixed)
d = load('Resources/lib/data/texts_en.json')
o = load('Resources/lib/data/texts_en1.json')
def walk(obj, prefix=''):
    out = {}
    if isinstance(obj, dict):
        for k,v in obj.items(): out.update(walk(v, prefix+'/'+str(k)))
    else: out[prefix] = obj
    return out
fd, fo = walk(d), walk(o)
print('cur keys:', len(fd), ' orig keys:', len(fo))
import unicodedata
def is_ascii(s): return all(ord(c)<128 for c in s)
miss = [k for k in fo if k not in fd]
print('missing in current:', miss)
still_eng = [k for k,v in fd.items() if isinstance(v,str) and is_ascii(v) and len(v)>3 and k not in ('____comment_____',) and not k.endswith('img_path') and 'asset' not in v]
print('still-english values:')
for k in still_eng: print(' ', k, '=>', repr(fd[k])[:90])
# also array values
for k,v in fd.items():
    if isinstance(v, list):
        for i,x in enumerate(v):
            if isinstance(x,str) and is_ascii(x) and len(x)>3 and 'asset' not in x and x not in ('ERROR','SUCCESS','OK','YES','NO'):
                print(' list', k, i, '=>', repr(x)[:90])
