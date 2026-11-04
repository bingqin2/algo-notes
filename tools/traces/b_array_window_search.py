"""B 层：排序、数组、滑动窗口、二分里带图解的题：215、15、42、438、76、4。"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc215():
    nums, k = [3, 2, 1, 5, 6, 4, 9, 7], 3
    target = len(nums) - k
    t = Trace("lc215", "215 第 K 个最大元素 · 快速选择（k = 3）")
    t.array(nums, {}, f"第 3 大 = 升序排好后下标 n − k = {target} 的数。快速选择：划分一次后，只需要去目标下标所在的那一边继续，另一边不用管。")
    lo, hi = 0, len(nums) - 1
    pivots = [4, 7]                        # 为了演示固定主元（代码里是随机的）
    while True:
        pivot = pivots.pop(0) if pivots else nums[lo]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]; lt += 1; i += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]; gt -= 1
            else:
                i += 1
        if target < lt:
            side, nlo, nhi = f"目标下标 {target} < {lt}，去左边 [{lo}, {lt - 1}]", lo, lt - 1
        elif target > gt:
            side, nlo, nhi = f"目标下标 {target} > {gt}，去右边 [{gt + 1}, {hi}]", gt + 1, hi
        else:
            t.array(nums, {"lt": lt, "gt": gt}, f"以 {pivot} 划分 [{lo}, {hi}]：等于 {pivot} 的在 [{lt}, {gt}]，正好包含目标下标 {target}，答案就是 {pivot}。", hl=list(range(lt, gt + 1)), window=(lo, hi))
            break
        t.array(nums, {"lt": lt, "gt": gt}, f"以 {pivot} 划分 [{lo}, {hi}]：左边都 < {pivot}，右边都 > {pivot}。{side}。", hl=list(range(lt, gt + 1)), window=(lo, hi))
        lo, hi = nlo, nhi
    t.array(nums, {}, "每次只进入一边，期望 n + n/2 + n/4 + … = O(n)。主元要随机选，否则有序数组会退化成 O(n²)。")
    t.save()


def lc15():
    nums = sorted([-1, 0, 1, 2, -1, -4, -1])
    t = Trace("lc15", "15 三数之和 · 排序 + 固定一个 + 左右指针")
    res = []
    t.array(nums, {}, "先排序。固定 nums[i]，在它右边用左右指针找两个数，和为 −nums[i]。", extra="res = []")
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:
            t.array(nums, {"i": i}, f"nums[{i}] = {nums[i]} > 0，后面的数都更大，不可能和为 0，结束。", hl=[i], extra=f"res = {res}")
            break
        if i > 0 and nums[i] == nums[i - 1]:
            t.array(nums, {"i": i}, f"nums[{i}] 和前一个相同，跳过（去重 1）。", hl=[i], extra=f"res = {res}")
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                t.array(nums, {"i": i, "l": l, "r": r}, f"{nums[i]} + {nums[l]} + {nums[r]} = {s} < 0，l 右移。", hl=[i, l, r], window=(l, r), extra=f"res = {res}")
                l += 1
            elif s > 0:
                t.array(nums, {"i": i, "l": l, "r": r}, f"和 = {s} > 0，r 左移。", hl=[i, l, r], window=(l, r), extra=f"res = {res}")
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                ol, orr = l, r
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                skip = "，跳过和它们相同的值（去重 2、3）" if (l, r) != (ol, orr) else ""
                t.array(nums, {"i": i, "l": ol, "r": orr}, f"和为 0，记录 [{nums[i]}, {nums[ol]}, {nums[orr]}]{skip}，两个指针都向内移。", hl=[i, ol, orr], window=(ol, orr), extra=f"res = {res}")
                l += 1
                r -= 1
    t.array(nums, {}, f"结果 {res}。排序 O(n log n)，外层 n 次 × 双指针 O(n) = O(n²)。", extra=f"res = {res}")
    t.save()


def lc42():
    h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    t = Trace("lc42", "42 接雨水 · 双指针")
    l, r = 0, len(h) - 1
    lmax = rmax = res = 0
    t.array(h, {"l": l, "r": r}, "每个位置的水位 = min(左边最高, 右边最高)。双指针：哪边的最高值更小，哪边的水位就已经确定了。", extra="lmax = 0，rmax = 0，水 = 0")
    while l < r:
        lmax = max(lmax, h[l])
        rmax = max(rmax, h[r])
        if lmax < rmax:
            w = lmax - h[l]
            res += w
            t.array(h, {"l": l, "r": r}, f"lmax = {lmax} < rmax = {rmax}：右边一定有比 lmax 高的墙，l 处水位就是 lmax，存水 {lmax} − {h[l]} = {w}。l 右移。", hl=[l], extra=f"lmax = {lmax}，rmax = {rmax}，水 = {res}")
            l += 1
        else:
            w = rmax - h[r]
            res += w
            t.array(h, {"l": l, "r": r}, f"lmax = {lmax} ≥ rmax = {rmax}：r 处水位就是 rmax，存水 {rmax} − {h[r]} = {w}。r 左移。", hl=[r], extra=f"lmax = {lmax}，rmax = {rmax}，水 = {res}")
            r -= 1
    t.array(h, {}, f"两指针相遇，一共 {res}。O(n) 时间，O(1) 空间。", extra=f"水 = {res}")
    t.save()


def lc438():
    s, p = "cbaebabacd", "abc"
    m = len(p)
    need = Counter(p)
    t = Trace("lc438", "438 找到字符串中所有字母异位词 · 固定长度窗口")
    res = []
    t.array(list(s), {}, f"窗口长度固定为 {m}。每右移一格，进来一个字符、出去一个字符，比较窗口里的计数和 p 的计数。", extra=f"need = {dict(sorted(need.items()))}")
    win = Counter()
    for i, ch in enumerate(s):
        win[ch] += 1
        out = ""
        if i >= m:
            win[s[i - m]] -= 1
            out = f"，移出 '{s[i - m]}'"
        if i >= m - 1:
            ok = all(win[c] == need[c] for c in set(win) | set(need))
            if ok:
                res.append(i - m + 1)
            cnt = {c: v for c, v in sorted(win.items()) if v}
            t.array(list(s), {"i": i}, f"加入 '{ch}'{out}。窗口 {cnt}" + (f"，和 p 一样，记录起点 {i - m + 1}。" if ok else "，不一样。"), hl=[i], window=(i - m + 1, i), extra=f"res = {res}")
    t.array(list(s), {}, f"结果 {res}。计数数组只有 26 位，比较是 O(26)，总共 O(26n)。", extra=f"res = {res}")
    t.save()


def lc76():
    s, tt = "ADOBECODEBANC", "ABC"
    need = Counter(tt)
    t = Trace("lc76", "76 最小覆盖子串 · need / window + valid")
    window = Counter()
    valid = left = 0
    best, start = float("inf"), 0
    t.array(list(s), {}, "right 一直扩张；valid 记录有几种字符的数量已经够了。valid 等于需要的种类数时，窗口已经覆盖 t，开始收缩 left 找更短的。", extra="need = {A:1, B:1, C:1}，valid = 0")
    for right, ch in enumerate(s):
        if ch in need:
            window[ch] += 1
            if window[ch] == need[ch]:
                valid += 1
        if valid < len(need):
            t.array(list(s), {"L": left, "R": right}, f"加入 '{ch}'，valid = {valid}，还没覆盖。", hl=[right], window=(left, right), extra=f"valid = {valid}，最短 = {'无' if best == float('inf') else s[start:start + best]}")
            continue
        while valid == len(need):
            if right - left + 1 < best:
                start, best = left, right - left + 1
            d = s[left]
            t.array(list(s), {"L": left, "R": right}, f"覆盖了 t，窗口 \"{s[left:right + 1]}\" 长 {right - left + 1}，更新最短。尝试移出 '{d}'。", hl=[left], window=(left, right), extra=f"valid = {valid}，最短 = {s[start:start + best]}")
            left += 1
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    t.array(list(s), {}, f"答案 \"{s[start:start + best]}\"。每个字符最多进出窗口一次，O(|s| + |t|)。", window=(start, start + best - 1), extra=f"最短 = {s[start:start + best]}")
    t.save()


def lc4():
    a, b = [1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    t = Trace("lc4", "4 两个正序数组的中位数 · 在短数组上二分划分点")
    cells = lambda i, j: [f"{x}" for x in a[:i]] + ["|"] + [f"{x}" for x in a[i:]] + ["‖"] + [f"{x}" for x in b[:j]] + ["|"] + [f"{x}" for x in b[j:]]
    t.array(a + ["‖"] + b, {}, f"在 nums1（左段）取 i 个、nums2（右段）取 j = {half} − i 个，组成「左半部分」。要找的 i 满足：左半部分最大值 ≤ 右半部分最小值。", extra=f"m = {m}，n = {n}，左半部分共 {half} 个")
    lo, hi = 0, m
    INF = float("inf")
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        l1 = a[i - 1] if i else -INF
        r1 = a[i] if i < m else INF
        l2 = b[j - 1] if j else -INF
        r2 = b[j] if j < n else INF
        c = cells(i, j)
        if l1 > r2:
            msg = f"i = {i}，j = {j}：nums1 左边最大 {l1} > nums2 右边最小 {r2}，nums1 取多了，hi = i − 1。"
            hi = i - 1
        elif l2 > r1:
            msg = f"i = {i}，j = {j}：nums2 左边最大 {l2} > nums1 右边最小 {r1}，nums1 取少了，lo = i + 1。"
            lo = i + 1
        else:
            ans = max(l1, l2) if (m + n) % 2 else (max(l1, l2) + min(r1, r2)) / 2
            msg = f"i = {i}，j = {j}：{l1} ≤ {r2} 且 {l2} ≤ {r1}，划分正确。总数 {m + n} 是奇数，中位数 = 左半部分最大值 max({l1}, {l2}) = {ans}。"
            t.array(c, {}, msg, extra=f"lo = {lo}，hi = {hi}")
            break
        t.array(c, {}, msg, extra=f"lo = {lo}，hi = {hi}")
    t.array(c, {}, "每次二分只在短数组上进行，O(log min(m, n))。「|」是划分位置，「‖」分隔两个数组。")
    t.save()


if __name__ == "__main__":
    for f in (lc215, lc15, lc42, lc438, lc76, lc4):
        f()
