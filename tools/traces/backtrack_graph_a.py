"""回溯、图 A 层题的执行过程：46、47、22、39、131、60、200、547、207、210。

回溯题画递归树：先把整棵树建好，再按 DFS 访问顺序一帧帧点亮。
"""
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import NNode, Trace  # noqa: E402


class Recorder:
    """回溯时记录事件：进入结点、找到答案、剪枝。最后按事件顺序生成帧。"""

    def __init__(self, root_label="·"):
        self.root = NNode(root_label)
        self.events = []      # (结点, 当前路径上的结点, 说明, 结果列表快照)
        self.marks = {}
        self.res = []

    def play(self, t, intro, outro):
        all_nodes = []
        def walk(n):
            all_nodes.append(n)
            for c in n.children:
                walk(c)
        walk(self.root)
        seen = {self.root}
        t.ntree(self.root, intro, hl=[self.root], dim=[n for n in all_nodes if n not in seen], extra="res = []")
        marks = {}
        for node, path, note, res, mark in self.events:
            seen.add(node)
            if mark:
                marks[node] = mark
            t.ntree(self.root, note, hl=path, dim=[n for n in all_nodes if n not in seen], marks=dict(marks), extra=f"res = {res}")
        t.ntree(self.root, outro, marks=dict(marks), extra=f"res = {self.res}")
        t.save()


def fmt(xs):
    return "[" + ", ".join(map(str, xs)) + "]"


def lc46():
    nums = [1, 2, 3]
    rec = Recorder()
    used = [False] * 3
    path, pnodes = [], [rec.root]

    def dfs(node):
        if len(path) == 3:
            rec.res.append(path[:])
            rec.events.append((node, pnodes[:], f"路径 {fmt(path)} 长度够了，记录答案，然后回溯。", fmt(rec.res), "✓"))
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            ch = node.add(x)
            used[i] = True
            path.append(x)
            pnodes.append(ch)
            if len(path) < 3:
                rec.events.append((ch, pnodes[:], f"选 {x}，路径 {fmt(path)}。下一层只能选还没用过的数。", fmt(rec.res), None))
            dfs(ch)
            pnodes.pop()
            path.pop()
            used[i] = False

    dfs(rec.root)
    t = Trace("lc46", "46 全排列 · 递归树（used 数组）")
    rec.play(t, "每一层决定一个位置放哪个数。高亮的是当前路径，灰色是还没走到的分支。",
             "6 个叶子就是 6 个排列。树有 n 层，第 k 层有 n!/(n-k)! 个结点，总时间 O(n · n!)。")


def lc47():
    nums = [1, 1, 2]
    labels = ["1", "1′", "2"]
    rec = Recorder()
    used = [False] * 3
    path, pnodes = [], [rec.root]

    def dfs(node):
        if len(path) == 3:
            rec.res.append(path[:])
            rec.events.append((node, pnodes[:], f"得到 {fmt(path)}，记录。", fmt(rec.res), "✓"))
            return
        for i in range(3):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                ch = node.add(labels[i])
                rec.events.append((ch, pnodes[:] + [ch], f"想在这一层选 1′，但前一个相同的 1 在这一层已经试过（used = False）。选它会得到重复的排列，剪掉。", fmt(rec.res), "✗"))
                continue
            ch = node.add(labels[i])
            used[i] = True
            path.append(nums[i])
            pnodes.append(ch)
            if len(path) < 3:
                rec.events.append((ch, pnodes[:], f"选 {labels[i]}，路径 {fmt(path)}。", fmt(rec.res), None))
            dfs(ch)
            pnodes.pop()
            path.pop()
            used[i] = False

    dfs(rec.root)
    t = Trace("lc47", "47 全排列 II · 同层去重（1′ 表示第二个 1）")
    rec.play(t, "先排序，相同的数挨在一起。规则：两个 1 只能按「先 1 后 1′」的顺序用。",
             "被剪掉的分支（✗）都会生成和左边兄弟一样的排列。最后只剩 3 个不重复的排列。")


def lc22():
    n = 3
    rec = Recorder()
    path, pnodes = [], [rec.root]

    def dfs(node, o, c):
        if len(path) == 2 * n:
            rec.res.append("".join(path))
            rec.events.append((node, pnodes[:], f"长度 {2 * n}，得到 {''.join(path)}。", fmt(rec.res), "✓"))
            return
        for ch_char, ok, no, nc, why in (("(", o < n, o + 1, c, f"左括号还剩 {n - o} 个"), (")", c < o, o, c + 1, f"右括号比左括号少（{c} < {o}）")):
            if not ok:
                continue
            ch = node.add(ch_char)
            path.append(ch_char)
            pnodes.append(ch)
            if len(path) < 2 * n:
                rec.events.append((ch, pnodes[:], f"{why}，放 '{ch_char}'：{''.join(path)}。", fmt(rec.res), None))
            dfs(ch, no, nc)
            pnodes.pop()
            path.pop()

    dfs(rec.root, 0, 0)
    t = Trace("lc22", "22 括号生成 · 只走合法的分支")
    rec.play(t, "每一层放一个字符。只有两条规则：左括号没用完才能放左；右括号比左括号少才能放右。",
             "不合法的分支根本不会生成，所以每个叶子都是答案：n = 3 时 5 个（卡特兰数）。")


