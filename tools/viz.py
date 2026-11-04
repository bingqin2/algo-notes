"""把 Python 解法的执行过程记录成帧，生成 docs/public/viz/<name>.json，
页面里用 <StepPlayer src="/viz/<name>.json" /> 播放。

用法见 tools/traces/ 下的例子：在解法的关键位置调用 t.list(...)、t.array(...) 或 t.tree(...)。
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "public" / "viz"


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class NNode:
    """多叉树结点，用来画回溯的递归树。"""
    def __init__(self, val):
        self.val, self.children = val, []

    def add(self, val):
        ch = NNode(val)
        self.children.append(ch)
        return ch


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(level):
    """按层序列表建树，None 表示空：[3, 9, 20, None, None, 15, 7]"""
    if not level:
        return None
    it = iter(level)
    root = TreeNode(next(it))
    q = [root]
    for node in q:
        for side in ("left", "right"):
            v = next(it, None)
            if v is not None:
                setattr(node, side, TreeNode(v))
                q.append(getattr(node, side))
    return root


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

    def tree(self, root, ptr: dict, note: str, hl=(), dim=(), marks=None, extra=""):
        """root: TreeNode；ptr: {'cur': node}；marks: {node: '文字'} 显示在结点上方；dim: 变暗的结点。"""
        nodes, edges, order = [], [], {}
        def walk(n, d):
            if n is None:
                return
            walk(n.left, d + 1)
            order[id(n)] = len(order)
            nodes.append({"id": id(n), "val": n.val, "x": order[id(n)], "d": d})
            walk(n.right, d + 1)
            for ch in (n.left, n.right):
                if ch is not None:
                    edges.append([id(n), id(ch)])
        walk(root, 0)
        # id 换成小整数，JSON 更短
        remap = {nd["id"]: k for k, nd in enumerate(nodes)}
        for nd in nodes:
            nd["id"] = remap[nd["id"]]
        self.frames.append({
            "kind": "tree",
            "nodes": nodes,
            "edges": [[remap[a], remap[b]] for a, b in edges],
            "ptr": {k: remap[id(v)] for k, v in ptr.items() if v is not None},
            "hl": [remap[id(n)] for n in hl if n is not None],
            "dim": [remap[id(n)] for n in dim if n is not None],
            "marks": {str(remap[id(n)]): s for n, s in (marks or {}).items()},
            "extra": extra,
            "note": note,
        })

    def ntree(self, root, note: str, hl=(), dim=(), marks=None, ptr=None, extra=""):
        """多叉树（回溯的递归树）。结点要有 .val 和 .children。叶子从左到右排，父结点放在孩子中间。"""
        nodes, edges, pos = [], [], {}
        leaf = [0]
        def walk(n, d):
            for ch in n.children:
                walk(ch, d + 1)
                edges.append([id(n), id(ch)])
            if n.children:
                x = (pos[id(n.children[0])] + pos[id(n.children[-1])]) / 2
            else:
                x = leaf[0]
                leaf[0] += 1
            pos[id(n)] = x
            nodes.append({"id": id(n), "val": n.val, "x": x, "d": d})
        walk(root, 0)
        remap = {nd["id"]: k for k, nd in enumerate(nodes)}
        for nd in nodes:
            nd["id"] = remap[nd["id"]]
        self.frames.append({
            "kind": "tree",
            "wide": True,
            "nodes": nodes,
            "edges": [[remap[a], remap[b]] for a, b in edges],
            "ptr": {k: remap[id(v)] for k, v in (ptr or {}).items() if v is not None},
            "hl": [remap[id(n)] for n in hl if n is not None],
            "dim": [remap[id(n)] for n in dim if n is not None],
            "marks": {str(remap[id(n)]): s for n, s in (marks or {}).items()},
            "extra": extra,
            "note": note,
        })

    def grid(self, cells, note: str, hl=(), tone=None, extra=""):
        """二维网格。hl: [(r, c)]；tone: 和 cells 同形状的整数，0 不上色，1~4 是四种底色。"""
        self.frames.append({
            "kind": "grid",
            "cells": [list(r) for r in cells],
            "hl": [list(x) for x in hl],
            "tone": [list(r) for r in tone] if tone else None,
            "ptr": {},
            "extra": extra,
            "note": note,
        })

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / f"{self.name}.json"
        path.write_text(json.dumps({"title": self.title, "frames": self.frames}, ensure_ascii=False, indent=1))
        print(f"{path.relative_to(OUT.parent.parent.parent)}: {len(self.frames)} 帧")
