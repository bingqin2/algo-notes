"""C 层带图解的题（第二部分）：460 LFU。"""
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc460():
    cap, rows = 2, 3
    kv, fk, minf = {}, defaultdict(OrderedDict), 0
    t = Trace("lc460", "460 LFU 缓存 · 频率桶 + minFreq（capacity = 2）")

    def frame(note, hl=(), red=()):
        cells, tone = [], []
        for f in range(1, rows + 1):
            keys = list(fk.get(f, {}))
            row = [f"freq {f}"] + [f"k{k}" for k in keys] + [""] * (cap - len(keys))
            cells.append(row)
            tone.append([1 if f == minf and kv else 0] + [4 if (f, k) in red else 0 for k in keys] + [0] * (cap - len(keys)))
        pos = [(f - 1, 1 + list(fk[f]).index(k)) for f, k in hl]
        extra = "kv = {" + ", ".join(f"{k}: (val {v}, freq {fr})" for k, (v, fr) in kv.items()) + "}" + f" · minFreq = {minf}"
        t.grid(cells, note, hl=pos, tone=tone, extra=extra)

    def touch(key):
        nonlocal minf
        f = kv[key][1]
        del fk[f][key]
        if not fk[f]:
            del fk[f]
            if minf == f:
                minf = f + 1
        kv[key][1] = f + 1
        fk[f + 1][key] = None

    frame("每个频率一个桶，桶里的 key 按最近使用排序（左边最久）。kv 存 key → (值, 频率)，minFreq 记最小频率（绿色那一行）。")
    for op, *args in [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("get", 3), ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)]:
        key = args[0]
        if op == "get":
            if key not in kv:
                frame(f"get({key})：不在 kv 里，返回 −1。")
                continue
            f = kv[key][1]
            touch(key)
            frame(f"get({key}) = {kv[key][0]}：频率 {f} → {f + 1}，从 freq {f} 的桶移到 freq {f + 1} 的桶末尾。" +
                  (f"freq {f} 的桶空了，而它正是 minFreq，所以 minFreq = {minf}。" if f not in fk and minf == f + 1 else ""), hl=[(f + 1, key)])
        else:
            if len(kv) == cap:
                old = next(iter(fk[minf]))
                frame(f"put({key}, {args[1]})：缓存满了。淘汰 minFreq = {minf} 的桶里最左边（最久没用）的 k{old}。" +
                      ("同频率时按 LRU 淘汰。" if len(fk[minf]) > 1 else ""), red=[(minf, old)])
                fk[minf].popitem(last=False)
                if not fk[minf]:
                    del fk[minf]
                del kv[old]
            kv[key] = [args[1], 1]
            fk[1][key] = None
            minf = 1
            frame(f"put({key}, {args[1]})：新 key 频率是 1，放进 freq 1 的桶，minFreq 重置为 1。", hl=[(1, key)])
    frame("get 和 put 都是 O(1)：哈希表找 key，OrderedDict（Java 里用 LinkedHashSet）按顺序删插，minFreq 只会 +1 或重置为 1。")
    t.save()


if __name__ == "__main__":
    lc460()
