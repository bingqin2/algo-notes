"""B 层：链表、栈、堆、前缀和里带图解的题：148、84、295、560。"""
import heapq
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc148():
    a = [4, 2, 1, 3, 8, 5, 7, 6]
    n = len(a)
    t = Trace("lc148", "148 排序链表 · 自底向上归并（格子是链表当前的顺序）")
    t.array(a, {}, "不用递归：先把相邻的长度为 1 的两段合并，再合并长度为 2 的，再 4 的……每轮扫一遍链表。只用几个指针，O(1) 额外空间。", extra="step = 1")
    step = 1
    while step < n:
        for lo in range(0, n, 2 * step):
            mid, hi = min(lo + step, n), min(lo + 2 * step, n)
            left, right = a[lo:mid], a[mid:hi]
            a[lo:hi] = sorted(a[lo:hi])
            t.array(a, {}, f"step = {step}：切下两段 {left} 和 {right}，合并成 {a[lo:hi]}，接到已处理部分的末尾。", hl=list(range(lo, hi)), window=(lo, hi - 1), extra=f"step = {step}")
        step *= 2
    t.array(a, {}, f"step 到 {step} ≥ n，排好了。一共 log n 轮，每轮 O(n)，总 O(n log n)。", extra="")
    t.save()


def lc84():
    heights = [2, 1, 5, 6, 2, 3]
    h = [0] + heights + [0]
    t = Trace("lc84", "84 柱状图中最大的矩形 · 单调递增栈 + 左右哨兵")
    stack, best = [], 0
    t.array(h, {}, "两端各加一个高度 0 的哨兵。栈里存下标，高度单调递增。一个柱子被弹出时，它向左、向右能延伸的边界就都确定了。", extra="栈 = []，best = 0")
    for i, x in enumerate(h):
        while stack and h[stack[-1]] > x:
            j = stack.pop()
            width = i - stack[-1] - 1
            area = h[j] * width
            best = max(best, area)
            t.array(h, {"i": i, "弹出": j}, f"h[{i}] = {x} < 栈顶高度 {h[j]}：弹出 {j}。以 {h[j]} 为高，右边界是 {i}（第一个更矮的），左边界是新栈顶 {stack[-1]}，宽 {width}，面积 {area}。", hl=[j], window=(stack[-1] + 1, i - 1), extra=f"栈 = {stack}，best = {best}")
        stack.append(i)
        if i < len(h) - 1:
            t.array(h, {"i": i}, f"h[{i}] = {x} 入栈，栈保持递增。", hl=[i], extra=f"栈 = {stack}，best = {best}")
    t.array(h, {}, f"最右边的哨兵 0 把所有柱子都弹出了。答案 {best}。每个下标进出栈一次，O(n)。", extra=f"best = {best}")
    t.save()


def lc295():
    t = Trace("lc295", "295 数据流的中位数 · 两个堆（左：较小一半的大顶堆，右：较大一半的小顶堆）")
    small, large = [], []
    stream = [5, 2, 8, 1, 9, 3]

    def cells():
        left = sorted(-x for x in small)
        right = sorted(large)
        return left + ["|"] + right

    def med():
        return -small[0] if len(small) > len(large) else (-small[0] + large[0]) / 2

    t.array(["|"], {}, "两个堆把数据分成两半：small 存较小的一半（大顶堆，堆顶是这一半的最大值），large 存较大的一半（小顶堆）。保持 small 的个数等于 large 或多一个。中位数只看两个堆顶。", extra="")
    for x in stream:
        heapq.heappush(small, -x)
        moved = -heapq.heappop(small)
        heapq.heappush(large, moved)
        extra = ""
        if len(large) > len(small):
            back = heapq.heappop(large)
            heapq.heappush(small, -back)
            extra = f"，large 比 small 多了，把 large 的最小值 {back} 移回 small"
        c = cells()
        bar = c.index("|")
        t.array(c, {}, f"加入 {x}：先放进 small，再把 small 的最大值 {moved} 移到 large（保证左边都 ≤ 右边）{extra}。中位数 = {med()}。", hl=[bar - 1] + ([bar + 1] if len(small) == len(large) else []), extra=f"small 堆顶 {-small[0]}，large 堆顶 {large[0] if large else '空'}")
    t.array(cells(), {}, "addNum 是 O(log n)，findMedian 是 O(1)。格子里为了好看排了序，堆里实际不是有序的，只保证堆顶。")
    t.save()


def lc560():
    nums, k = [1, 2, -1, 3, -2, 2, 1], 3
    t = Trace("lc560", "560 和为 K 的子数组 · 前缀和 + 哈希表计数（k = 3）")
    count = Counter({0: 1})
    s = res = 0
    fmt = lambda: "{" + ", ".join(f"{a}: {b}" for a, b in sorted(count.items())) + "}"
    t.array(nums, {}, "子数组 (j, i] 的和 = s_i − s_j。以 i 结尾、和为 k 的子数组个数 = 之前出现过几次前缀和 s_i − k。哈希表记录每个前缀和出现的次数，空前缀记为 {0: 1}。", extra=f"s = 0，res = 0，count = {fmt()}")
    for i, x in enumerate(nums):
        s += x
        add = count[s - k]
        res += add
        msg = f"加 {x}，s = {s}。找 s − k = {s - k}：出现过 {add} 次" + (f"，有 {add} 个以下标 {i} 结尾的子数组和为 {k}。" if add else "。")
        count[s] += 1
        t.array(nums, {"i": i}, msg + f" 然后 count[{s}] + 1。", hl=[i], extra=f"s = {s}，res = {res}，count = {fmt()}")
    t.array(nums, {}, f"答案 {res}。有负数时窗口不单调，滑动窗口不能用，前缀和 + 哈希表 O(n)。", extra=f"res = {res}")
    t.save()


if __name__ == "__main__":
    for f in (lc148, lc84, lc295, lc560):
        f()
