"""B 层：动态规划、贪心里带图解的题：1143（二维 DP 表）、55（最远可达位置）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc1143():
    a, b = "abcde", "ace"
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    t = Trace("lc1143", "1143 最长公共子序列 · dp[i][j]（行：abcde 的前 i 个，列：ace 的前 j 个）")

    def cells():
        head = [" ", "∅"] + list(b)
        rows = [head]
        for i in range(m + 1):
            rows.append([("∅" if i == 0 else a[i - 1])] + dp[i])
        return rows

    def tone(cur=None, src=()):
        tn = [[0] * (n + 2) for _ in range(m + 2)]
        for r, c in src:
            tn[r + 1][c + 1] = 2
        if cur:
            tn[cur[0] + 1][cur[1] + 1] = 1
        return tn

    t.grid(cells(), "第 0 行、第 0 列是空串，LCS 为 0。每个格子只依赖左边、上边、左上三个格子。", tone=tone())
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                msg = f"a[{i - 1}] = '{a[i - 1]}' 等于 b[{j - 1}] = '{b[j - 1]}'：这两个字符一起放进公共子序列，dp = 左上 + 1 = {dp[i][j]}。"
                src = [(i - 1, j - 1)]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                msg = f"'{a[i - 1]}' ≠ '{b[j - 1]}'：至少有一个用不上，取 max(上 {dp[i - 1][j]}, 左 {dp[i][j - 1]}) = {dp[i][j]}。"
                src = [(i - 1, j), (i, j - 1)]
            t.grid(cells(), msg, hl=[(i + 1, j + 1)], tone=tone((i, j), src))
    t.grid(cells(), f"右下角 dp[{m}][{n}] = {dp[m][n]} 就是答案（\"ace\"）。O(mn) 时间；只依赖上一行，可以压缩成一维。", hl=[(m + 1, n + 1)], tone=tone((m, n)))
    t.save()


def lc55():
    nums = [2, 3, 1, 0, 4]
    t = Trace("lc55", "55 跳跃游戏 · 维护最远可达位置")
    far = 0
    t.array(nums, {}, "从左往右走，far 记录目前能跳到的最远下标。走到的位置超过 far，就说明这个位置到不了。", extra="far = 0")
    for i, x in enumerate(nums):
        if i > far:
            t.array(nums, {"i": i}, f"i = {i} > far = {far}，到不了，返回 False。", hl=[i], extra=f"far = {far}")
            break
        old = far
        far = max(far, i + x)
        t.array(nums, {"i": i}, f"i = {i} 能到。从这里最远跳到 {i} + {x} = {i + x}，far = max({old}, {i + x}) = {far}。", hl=[i], window=(i, min(far, len(nums) - 1)), extra=f"far = {far}")
        if far >= len(nums) - 1:
            t.array(nums, {"i": i}, f"far = {far} ≥ 最后一个下标 {len(nums) - 1}，最后一个位置一定能到。代码里也可以在这里提前返回 True。", hl=[len(nums) - 1], extra=f"far = {far}")
            break
    t.array(nums, {}, "只遍历一遍，O(n) 时间，O(1) 空间。", extra=f"far = {far}")
    t.save()


if __name__ == "__main__":
    lc1143()
    lc55()
