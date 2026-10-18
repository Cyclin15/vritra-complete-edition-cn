"""Corona resource.car + Lua 5.1 (Corona flavor) bytecode patcher.

Car format (per Solar2D librtt/Rtt_Archive.cpp):
  "rac\x01"
  [kContentsTag=1:u32][contentsLen:u32]
  contents:
    [numElements:u32]
    per entry: [type=1:u32][offset:u32][nameLen:u32][name][\0][pad4]
  data blocks (contiguous, stride = align4(12+srclen)):
    [kDataTag=2:u32][4+align4(srclen):u32][srclen:u32][data][pad4]
  EOF: [kEOFTag=0xFFFFFFFF:u32][0:u32]

Lua 5.1 chunk (Corona flavor: no LUAC_TAIL, LUA_TBOOLEAN has value byte):
  header 12 bytes; protos: src TS, linedef, lastlinedef, nups, numparams,
  is_vararg, maxstack, [ncode:u32][code], [nk + consts], [nprotos + protos],
  [nline + ints], [nlocvars + (name, start, end)], [nupvals + names]
"""
import struct


# ---------- Lua chunk parse/serialize ----------

def _r_ts(d, p):
    n = struct.unpack_from('<I', d, p)[0]
    p += 4
    if n == 0:
        return None, p
    s = d[p:p + n]
    p += n
    assert s[-1] == 0, 'string not null-terminated'
    return s[:-1], p


def _w_ts(b, s):
    if s is None:
        b += struct.pack('<I', 0)
    else:
        b += struct.pack('<I', len(s) + 1) + s + b'\x00'
    return b


def parse_proto(d, p):
    src, p = _r_ts(d, p)
    linedef, lastdef = struct.unpack_from('<ii', d, p); p += 8
    nups, numparams, vararg, maxstack = d[p], d[p+1], d[p+2], d[p+3]; p += 4
    ncode = struct.unpack_from('<I', d, p)[0]; p += 4
    code = d[p:p + ncode*4]; p += ncode*4
    nk = struct.unpack_from('<I', d, p)[0]; p += 4
    consts = []
    for i in range(nk):
        t = d[p]; p += 1
        if t == 0:
            consts.append((0, None))
        elif t == 1:
            consts.append((1, d[p])); p += 1
        elif t == 3:
            consts.append((3, d[p:p+8])); p += 8
        elif t == 4:
            s, p = _r_ts(d, p)
            consts.append((4, s))
        else:
            raise ValueError(f'bad const type {t} at {p-1:#x}')
    nprotos = struct.unpack_from('<I', d, p)[0]; p += 4
    protos = []
    for i in range(nprotos):
        pr, p = parse_proto(d, p)
        protos.append(pr)
    nline = struct.unpack_from('<I', d, p)[0]; p += 4
    lineinfo = d[p:p + nline*4]; p += nline*4
    nloc = struct.unpack_from('<I', d, p)[0]; p += 4
    locvars = []
    for i in range(nloc):
        nm, p = _r_ts(d, p)
        s, e = struct.unpack_from('<ii', d, p); p += 8
        locvars.append((nm, s, e))
    nup = struct.unpack_from('<I', d, p)[0]; p += 4
    upvals = []
    for i in range(nup):
        nm, p = _r_ts(d, p)
        upvals.append(nm)
    proto = dict(src=src, linedef=linedef, lastdef=lastdef, nups=nups,
                 numparams=numparams, vararg=vararg, maxstack=maxstack,
                 code=code, consts=consts, protos=protos,
                 lineinfo=lineinfo, locvars=locvars, upvals=upvals)
    return proto, p