def lc39():
    cand, target = [2, 3, 6, 7], 7
    rec = Recorder("7")
    path, pnodes = [], [rec.root]

    def dfs(node, start, rest):
        if rest == 0:
            rec.res.append(path[:])
            rec.events.append((node, pnodes[:], f"剩余 0，得到 {fmt(path)}。", fmt(rec.res), "✓"))
            return
        for i in range(start, len(cand)):
            c = cand[i]
            if c > rest:
                rec.events.append((node, pnodes[:], f"剩余 {rest}，下一个候选 {c} > {rest}，后面的更大，这一层直接 break。", fmt(rec.res), "✗" if not node.children else None))
                break
            ch = node.add(rest - c)
            path.append(c)
            pnodes.append(ch)
            if rest - c > 0:
                rec.events.append((ch, pnodes[:], f"选 {c}，剩余 {rest - c}。下一层从 {c} 开始选（可以重复选，但不回头选更小的）。", fmt(rec.res), None))
            dfs(ch, i, rest - c)
            pnodes.pop()
            path.pop()

    dfs(rec.root, 0, target)
    t = Trace("lc39", "39 组合总和 · 结点里是剩余的目标值")
    rec.play(t, "candidates = [2, 3, 6, 7]（已排序），target = 7。结点里写的是还差多少。",
             "答案 [[2, 2, 3], [7]]。start 保证组合按非降序生成，所以 [2, 2, 3] 和 [3, 2, 2] 不会重复出现。")


def lc131():
    s = "aabb"
    rec = Recorder()
    path, pnodes = [], [rec.root]

    def pal(x):
        return x == x[::-1]

    def dfs(node, i):
        if i == len(s):
            rec.res.append(path[:])
            rec.events.append((node, pnodes[:], f"切到结尾，得到 {path}。", str(rec.res), "✓"))
            return
        for j in range(i, len(s)):
            piece = s[i:j + 1]
            if not pal(piece):
                continue
            ch = node.add(piece)
            path.append(piece)
            pnodes.append(ch)
            if j + 1 < len(s):
                rec.events.append((ch, pnodes[:], f"下一段切 \"{piece}\"（回文），剩下 \"{s[j + 1:]}\" 继续切。", str(rec.res), None))
            dfs(ch, j + 1)
            pnodes.pop()
            path.pop()

    dfs(rec.root, 0)
    t = Trace("lc131", "131 分割回文串 · 每层决定下一段切多长")
    rec.play(t, "s = \"aabb\"。每一层枚举下一段的结尾，只有回文的段才往下走（\"aab\"、\"ab\" 这些直接跳过）。",
             "4 种切法。判断回文用预处理的 pal[i][j]，每次 O(1)。")


def lc60():
    n, k = 4, 9
    t = Trace("lc60", "60 排列序列 · 逐位确定（n = 4，k = 9）")
    fact = [1, 1, 2, 6]
    digits = [1, 2, 3, 4]
    k0 = k - 1
    res = []
    t.array(digits, {}, f"k 先减 1 变成从 0 开始数：k = {k0}。第一位每换一个数，后面 3 位有 3! = 6 种排法。", extra=f"k = {k0}，结果 = \"\"")
    for i in range(n - 1, -1, -1):
        idx, k0 = divmod(k0, fact[i])
        pick = digits[idx]
        t.array(digits, {"idx": idx}, f"后面还有 {i} 位，每组 {i}! = {fact[i]} 个。商 {idx}：选剩余数里第 {idx} 个，即 {pick}；余数 {k0} 留给后面。", hl=[idx], extra=f"k = {k0}，结果 = \"{''.join(map(str, res + [pick]))}\"")
        digits.pop(idx)
        res.append(pick)
    t.array(res, {}, f"答案 \"{''.join(map(str, res))}\"。不用枚举，时间 O(n²)（列表删除是 O(n)）。", extra="")
    t.save()


