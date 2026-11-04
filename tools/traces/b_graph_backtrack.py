"""B 层：图、回溯里带图解的题：994（网格多源 BFS）、78（子集的递归树）。"""
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402
from backtrack_graph_a import Recorder, fmt  # noqa: E402


def lc994():
    g = [[2, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1], [2, 0, 1, 1]]
    m, n = len(g), len(g[0])
    t = Trace("lc994", "994 腐烂的橘子 · 多源 BFS（2 腐烂，1 新鲜，0 空）")
    tone = [[4 if g[r][c] == 2 else 0 for c in range(n)] for r in range(m)]
    q = deque((r, c) for r in range(m) for c in range(n) if g[r][c] == 2)
    fresh = sum(row.count(1) for row in g)
    t.grid(g, "把所有一开始就腐烂的橘子同时放进队列（多个起点），然后一层一层扩散，每一层就是一分钟。", hl=list(q), tone=tone, extra=f"minute = 0，新鲜 = {fresh}")
    minute = 0
    while q and fresh:
        minute += 1
        new = []
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and g[nr][nc] == 1:
                    g[nr][nc] = 2
                    tone[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    new.append((nr, nc))
        t.grid(g, f"第 {minute} 分钟：上一层的腐烂橘子把相邻的 {len(new)} 个新鲜橘子变坏（黄色），它们组成下一层。", hl=new, tone=tone, extra=f"minute = {minute}，新鲜 = {fresh}")
        for r, c in new:
            tone[r][c] = 4
    t.grid(g, ("还剩新鲜橘子，永远不会变坏，返回 -1。" if fresh else f"新鲜橘子全部变坏，用时 {minute} 分钟。") + "每个格子只入队一次，O(mn)。", tone=tone, extra=f"答案 = {-1 if fresh else minute}")
    t.save()


def lc78():
    nums = [1, 2, 3]
    rec = Recorder("[]")
    path, pnodes = [], [rec.root]

    def dfs(node, start):
        rec.res.append(path[:])
        rec.events.append((node, pnodes[:], f"到达结点 {fmt(path)}：每个结点都是一个子集，记录。", fmt(rec.res), "✓"))
        for i in range(start, len(nums)):
            ch = node.add(nums[i])
            path.append(nums[i])
            pnodes.append(ch)
            dfs(ch, i + 1)
            path.pop()
            pnodes.pop()

    dfs(rec.root, 0)
    t = Trace("lc78", "78 子集 · 回溯的递归树（start 之后的数才能选，避免重复）")
    rec.play(t, "从空集出发。在第 i 个数之后只能选下标更大的数，这样 [1, 2] 和 [2, 1] 只会出现一次。", f"一共 2³ = {len(rec.res)} 个子集，每个结点一个。时间 O(n · 2ⁿ)（复制路径要 O(n)）。")


if __name__ == "__main__":
    lc994()
    lc78()
