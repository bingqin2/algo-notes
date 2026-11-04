"""二叉树 A 层题的执行过程：102、124、236、230。"""
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace, build_tree  # noqa: E402


def lc102():
    root = build_tree([3, 9, 20, 4, None, 15, 7])
    t = Trace("lc102", "102 层序遍历 · BFS 按层")
    q, res = deque([root]), []
    t.tree(root, {"队首": root}, "队列里先放根结点。关键：每一轮开始时，队列里恰好是完整的一层。", hl=[root], extra="queue = [3]，res = []")
    seen = {root}
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            for ch in (node.left, node.right):
                if ch:
                    q.append(ch)
                    seen.add(ch)
        res.append(level)
        t.tree(root, {}, f"一次弹出这一层的 {size} 个结点，记录 {level}，同时把它们的孩子入队。", hl=[n for n in q], extra=f"queue = {[n.val for n in q]}，res = {res}")
    t.tree(root, {}, f"队列空了，结束。结果 {res}。右视图（199）就是每层的最后一个：{[l[-1] for l in res]}。", extra=f"res = {res}")
    t.save()


def lc124():
    root = build_tree([-10, 9, 20, None, None, 15, 7])
    t = Trace("lc124", "124 二叉树中的最大路径和 · 后序")
    marks, best = {}, [float("-inf")]
    t.tree(root, {}, "后序遍历：先算左右孩子能提供的单边最大贡献，再算经过当前结点的路径。结点上方显示它返回的贡献值。")

    def gain(node):
        if not node:
            return 0
        l = max(gain(node.left), 0)
        r = max(gain(node.right), 0)
        through = node.val + l + r
        best[0] = max(best[0], through)
        g = node.val + max(l, r)
        marks[node] = f"↑{g}"
        t.tree(root, {"node": node}, f"结点 {node.val}：左贡献 {l}，右贡献 {r}。以它为最高点的路径和 = {node.val} + {l} + {r} = {through}；往上只能带一边，返回 {g}。", hl=[node], marks=dict(marks), extra=f"best = {best[0]}")
        return g

    gain(root)
    t.tree(root, {}, f"答案 {best[0]}：路径 15 → 20 → 7，不经过根。根结点 -10 的贡献是负数，它的父结点（如果有）不会要它。", marks=dict(marks), extra=f"best = {best[0]}")
    t.save()


def lc236():
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p, q = root.left.left, root.left.right.right   # 6 和 4
    t = Trace("lc236", "236 最近公共祖先 · p = 6，q = 4")
    marks = {}
    t.tree(root, {"p": p, "q": q}, "后序递归：每个结点返回「在我这棵子树里找到的 p 或 q 或答案」，没有就返回空。", hl=[p, q])

    def go(node):
        if not node:
            return None
        if node is p or node is q:
            marks[node] = f"返回{node.val}"
            t.tree(root, {"p": p, "q": q, "node": node}, f"{node.val} 就是要找的结点，直接返回它（不用再往下找）。", hl=[node], marks=dict(marks))
            return node
        left, right = go(node.left), go(node.right)
        if left and right:
            res, msg = node, f"左边找到 {left.val}，右边找到 {right.val}：p、q 分在两边，{node.val} 就是最近公共祖先。"
        else:
            res = left or right
            msg = f"结点 {node.val}：左边返回 {left.val if left else '空'}，右边返回 {right.val if right else '空'}，把非空的那个往上传。"
        marks[node] = f"返回{res.val}" if res else "空"
        t.tree(root, {"p": p, "q": q, "node": node}, msg, hl=[node], marks=dict(marks))
        return res

    ans = go(root)
    t.tree(root, {"答案": ans}, f"根结点最终返回 {ans.val}，它就是 6 和 4 的最近公共祖先。", hl=[ans], marks=dict(marks))
    t.save()


def lc230():
    root = build_tree([5, 3, 6, 2, 4, None, None, 1])
    k = 3
    t = Trace("lc230", "230 二叉搜索树中第 K 小的元素 · k = 3")
    stack, node, cnt, visited = [], root, 0, []
    t.tree(root, {"node": node}, "BST 的中序遍历是升序。用栈模拟中序，数到第 k 个就停，不用遍历整棵树。", extra="stack = []")
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        t.tree(root, {"栈顶": stack[-1]}, "一路往左走到底，沿途结点入栈。", hl=list(stack), extra=f"stack = {[n.val for n in stack]}")
        node = stack.pop()
        cnt += 1
        visited.append(node)
        if cnt == k:
            t.tree(root, {"答案": node}, f"弹出 {node.val}，这是第 {cnt} 小的，返回。剩下的结点不用再看。", hl=[node], marks={n: f"#{i+1}" for i, n in enumerate(visited)}, extra=f"stack = {[n.val for n in stack]}")
            break
        t.tree(root, {"node": node}, f"弹出 {node.val}，是第 {cnt} 小的。接着转向它的右子树。", hl=[node], marks={n: f"#{i+1}" for i, n in enumerate(visited)}, extra=f"stack = {[n.val for n in stack]}")
        node = node.right
    t.save()


if __name__ == "__main__":
    lc102(); lc124(); lc236(); lc230()
