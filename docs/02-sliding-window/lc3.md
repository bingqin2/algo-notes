---
title: "3. 无重复字符的最长子串"
status: done
asked: "字节 ×3 · 小米"
---

# 3. 无重复字符的最长子串

> [力扣 3](https://leetcode.cn/problemset/?search=3) · 近两年面经里出现在：**字节 ×3 · 小米**

## 识别信号

求「最长/最短的连续子串（子数组）」，而且窗口内的条件可以在左右指针移动时增量更新。这道题是滑动窗口的模板题。

## 解法一：哈希集合 + 逐步收缩

**思路**：右指针每次加入一个字符。如果它已经在窗口里，就不断右移左指针、把字符移出集合，直到不重复为止。

```python
def lengthOfLongestSubstring(s: str) -> int:
    window = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in window:
            window.remove(s[left])
            left += 1
        window.add(ch)
        best = max(best, right - left + 1)
    return best
```

**复杂度**：时间 O(n)（每个字符最多进出集合各一次），空间 O(字符集大小)。

## 解法二：记录最后出现位置，左指针直接跳

**思路**：用哈希表记录每个字符最后一次出现的下标。遇到重复字符时，如果它上次出现的位置在窗口内，左指针直接跳到那个位置的下一位。

<StepPlayer src="/viz/lc3.json" />

```python
def lengthOfLongestSubstring(s: str) -> int:
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # 必须判断是否在窗口内
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**复杂度**：时间 O(n)，空间 O(字符集大小)。

## 滑动窗口通用模板

```python
def sliding_window(s):
    window = {}                      # 窗口内的状态
    left = 0
    for right, c in enumerate(s):
        # 1. 把 c 加入窗口，更新状态
        while 窗口需要收缩:
            # 2. 把 s[left] 移出窗口，更新状态
            left += 1
        # 3. 在这里更新答案（求最长时）
```

求最长时在收缩之后更新答案；求最短时（如 [76. 最小覆盖子串](./lc76)）在收缩的循环里面更新答案。

## 易错点

- 解法二忘记判断 `last[ch] >= left`。例如 `"abba"`：扫到最后一个 `a` 时，它上次出现的位置 0 已经不在窗口里了，左指针不能往回跳。
- 用 `right - left` 算长度，少了 1。

## 相关题

- [76. 最小覆盖子串](./lc76)
- [1004. 最大连续 1 的个数 III](./lc1004)
