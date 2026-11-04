"""动态规划 A 层题的执行过程：198、53、300、5、322。"""
import sys
from bisect import bisect_left
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc198():
    nums = [2, 7, 9, 3, 1]
    t = Trace("lc198", "198 打家劫舍 · dp[i] = max(dp[i-1], dp[i-2] + nums[i])")
    dp = ["?"] * len(nums)
    t.array(nums, {}, "dp[i] 表示前 i 间房（0..i）最多能偷多少。每间房只有两种选择：偷或不偷。", extra=f"dp = {dp}")
    dp[0] = nums[0]
    t.array(nums, {"i": 0}, "dp[0] = nums[0] = 2：只有一间房，偷它。", hl=[0], extra=f"dp = {dp}")
    dp[1] = max(nums[0], nums[1])
    t.array(nums, {"i": 1}, "dp[1] = max(2, 7) = 7：两间房只能偷一间，偷大的。", hl=[1], extra=f"dp = {dp}")
    for i in range(2, len(nums)):
        skip, take = dp[i - 1], dp[i - 2] + nums[i]
        dp[i] = max(skip, take)
        choice = "偷" if take >= skip else "不偷"
        t.array(nums, {"i": i}, f"不偷第 {i} 间：dp[{i-1}] = {skip}；偷：dp[{i-2}] + {nums[i]} = {take}。取大的 → {choice}，dp[{i}] = {dp[i]}。", hl=[i, i - 2] if take >= skip else [i - 1], extra=f"dp = {dp}")
    t.array(nums, {}, f"答案 dp[{len(nums)-1}] = {dp[-1]}（偷 2、9、1）。dp[i] 只依赖前两个值，所以可以只用两个变量，空间 O(1)。", hl=[0, 2, 4], extra=f"dp = {dp}")
    t.save()


def lc53():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    t = Trace("lc53", "53 最大子数组和 · Kadane")
    cur = best = nums[0]
    start = bs = be = 0
    t.array(nums, {"i": 0}, "cur = 以当前元素结尾的最大子数组和。初始 cur = best = -2。", hl=[0], window=(0, 0), extra=f"cur = {cur}，best = {best}")
    for i in range(1, len(nums)):
        x = nums[i]
        if cur + x < x:
            cur, start = x, i
            why = f"前面的和 {cur - x if False else '为负'}，接上反而更小，从 {x} 重新开始"
        else:
            cur += x
            why = f"接上前面：cur = {cur}"
        if cur > best:
            best, bs, be = cur, start, i
        t.array(nums, {"i": i}, why + f"。best = {best}。", hl=[i], window=(start, i), extra=f"cur = {cur}，best = {best}（区间 [{bs}, {be}]）")
    t.array(nums, {}, f"答案 {best}，子数组是 [4, -1, 2, 1]。", hl=list(range(bs, be + 1)), window=(bs, be), extra=f"best = {best}")
    t.save()


def lc300():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    t = Trace("lc300", "300 最长递增子序列 · 贪心 + 二分")
    tails = []
    t.array(nums, {}, "tails[k] = 长度为 k+1 的递增子序列里，最小的结尾。结尾越小，后面越容易接上。", extra="tails = []")
    for i, x in enumerate(nums):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            msg = f"{x} 比所有结尾都大，接在最后，长度变成 {len(tails)}。"
        else:
            old = tails[k]
            tails[k] = x
            msg = f"二分找到第一个 ≥ {x} 的位置 {k}，把 {old} 换成 {x}：长度为 {k+1} 的子序列结尾变小了。"
        t.array(nums, {"i": i}, msg, hl=[i], extra=f"tails = {tails}")
    t.array(nums, {}, f"答案 = len(tails) = {len(tails)}。注意 tails 本身不一定是一个真实的子序列。时间 O(n log n)。", extra=f"tails = {tails}")
    t.save()


def lc5():
    s = "cbabad"
    t = Trace("lc5", "5 最长回文子串 · 中心扩展")
    best = (0, 1)
    for i in range(len(s)):
        for l, r, kind in ((i, i, "奇"), (i, i + 1, "偶")):
            if r >= len(s):
                continue
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l, r = l - 1, r + 1
            lo, hi = l + 1, r - 1
            if hi >= lo:
                if hi - lo + 1 > best[1] - best[0]:
                    best = (lo, hi + 1)
                t.array(s, {"l": max(lo, 0), "r": hi}, f"以 {'s[%d]' % i if kind == '奇' else 's[%d..%d]' % (i, i + 1)} 为中心（{kind}数长度），扩展到 \"{s[lo:hi+1]}\"。", hl=list(range(lo, hi + 1)), window=(lo, hi), extra=f"目前最长：\"{s[best[0]:best[1]]}\"")
            else:
                t.array(s, {"i": i}, f"以 s[{i}..{i+1}] 为中心（偶数长度）：两个字符不相等，扩展不了。", hl=[i, i + 1], extra=f"目前最长：\"{s[best[0]:best[1]]}\"")
    t.array(s, {}, f"答案 \"{s[best[0]:best[1]]}\"。每个位置作中心扩展两次（奇、偶），时间 O(n²)，空间 O(1)。", hl=list(range(*best)), window=(best[0], best[1] - 1))
    t.save()


def lc322():
    coins, amount = [1, 2, 5], 11
    t = Trace("lc322", "322 零钱兑换 · coins = [1, 2, 5]，amount = 11")
    INF = "∞"
    dp = [0] + [INF] * amount
    t.array(dp, {}, "dp[x] = 凑出金额 x 最少要几枚硬币。dp[0] = 0，其余先设为 ∞。下标就是金额。")
    for x in range(1, amount + 1):
        cand = [(dp[x - c] + 1, c) for c in coins if c <= x and dp[x - c] != INF]
        best = min(cand)
        dp[x] = best[0]
        parts = "、".join(f"dp[{x}-{c}]+1={v}" for v, c in cand)
        t.array(dp, {"x": x}, f"金额 {x}：最后一枚分别试 {', '.join(str(c) for _, c in cand)}：{parts}。取最小 {dp[x]}。", hl=[x] + [x - best[1]])
    t.array(dp, {}, "答案 dp[11] = 3（5 + 5 + 1）。时间 O(amount × 硬币种类)。", hl=[11])
    t.save()


if __name__ == "__main__":
    lc198(); lc53(); lc300(); lc5(); lc322()