def lc200():
    g = [list("11000"), list("11010"), list("00100"), list("00011")]
    m, n = len(g), len(g[0])
    tone = [[0] * n for _ in range(m)]
    t = Trace("lc200", "200 岛屿数量 · DFS 沉岛")
    t.grid(g, "扫描每个格子，遇到 '1' 就发现一个新岛，从它开始 DFS，把相连的陆地都改成 '0'（沉掉），这样不会重复计数。", tone=tone, extra="count = 0")
    count = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] != '1':
                continue
            count += 1
            order = []
            def sink(x, y):
                if not (0 <= x < m and 0 <= y < n) or g[x][y] != '1':
                    return
                g[x][y] = '0'
                tone[x][y] = count
                order.append((x, y))
                sink(x + 1, y); sink(x - 1, y); sink(x, y + 1); sink(x, y - 1)
            g_before = [r[:] for r in g]
            tone_before = [r[:] for r in tone]
            sink(i, j)
            t.grid(g_before, f"({i}, {j}) 是 '1'：第 {count} 个岛，从这里开始 DFS。", hl=[(i, j)], tone=tone_before, extra=f"count = {count}")
            t.grid(g, f"DFS 访问了 {len(order)} 个格子，都改成 '0'。按访问顺序：" + " → ".join(f"({x},{y})" for x, y in order) + "。", hl=order, tone=tone, extra=f"count = {count}")
    t.grid(g, f"扫描结束，一共 {count} 个岛。每个格子最多被访问常数次，时间 O(mn)。", tone=tone, extra=f"count = {count}")
    t.save()


def lc547():
    n = 6
    edges = [(0, 1), (2, 3), (1, 4), (3, 5), (2, 5), (0, 4)]
    parent = list(range(n))
    rank = [0] * n
    t = Trace("lc547", "547 省份数量 · 并查集（格子里是 parent）")

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    count = n
    t.array(parent, {}, "一开始每个城市自己是一个集合：parent[i] = i。省份数 = 集合数 = 6。", extra=f"rank = {rank}，省份数 = {count}")
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            t.array(parent, {"a": a, "b": b}, f"{a} 和 {b} 相连，但根都是 {ra}，已经在同一个省，不变。", hl=[a, b], extra=f"rank = {rank}，省份数 = {count}")
            continue
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        count -= 1
        t.array(parent, {"a": a, "b": b}, f"{a}、{b} 相连：根 {rb} 挂到根 {ra} 下面（按秩：矮的挂到高的下面），省份数减 1。", hl=[ra, rb], extra=f"rank = {rank}，省份数 = {count}")
    t.array(parent, {}, f"处理完所有边，答案 {count}：{{0, 1, 4}} 和 {{2, 3, 5}}。", extra=f"省份数 = {count}")
    t.save()


def lc207():
    n = 4
    pre = [[1, 0], [2, 1], [3, 2], [1, 3]]
    graph = [[] for _ in range(n)]
    for a, b in pre:
        graph[b].append(a)
    names = {0: "白", 1: "灰", 2: "黑"}
    state = [0] * n
    t = Trace("lc207", "207 课程表 · DFS 三色标记判环")
    show = lambda: [names[s] for s in state]
    edges = "边：0→1，1→2，2→3，3→1"
    t.array(show(), {}, "白 = 没访问，灰 = 在当前 DFS 路径上，黑 = 已经确认它后面没有环。走到灰色的点说明绕回来了，有环。", extra=edges)
    stack = []

    def dfs(u):
        state[u] = 1
        stack.append(u)
        t.array(show(), {"u": u}, f"进入 {u}，标灰。当前路径 {stack}。", hl=[u], extra=edges)
        for v in graph[u]:
            if state[v] == 1:
                t.array(show(), {"u": u, "v": v}, f"{u} → {v}，而 {v} 是灰色（在当前路径上）：发现环 {stack[stack.index(v):] + [v]}，返回 False。", hl=[u, v], extra=edges)
                return True
            if state[v] == 0 and dfs(v):
                return True
        state[u] = 2
        stack.pop()
        t.array(show(), {"u": u}, f"{u} 的后续都没有环，标黑。", hl=[u], extra=edges)
        return False

    dfs(0)
    t.save()


def lc210():
    n = 6
    pre = [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3], [5, 2]]
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pre:
        graph[b].append(a)
        indeg[a] += 1
    t = Trace("lc210", "210 课程表 II · Kahn（格子里是入度）")
    edges = "边：0→1，0→2，1→3，2→3，3→4，2→5"
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    t.array(indeg, {}, f"入度 = 还有几门先修课没修。入度为 0 的课可以直接修，先入队：{list(q)}。", hl=list(q), extra=f"{edges}；queue = {list(q)}，order = []")
    while q:
        u = q.popleft()
        order.append(u)
        freed = []
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
                freed.append(v)
        msg = f"修课 {u}，它的后续课 {graph[u]} 入度各减 1。" if graph[u] else f"修课 {u}，它没有后续课。"
        if freed:
            msg += f" {freed} 入度变成 0，入队。"
        t.array(indeg, {"u": u}, msg, hl=[u] + freed, extra=f"queue = {list(q)}，order = {order}")
    t.array(indeg, {}, f"队列空了，修了 {len(order)} 门 = 全部课程，没有环。拓扑序 {order}。", extra=f"order = {order}")
    t.save()


if __name__ == "__main__":
    for f in (lc46, lc47, lc22, lc39, lc131, lc60, lc200, lc547, lc207, lc210):
        f()