def write_proto(b, f):
    b = _w_ts(b, f['src'])
    b += struct.pack('<ii', f['linedef'], f['lastdef'])
    b += bytes([f['nups'], f['numparams'], f['vararg'], f['maxstack']])
    b += struct.pack('<I', len(f['code'])//4) + f['code']
    b += struct.pack('<I', len(f['consts']))
    for t, v in f['consts']:
        b += bytes([t])
        if t == 1:
            b += bytes([v])
        elif t == 3:
            b += v
        elif t == 4:
            b = _w_ts(b, v)
    b += struct.pack('<I', len(f['protos']))
    for pr in f['protos']:
        b = write_proto(b, pr)
    b += struct.pack('<I', len(f['lineinfo'])//4) + f['lineinfo']
    b += struct.pack('<I', len(f['locvars']))
    for nm, s, e in f['locvars']:
        b = _w_ts(b, nm)
        b += struct.pack('<ii', s, e)
    b += struct.pack('<I', len(f['upvals']))
    for nm in f['upvals']:
        b = _w_ts(b, nm)
    return b


def parse_chunk(d):
    assert d[:12] == b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00', 'bad lua header'
    proto, p = parse_proto(d, 12)
    return proto, p


def write_chunk(proto):
    return b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00' + write_proto(b'', proto)[len(b''):] if False else write_proto(b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00', proto)


def replace_strings(proto, mapping, path=''):
    """Replace string constants (and proto source names never) by exact match.
    mapping: dict[bytes] -> bytes. Returns list of (path, old, new) applied."""
    applied = []
    new_consts = []
    for i, (t, v) in enumerate(proto['consts']):
        if t == 4 and v in mapping and mapping[v] != v:
            applied.append((f'{path}k[{i}]', v, mapping[v]))
            new_consts.append((4, mapping[v]))
        else:
            new_consts.append((t, v))
    proto['consts'] = new_consts
    for i, pr in enumerate(proto['protos']):
        applied += replace_strings(pr, mapping, f'{path}p[{i}].')
    return applied


def align4(n):
    return (n + 3) & ~3


# ---------- car parse/serialize ----------

def parse_car(d):
    assert d[:4] == b'rac\x01'
    tag, contents_len = struct.unpack_from('<II', d, 4)
    assert tag == 1
    num = struct.unpack_from('<I', d, 12)[0]
    p = 16
    entries = []
    for i in range(num):
        etype, off = struct.unpack_from('<II', d, p)
        nlen = struct.unpack_from('<I', d, p+8)[0]
        name = d[p+12:p+12+nlen]
        p = align4(p + 12 + nlen + 1)
        entries.append({'type': etype, 'offset': off, 'name': name})
    data_start = 12 + contents_len  # == 4 + 8 + contents_len
    blobs = {}
    for e in entries:
        tag2, a, b = struct.unpack_from('<III', d, e['offset'])
        assert tag2 == 2
        assert a == 4 + align4(b), f'bad len field for {e["name"]}'
        blobs[e['name']] = d[e['offset']+12:e['offset']+12+b]
    return entries, blobs


def build_car(entries, blobs):
    # entries: list of dicts with 'name' (bytes, stored form) ; blobs: name->bytes
    num = len(entries)
    contents_len = 4 + sum(12 + align4(len(e['name']) + 1) for e in entries)
    out = bytearray()
    out += b'rac\x01'
    out += struct.pack('<II', 1, contents_len)
    out += struct.pack('<I', num)
    # first pass: compute offsets
    offset_base = 4 + 8 + contents_len
    for e in entries:
        e['offset'] = offset_base
        offset_base += align4(len(blobs[e['name']])) + 12
    for e in entries:
        out += struct.pack('<II', e['type'], e['offset'])
        out += struct.pack('<I', len(e['name'])) + e['name'] + b'\x00'
        while len(out) % 4:
            out += b'\x00'
    assert len(out) == 12 + contents_len, (len(out), 12 + contents_len)
    for e in entries:
        blob = blobs[e['name']]
        out += struct.pack('<III', 2, 4 + align4(len(blob)), len(blob))
        out += blob
        while len(out) % 4:
            out += b'\x00'
    out += struct.pack('<II', 0xFFFFFFFF, 0)
    return bytes(out)


if __name__ == '__main__':
    import sys
    car_path = sys.argv[1] if len(sys.argv) > 1 else '../Resources/resource.car'
    d = open(car_path, 'rb').read()
    entries, blobs = parse_car(d)
    print(f'car: {len(entries)} entries, {len(d)} bytes')
    # round-trip test
    rebuilt = build_car(entries, blobs)
    print('car round-trip identical:', rebuilt == d)
    # lua round-trip test
    ok = bad = 0
    for e in entries:
        blob = blobs[e['name']]
        proto, consumed = parse_chunk(blob)
        assert consumed == len(blob)
        redump = write_chunk(proto)
        if redump == blob:
            ok += 1
        else:
            bad += 1
            if bad <= 3:
                print('LUA MISMATCH', e['name'])
    print(f'lua round-trip: {ok} ok, {bad} mismatch')
