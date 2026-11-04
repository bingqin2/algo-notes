"""C 层带图解的题（第一部分）：69、160、1、226。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace, TreeNode  # noqa: E402


def lc69():
    x = 20
    cells = list(range(x + 1))
    t = Trace("lc69", "69 x 的平方根 · 对答案二分（x = 20）")
    lo, hi = 0, x
    t.array(cells, {"lo": lo, "hi": hi}, "答案 m 满足 m² ≤ x 且 (m+1)² > x，也就是「最后一个平方不超过 x 的数」。在 [0, x] 上二分。", window=(lo, hi))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            t.array(cells, {"lo": lo, "mid": mid, "hi": hi}, f"{mid}² = {mid * mid} ≤ {x}：{mid} 可能是答案，lo = mid。mid 用上取整，否则 lo、hi 相邻时会死循环。", hl=[mid], window=(lo, hi))
            lo = mid
        else:
            t.array(cells, {"lo": lo, "mid": mid, "hi": hi}, f"{mid}² = {mid * mid} > {x}：太大，hi = mid − 1。", hl=[mid], window=(lo, hi))
            hi = mid - 1
    r, steps = x, []
    while r * r > x:
        r = (r + x // r) // 2
        steps.append(r)
    t.array(cells, {"lo": lo}, f"答案 {lo}，O(log x)。牛顿迭代 r = (r + x / r) / 2 从 {x} 开始：{' → '.join(map(str, steps))}，收敛更快。", hl=[lo])
    t.save()


def lc160():
    a, b, common = ["a1", "a2"], ["b1", "b2", "b3"], ["c1", "c2"]
    pa = a + common + ["∅"] + b + common
    pb = b + common + ["∅"] + a + common
    n = max(len(pa), len(pb))
    pa += [""] * (n - len(pa))
    pb += [""] * (n - len(pb))
    t = Trace("lc160", "160 相交链表 · 两个指针都走 A + B")
    t.grid([pa, pb], "第一行是指针 a 走过的路：A 走完接着走 B；第二行是指针 b：B 走完接着走 A。∅ 也算一步。a 走 2 + 2 + 1 + 3 = 8 步、b 走 3 + 2 + 1 + 2 = 8 步，在第 8 步同时到达 c1。", tone=[[1 if x in common else 0 for x in pa], [1 if x in common else 0 for x in pb]])
    for step in range(n):
        x, y = pa[step], pb[step]
        hit = x == y and x in common
        msg = f"第 {step} 步：a 在 {x}，b 在 {y}。" + ("两个指针指向同一个结点，就是交点。" if hit else ("走到链表末尾（∅）后跳到另一条链表的头。" if "∅" in (x, y) else ""))
        t.grid([pa, pb], msg, hl=[(0, step), (1, step)], tone=[[1 if v in common else 0 for v in pa], [1 if v in common else 0 for v in pb]])
        if hit:
            break
    t.grid([pa, pb], "原理：a 走了 A 独有 + 公共 + B 独有，b 走了 B 独有 + 公共 + A 独有，长度相等，所以同时到达交点。不相交时同时走到 ∅。O(m + n) 时间，O(1) 空间。")
    t.save()


def lc1():
    nums, target = [3, 8, 11, 2, 7, 15], 9
    t = Trace("lc1", "1 两数之和 · 哈希表一次遍历（target = 9）")
    seen = {}
    t.array(nums, {}, "边遍历边查：对每个 x，看 target − x 之前有没有出现过。先查再放，保证不会用到自己。", extra="seen = {}")
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            t.array(nums, {"i": i}, f"x = {x}，需要 {need}：在 seen 里，下标 {seen[need]}。答案 [{seen[need]}, {i}]。", hl=[seen[need], i], extra=f"seen = {seen}")
            break
        seen[x] = i
        t.array(nums, {"i": i}, f"x = {x}，需要 {need}：还没出现过。把 {x} → {i} 放进 seen。", hl=[i], extra=f"seen = {seen}")
    t.array(nums, {}, "一次遍历，O(n) 时间，O(n) 空间。有序数组可以用双指针 O(1) 空间（167 题）。")
    t.save()


def lc226():
    root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
    t = Trace("lc226", "226 翻转二叉树 · 后序：先翻转左右子树，再交换")
    t.tree(root, {}, "递归：翻转左子树、翻转右子树，然后交换当前结点的左右孩子。前序（先交换再递归）也可以。")

    def flip(node):
        if not node:
            return None
        flip(node.left)
        flip(node.right)
        node.left, node.right = node.right, node.left
        if node.left or node.right:
            t.tree(root, {"node": node}, f"结点 {node.val} 的两棵子树已经翻转好了，交换它的左右孩子。", hl=[node])
        return node

    flip(root)
    t.tree(root, {}, "每个结点访问一次，O(n) 时间，O(h) 递归栈。")
    t.save()


if __name__ == "__main__":
    for f in (lc69, lc160, lc1, lc226):
        f()
