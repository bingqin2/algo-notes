"""排序、二分、滑动窗口 A 层的执行过程：快排、归并、堆排序、33、704、1004、239。"""
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace, TreeNode  # noqa: E402


def quick():
    a = [5, 2, 8, 3, 9, 1, 6, 4]
    t = Trace("quick-sort", "快速排序 · Lomuto 划分（主元取最后一个）")
    t.array(a, {}, "每次划分：选一个主元，把比它小的放左边，比它大的放右边，主元就到了最终位置。再递归处理两边。")

    def partition(lo, hi):
        pivot = a[hi]
        i = lo
        t.array(a, {"i": i, "j": lo, "pivot": hi}, f"划分 [{lo}, {hi}]，主元 {pivot}。i 左边都是 < {pivot} 的数。", hl=[hi], window=(lo, hi))
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                t.array(a, {"i": i, "j": j, "pivot": hi}, f"{a[i]} < {pivot}：和 i 位置交换，i 右移。", hl=[i, j], window=(lo, hi))
                i += 1
            else:
                t.array(a, {"i": i, "j": j, "pivot": hi}, f"{a[j]} ≥ {pivot}：不动。", hl=[j], window=(lo, hi))
        a[i], a[hi] = a[hi], a[i]
        t.array(a, {"i": i}, f"主元换到 i = {i}，它左边都比它小，右边都比它大，位置定了。", hl=[i], window=(lo, hi))
        return i

    def sort(lo, hi, depth):
        if lo >= hi:
            return
        p = partition(lo, hi)
        if depth == 0:
            sort(lo, p - 1, depth + 1)
            sort(p + 1, hi, depth + 1)

    sort(0, len(a) - 1, 0)
    t.array(a, {}, "第一层划分和左右各一次划分就演示到这里，继续递归就排好了：[1, 2, 3, 4, 5, 6, 8, 9]。平均 O(n log n)，最坏 O(n²)。")
    t.save()


def merge():
    a = [5, 2, 8, 3, 9, 1, 6, 4]
    t = Trace("merge-sort", "归并排序 · 自顶向下")
    t.array(a, {}, "先把两半各自排好（递归），再把两个有序的半边合并。下面是每一次合并的结果。")
    tmp = a[:]

    def sort(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid + 1, hi)
        left, right = a[lo:mid + 1], a[mid + 1:hi + 1]
        tmp[lo:hi + 1] = a[lo:hi + 1]
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if j > hi or (i <= mid and tmp[i] <= tmp[j]):
                a[k] = tmp[i]; i += 1
            else:
                a[k] = tmp[j]; j += 1
        t.array(a, {"lo": lo, "hi": hi}, f"合并 {left} 和 {right} → {a[lo:hi + 1]}。两个指针各走一遍，O(长度)。", hl=list(range(lo, hi + 1)), window=(lo, hi))

    sort(0, len(a) - 1)
    t.array(a, {}, "一共 log n 层，每层合并总共 O(n)，所以 O(n log n)，且任何输入都一样。需要 O(n) 的辅助数组。")
    t.save()


