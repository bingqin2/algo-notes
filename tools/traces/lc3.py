"""3. 无重复字符的最长子串：滑动窗口的执行过程。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def main():
    s = "abcabcbb"
    t = Trace("lc3", "3 无重复字符的最长子串 · 滑动窗口")
    last = {}
    left = best = 0
    t.array(s, {"left": 0}, "窗口 [left, right] 内保证没有重复字符；last 记录每个字符最后出现的位置。", extra="last = {}")
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            t.array(s, {"left": left, "right": right}, f"'{ch}' 在窗口里出现过（位置 {last[ch]}），left 跳到 {last[ch] + 1}。", hl=[last[ch], right], window=(left, right - 1), extra=f"last = {last}")
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
        t.array(s, {"left": left, "right": right}, f"窗口 = \"{s[left:right + 1]}\"，长度 {right - left + 1}，目前最长 {best}。", hl=[right], window=(left, right), extra=f"last = {last}")
    t.array(s, {}, f"扫描结束，答案 = {best}。时间 O(n)，每个字符最多进出窗口一次。")
    t.save()


if __name__ == "__main__":
    main()
