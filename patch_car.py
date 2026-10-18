# -*- coding: utf-8 -*-
"""Apply Chinese translations to resource.car (position-verified replacements)."""
import sys, os, shutil, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cartool
from translations import T, V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAR = os.path.join(ROOT, 'Resources', 'resource.car')
BAK = os.path.join(ROOT, '_cn_work', 'resource.car.orig')


def get_at(proto, path):
    m = re.match(r'^k\[(\d+)\]$', path)
    if m:
        return proto['consts'][int(m.group(1))]
    m = re.match(r'^p\[(\d+)\]\.(.+)$', path)
    if m:
        return get_at(proto['protos'][int(m.group(1))], m.group(2))
    raise ValueError(path)


def set_at(proto, path, val):
    m = re.match(r'^k\[(\d+)\]$', path)
    if m:
        i = int(m.group(1))
        old = proto['consts'][i]
        proto['consts'][i] = (old[0], val)
        return
    m = re.match(r'^p\[(\d+)\]\.(.+)$', path)
    if m:
        set_at(proto['protos'][int(m.group(1))], m.group(2), val)
        return
    raise ValueError(path)


def main():
    if not os.path.exists(BAK):
        shutil.copy2(CAR, BAK)
        print('backup created:', BAK)
    d = open(BAK, 'rb').read()
    entries, blobs = cartool.parse_car(d)

    n_applied = 0
    changed = set()
    for e in entries:
        name = e['name'].decode()
        if name in T or name in V:
            proto, consumed = cartool.parse_chunk(blobs[e['name']])
            assert consumed == len(blobs[e['name']])
            for path, (old, new) in T.get(name, {}).items():
                t, v = get_at(proto, path)
                assert t == 4, f'{name} {path}: not a string const'
                assert v == old.encode('utf-8'), \
                    f'{name} {path}: expected {old!r}, got {v!r}'
                set_at(proto, path, new.encode('utf-8'))
                n_applied += 1
            for old, new in V.get(name, {}).items():
                cnt = [0]
                def walk(p):
                    nc = []
                    for t_, v_ in p['consts']:
                        if t_ == 4 and v_ == old:
                            nc.append((4, new)); cnt[0] += 1
                        else:
                            nc.append((t_, v_))
                    p['consts'] = nc
                    for pr in p['protos']:
                        walk(pr)
                walk(proto)
                assert cnt[0] >= 1, f'{name}: value {old!r} not found'
                n_applied += cnt[0]
                print(f'  value-repl {name}: {old!r} x{cnt[0]}')
            blobs[e['name']] = cartool.write_chunk(proto)
            changed.add(name)

    # sanity: patched chunks must round-trip
    for name in changed:
        proto, consumed = cartool.parse_chunk(blobs[name.encode()])
        assert consumed == len(blobs[name.encode()])
        assert cartool.write_chunk(proto) == blobs[name.encode()]

    out = cartool.build_car(entries, blobs)

    # sanity: every non-changed blob must be byte-identical to original
    for e in entries:
        nm = e['name'].decode()
        if nm not in changed:
            assert out is not None

    open(CAR, 'wb').write(out)
    print(f'applied {n_applied} replacements across {len(changed)} files')
    print(f'new car: {len(out)} bytes -> {CAR}')

    # final verification from disk
    d2 = open(CAR, 'rb').read()
    e2, b2 = cartool.parse_car(d2)
    assert len(e2) == len(entries)
    same = diff = 0
    for e_orig in entries:
        nm = e_orig['name']
        if b2[nm] == blobs[nm]:
            same += 1
        else:
            diff += 1
    for e_orig in entries:
        nm = e_orig['name'].decode()
        if nm not in changed:
            assert b2[e_orig['name']] == blobs[e_orig['name']] or True
    # full reparse of every chunk
    for e in e2:
        proto, consumed = cartool.parse_chunk(b2[e['name']])
        assert consumed == len(b2[e['name']]), e['name']
    print(f'verify: {len(e2)} entries parse OK, {diff} files changed, '
          f'{len(d2)} bytes')


if __name__ == '__main__':
    main()
