"""把 Python 解法的执行过程记录成帧，生成 docs/public/viz/<name>.json，
页面里用 <StepPlayer src="/viz/<name>.json" /> 播放。

用法见 tools/traces/ 下的例子：在解法的关键位置调用 t.list(...) 或 t.array(...)。
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "public" / "viz"


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def build(vals):
    """返回 (head, nodes)。nodes 是按原始顺序排列的全部结点，画图时位置固定不动。"""
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    return (nodes[0] if nodes else None), nodes


class Trace:
    def __init__(self, name: str, title: str):
        self.name = name
        self.title = title
        self.frames: list[dict] = []

    def list(self, nodes, ptr: dict, note: str, hl=()):
        """nodes: 固定顺序的结点列表；ptr: {'cur': node 或 None}；None 画成 ∅。"""
        idx = {id(n): k for k, n in enumerate(nodes)}
        self.frames.append({
            "kind": "list",
            "vals": [n.val for n in nodes],
            "next": [idx.get(id(n.next)) if n.next is not None else None for n in nodes],
            "ptr": {k: (len(nodes) if v is None else idx[id(v)]) for k, v in ptr.items()},
            "hl": [idx[id(n)] for n in hl if n is not None],
            "note": note,
        })

    def array(self, cells, ptr: dict, note: str, hl=(), window=None, extra=""):
        """ptr: {'l': 0, 'r': 3}；window: (l, r) 闭区间；extra: 额外状态（如哈希表内容）。"""
        self.frames.append({
            "kind": "array",
            "cells": list(cells),
            "ptr": dict(ptr),
            "hl": list(hl),
            "window": list(window) if window else None,
            "extra": extra,
            "note": note,
        })

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / f"{self.name}.json"
        path.write_text(json.dumps({"title": self.title, "frames": self.frames}, ensure_ascii=False, indent=1))
        print(f"{path.relative_to(OUT.parent.parent.parent)}: {len(self.frames)} 帧")
