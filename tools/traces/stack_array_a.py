"""栈、数组双指针 A 层题的执行过程：20、32、224、394、739、11、31、88。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def show(st):
    return "[" + ", ".join(map(str, st)) + "]"


def lc20():
    s = "{[()]}(]"
    t = Trace("lc20", "20 有效的括号 · 栈")
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    t.array(s, {}, "左括号入栈；右括号必须和栈顶的左括号配对。", extra="栈（底 → 顶）= []")
    for i, c in enumerate(s):
        if c in pair:
            if st and st[-1] == pair[c]:
                st.pop()
                t.array(s, {"i": i}, f"'{c}' 和栈顶 '{pair[c]}' 配对，弹出。", hl=[i], extra=f"栈 = {show(st)}")
            else:
                top = st[-1] if st else "空"
                t.array(s, {"i": i}, f"'{c}' 需要 '{pair[c]}'，但栈顶是 '{top}'，不合法，返回 False。", hl=[i], extra=f"栈 = {show(st)}")
                break
        else:
            st.append(c)
            t.array(s, {"i": i}, f"'{c}' 是左括号，入栈。", hl=[i], extra=f"栈 = {show(st)}")
    t.save()


def lc32():
    s = ")()(())("
    t = Trace("lc32", "32 最长有效括号 · 栈存下标")
    st = [-1]
    best = 0
    t.array(s, {}, "栈底先放 -1，表示「最后一个没被匹配的右括号」的位置，作为计算长度的起点。", extra="栈 = [-1]，best = 0")
    for i, c in enumerate(s):
        if c == '(':
            st.append(i)
            t.array(s, {"i": i}, f"'(' 入栈下标 {i}。", hl=[i], extra=f"栈 = {show(st)}，best = {best}")
        else:
            st.pop()
            if not st:
                st.append(i)
                t.array(s, {"i": i}, f"弹出后栈空：这个 ')' 没人配对，把 {i} 压进去作为新的起点。", hl=[i], extra=f"栈 = {show(st)}，best = {best}")
            else:
                length = i - st[-1]
                best = max(best, length)
                t.array(s, {"i": i}, f"配对成功。有效串从栈顶 {st[-1]} 的后一位到 {i}，长度 {i} - {st[-1]} = {length}。", hl=[i], window=(st[-1] + 1, i), extra=f"栈 = {show(st)}，best = {best}")
    t.array(s, {}, f"答案 {best}：\"()(())\"。", window=(1, 6), extra=f"best = {best}")
    t.save()


def lc224():
    s = "1-(2+3)+4"
    t = Trace("lc224", "224 基本计算器 · 遇到 ( 把外层状态压栈")
    st = []
    res, num, sign = 0, 0, 1
    def ex():
        return f"res = {res}，sign = {'+' if sign > 0 else '-'}，num = {num}，栈 = {show(st)}"
    t.array(s, {}, "res 是当前这一层已经算出的结果，sign 是下一个数的符号。", extra=ex())
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
            msg = f"读数字，num = {num}。"
        elif c in '+-':
            res += sign * num
            num, sign = 0, (1 if c == '+' else -1)
            msg = f"遇到 '{c}'：把前一个数加进 res，下一个数的符号是 {c}。"
        elif c == '(':
            st.append((res, sign))
            res, sign = 0, 1
            msg = "遇到 '('：把外层的 (res, sign) 压栈，括号里从 0 开始算。"
        else:
            res += sign * num
            num = 0
            prev, ps = st.pop()
            inner = res
            res = prev + ps * res
            msg = f"遇到 ')'：括号里算完是 {inner}，弹出外层 ({prev}, {'+' if ps > 0 else '-'})，res = {prev} {'+' if ps > 0 else '-'} {inner} = {res}。"
        t.array(s, {"i": i}, msg, hl=[i], extra=ex())
    t.array(s, {}, f"结尾再加上最后一个数：{res} + {sign * num} = {res + sign * num}。", extra=f"答案 = {res + sign * num}")
    t.save()


def lc394():
    s = "3[a2[c]]"
    t = Trace("lc394", "394 字符串解码 · 栈存 (之前的串, 次数)")
    st = []
    cur, k = "", 0
    def ex():
        return f"cur = \"{cur}\"，k = {k}，栈 = [" + ", ".join(f"(\"{a}\", {b})" for a, b in st) + "]"
    t.array(s, {}, "cur 是当前这层正在拼的字符串，k 是正在读的次数。", extra=ex())
    for i, c in enumerate(s):
        if c.isdigit():
            k = k * 10 + int(c)
            msg = f"读次数，k = {k}。"
        elif c == '[':
            st.append((cur, k))
            msg = f"遇到 '['：把 (\"{cur}\", {k}) 压栈，进入里层，cur 和 k 清空。"
            cur, k = "", 0
        elif c == ']':
            prev, times = st.pop()
            msg = f"遇到 ']'：弹出 (\"{prev}\", {times})，cur = \"{prev}\" + \"{cur}\" × {times}。"
            cur = prev + cur * times
        else:
            cur += c
            msg = f"字母直接接到 cur 后面。"
        t.array(s, {"i": i}, msg, hl=[i], extra=ex())
    t.array(s, {}, f"答案 \"{cur}\"。", extra=f"答案 = \"{cur}\"")
    t.save()


def lc739():
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    t = Trace("lc739", "739 每日温度 · 单调递减栈")
    ans = [0] * len(temps)
    st = []
    t.array(temps, {}, "栈里存还没找到更高温度的下标，从栈底到栈顶温度递减。", extra=f"栈 = []，ans = {ans}")
    for i, x in enumerate(temps):
        popped = []
        while st and temps[st[-1]] < x:
            j = st.pop()
            ans[j] = i - j
            popped.append(j)
        st.append(i)
        if popped:
            msg = f"{x} 比栈顶高：弹出 " + "、".join(f"{j}（{temps[j]}，等 {i - j} 天）" for j in popped) + f"，再把 {i} 入栈。"
        else:
            msg = f"{x} 不比栈顶高，{i} 入栈等着。"
        t.array(temps, {"i": i}, msg, hl=[i] + popped, extra=f"栈 = {show(st)}，ans = {ans}")
    t.array(temps, {}, f"遍历结束，栈里剩下的 {show(st)} 右边没有更高的，答案保持 0。每个下标只入栈出栈一次，O(n)。", hl=st, extra=f"ans = {ans}")
    t.save()


def lc11():
    h = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    t = Trace("lc11", "11 盛最多水的容器 · 移动短板")
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        area = min(h[l], h[r]) * (r - l)
        best = max(best, area)
        if h[l] < h[r]:
            msg = f"面积 = min({h[l]}, {h[r]}) × {r - l} = {area}。左边是短板，移动 l：长板留着，宽度变小，面积只会更小，所以以 l 为边的其他组合都可以排除。"
            t.array(h, {"l": l, "r": r}, msg, hl=[l, r], window=(l, r), extra=f"best = {best}")
            l += 1
        else:
            msg = f"面积 = min({h[l]}, {h[r]}) × {r - l} = {area}。右边是短板（或一样高），移动 r。"
            t.array(h, {"l": l, "r": r}, msg, hl=[l, r], window=(l, r), extra=f"best = {best}")
            r -= 1
    t.array(h, {"l": l, "r": r}, f"l 和 r 相遇，答案 {best}（下标 1 和 8）。", hl=[1, 8], extra=f"best = {best}")
    t.save()


def lc31():
    nums = [1, 5, 8, 4, 7, 6, 5, 3, 1]
    t = Trace("lc31", "31 下一个排列 · 找下降点 → 交换 → 反转")
    n = len(nums)
    t.array(nums, {}, "目标：比当前排列大的排列里最小的一个。要让变化尽量靠右。", extra=f"nums = {nums}")
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        t.array(nums, {"i": i}, f"nums[{i}] = {nums[i]} ≥ nums[{i + 1}] = {nums[i + 1]}，后缀还是降序，继续往左。", hl=[i, i + 1], window=(i + 1, n - 1))
        i -= 1
    t.array(nums, {"i": i}, f"nums[{i}] = {nums[i]} < nums[{i + 1}] = {nums[i + 1]}：下降点。后缀 {nums[i + 1:]} 是降序的，已经是这些数能排出的最大值，所以必须改 nums[{i}]。", hl=[i], window=(i + 1, n - 1))
    j = n - 1
    while nums[j] <= nums[i]:
        j -= 1
    t.array(nums, {"i": i, "j": j}, f"在后缀里从右往左找第一个比 {nums[i]} 大的数：nums[{j}] = {nums[j]}，它是后缀里比 {nums[i]} 大的最小的数。", hl=[i, j], window=(i + 1, n - 1))
    nums[i], nums[j] = nums[j], nums[i]
    t.array(nums, {"i": i, "j": j}, f"交换。后缀 {nums[i + 1:]} 仍然是降序。", hl=[i, j], window=(i + 1, n - 1))
    nums[i + 1:] = reversed(nums[i + 1:])
    t.array(nums, {"i": i}, f"把后缀反转成升序，让它最小。答案 {nums}。", hl=list(range(i + 1, n)), window=(i + 1, n - 1))
    t.save()


def lc88():
    nums1, m = [1, 4, 7, 0, 0, 0], 3
    nums2, n = [2, 5, 6], 3
    t = Trace("lc88", "88 合并两个有序数组 · 从后往前")
    i, j, k = m - 1, n - 1, m + n - 1
    t.array(nums1, {"i": i, "k": k}, "从后往前放：k 位置是空位或者已经处理过的元素，不会覆盖还没比较的数。", extra=f"nums2 = {nums2}，j = {j}")
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            msg = f"nums1[{i}] = {nums1[i]} > nums2[{j}] = {nums2[j]}，把 {nums1[i]} 放到 k = {k}。"
            nums1[k] = nums1[i]
            i -= 1
        else:
            msg = f"nums2[{j}] = {nums2[j]} 更大（或 nums1 已经用完），放到 k = {k}。"
            nums1[k] = nums2[j]
            j -= 1
        t.array(nums1, {"i": max(i, 0), "k": k} if i >= 0 else {"k": k}, msg, hl=[k], extra=f"nums2 = {nums2}，j = {j}")
        k -= 1
    t.array(nums1, {}, f"nums2 放完就结束，nums1 前面剩下的已经在正确位置。结果 {nums1}。", extra="")
    t.save()


if __name__ == "__main__":
    for f in (lc20, lc32, lc224, lc394, lc739, lc11, lc31, lc88):
        f()