def heap():
    a = [4, 10, 3, 5, 1, 8]
    t = Trace("heap-sort", "堆排序 · 大顶堆（数组下标 i 的孩子是 2i+1、2i+2）")
    n = len(a)

    def tree(size):
        nodes = [TreeNode(v) for v in a]
        for i in range(n):
            for c, side in ((2 * i + 1, "left"), (2 * i + 2, "right")):
                if c < n:
                    setattr(nodes[i], side, nodes[c])
        return nodes

    def frame(size, note, hl=()):
        nodes = tree(size)
        t.tree(nodes[0], {}, note, hl=[nodes[i] for i in hl], dim=nodes[size:], extra=f"数组 = {a}")

    frame(n, "数组本身就是一棵完全二叉树。先建大顶堆：从最后一个非叶子结点（下标 n/2-1 = 2）开始，往前逐个下沉。")

    def sift(i, size, phase):
        while True:
            big, l, r = i, 2 * i + 1, 2 * i + 2
            if l < size and a[l] > a[big]:
                big = l
            if r < size and a[r] > a[big]:
                big = r
            if big == i:
                return
            a[i], a[big] = a[big], a[i]
            frame(size, f"{phase}：{a[big]} 比孩子 {a[i]} 小，交换，继续往下沉。", hl=[i, big])
            i = big

    for i in range(n // 2 - 1, -1, -1):
        sift(i, n, f"建堆，下沉下标 {i}")
    frame(n, f"建堆完成，堆顶 {a[0]} 是最大值。", hl=[0])
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        frame(end, f"把堆顶 {a[end]} 换到末尾（下标 {end}），它已经排好，变灰。堆的大小减 1。", hl=[0, end])
        sift(0, end, "堆顶下沉")
    frame(0, f"排好了：{a}。建堆 O(n)，n 次下沉各 O(log n)，原地、不稳定。")
    t.save()


def lc33():
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 1
    t = Trace("lc33", "33 搜索旋转排序数组 · 找 1")
    lo, hi = 0, len(nums) - 1
    t.array(nums, {"lo": lo, "hi": hi}, "旋转过的数组从 mid 切开，两半里至少有一半是有序的。先判断哪一半有序，再看 target 在不在这一半。", window=(lo, hi))
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            t.array(nums, {"lo": lo, "mid": mid, "hi": hi}, f"nums[{mid}] = {target}，找到了。", hl=[mid], window=(lo, hi))
            break
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                msg = f"nums[lo] = {nums[lo]} ≤ nums[mid] = {nums[mid]}：左半边有序，{target} 在 [{nums[lo]}, {nums[mid]}) 里，去左边。"
                nlo, nhi = lo, mid - 1
            else:
                msg = f"nums[lo] = {nums[lo]} ≤ nums[mid] = {nums[mid]}：左半边有序，但 {target} 不在 [{nums[lo]}, {nums[mid]}) 里，去右边。"
                nlo, nhi = mid + 1, hi
        else:
            if nums[mid] < target <= nums[hi]:
                msg = f"nums[lo] > nums[mid]：右半边有序，{target} 在 ({nums[mid]}, {nums[hi]}] 里，去右边。"
                nlo, nhi = mid + 1, hi
            else:
                msg = f"nums[lo] > nums[mid]：右半边有序，但 {target} 不在 ({nums[mid]}, {nums[hi]}] 里，去左边。"
                nlo, nhi = lo, mid - 1
        t.array(nums, {"lo": lo, "mid": mid, "hi": hi}, msg, hl=[mid], window=(lo, hi))
        lo, hi = nlo, nhi
    t.save()


def lc704():
    nums = [1, 3, 3, 3, 5, 8, 9]
    target = 3
    t = Trace("lc704", "704 二分查找 · lower_bound 找第一个 ≥ 3")
    lo, hi = 0, len(nums)
    t.array(nums, {"lo": lo, "hi": hi}, "左闭右开 [lo, hi)，hi 从 n 开始。不变式：lo 左边都 < 3，hi 及右边都 ≥ 3。", window=(lo, hi - 1))
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            t.array(nums, {"lo": lo, "mid": mid, "hi": hi}, f"nums[{mid}] = {nums[mid]} < 3：答案在 mid 右边，lo = mid + 1。", hl=[mid], window=(lo, hi - 1))
            lo = mid + 1
        else:
            t.array(nums, {"lo": lo, "mid": mid, "hi": hi}, f"nums[{mid}] = {nums[mid]} ≥ 3：mid 可能就是答案，hi = mid（不能减 1）。", hl=[mid], window=(lo, hi - 1))
            hi = mid
    t.array(nums, {"lo": lo, "hi": hi}, f"lo == hi = {lo}，区间空了。第一个 3 在下标 {lo}；upper_bound 是 4，所以 3 出现了 4 - 1 = 3 次。", hl=[lo])
    t.save()


def lc1004():
    nums = [1, 1, 0, 0, 1, 1, 1, 0, 1, 0]
    k = 2
    t = Trace("lc1004", "1004 最大连续 1 的个数 III · k = 2")
    best = left = zeros = 0
    t.array(nums, {}, "换个说法：找最长的子数组，里面 0 的个数不超过 k。右边界一直往右扩，0 多了就收缩左边界。", extra="zeros = 0，best = 0")
    for right, x in enumerate(nums):
        zeros += x == 0
        moved = left
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)
        msg = f"加入 nums[{right}] = {x}。"
        if left != moved:
            msg += f" 0 超过 {k} 个，左边界从 {moved} 收缩到 {left}。"
        msg += f" 窗口长度 {right - left + 1}。"
        t.array(nums, {"L": left, "R": right}, msg, hl=[right], window=(left, right), extra=f"zeros = {zeros}，best = {best}")
    t.array(nums, {}, f"答案 {best}。每个元素最多进出窗口一次，O(n)。", extra=f"best = {best}")
    t.save()


def lc239():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    t = Trace("lc239", "239 滑动窗口最大值 · 单调递减队列（k = 3）")
    q = deque()
    res = []
    t.array(nums, {}, "队列里存下标，对应的值从队头到队尾递减。队头就是当前窗口的最大值。", extra="队列 = []，res = []")
    for i, x in enumerate(nums):
        popped = []
        while q and nums[q[-1]] <= x:
            popped.append(nums[q.pop()])
        q.append(i)
        msg = f"加入 {x}。"
        if popped:
            msg += f" 从队尾弹出比它小的 {popped}：它们比 {x} 早离开窗口又比 {x} 小，不可能再是最大值。"
        if q[0] <= i - k:
            msg += f" 队头下标 {q[0]} 已经滑出窗口，弹出。"
            q.popleft()
        if i >= k - 1:
            res.append(nums[q[0]])
            msg += f" 窗口最大值 = 队头 {nums[q[0]]}。"
        t.array(nums, {"i": i}, msg, hl=list(q), window=(max(0, i - k + 1), i), extra=f"队列 = {[nums[j] for j in q]}，res = {res}")
    t.save()


if __name__ == "__main__":
    for f in (quick, merge, heap, lc33, lc704, lc1004, lc239):
        f()
