---
title: "6. Z 字形变换"
lc: 6
slug: zigzag-conversion
difficulty: 中等
tier: A
source: "面试经典 150 · 面经"
asked: "腾讯 ×2"
status: done
---
# 6. Z 字形变换

> [力扣 6](https://leetcode.cn/problems/zigzag-conversion/) · 近两年面经里出现在：**腾讯 ×2**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

按之字形写、按行读。两种做法：**按行模拟**（直观，面试先写这个），**按周期算下标**（不需要额外的行缓存）。

```text
numRows = 4，s = "PAYPALISHIRING"

P     I     N        第 0 行：P I N
A   L S   I G        第 1 行：A L S I G
Y A   H R            第 2 行：Y A H R
P     I              第 3 行：P I

输出：PINALSIGYAHRPI
```

## 解法一：按行模拟，方向在首末行翻转

**思路**：准备 numRows 个字符串，用 r 记当前行，step 记方向（+1 往下，−1 往上）。每放一个字符就 `r += step`，到第 0 行改成往下，到最后一行改成往上。

```python
def convert(s, numRows):
    if numRows == 1:
        return s
    rows = [''] * numRows
    r, step = 0, 1
    for c in s:
        rows[r] += c
        if r == 0:
            step = 1                       # 到顶往下走
        elif r == numRows - 1:
            step = -1                      # 到底往上走
        r += step
    return ''.join(rows)
```

**复杂度**：时间 O(n)，空间 O(n)。

## 解法二：按周期 2n−2 直接计算下标

**思路**：一个周期是「竖着往下 numRows 个 + 斜着往上 numRows − 2 个」，长度 t = 2·numRows − 2。

- 第 0 行和最后一行：每个周期只有一个字符，下标 k, k + t, k + 2t, …（k 从 r 开始）。
- 中间第 r 行：每个周期有两个字符，一个在竖线上（k），一个在斜线上（k + t − 2r）。

```python
def convert(s, numRows):
    if numRows == 1:
        return s
    t = 2 * numRows - 2                    # 一个周期：竖着一列 + 斜着回来
    n = len(s)
    res = []
    for r in range(numRows):
        for k in range(r, n, t):           # 每个周期里第 r 行的第一个字符
            res.append(s[k])
            mid = k + t - 2 * r            # 中间行在斜线上还有一个
            if 0 < r < numRows - 1 and mid < n:
                res.append(s[mid])
    return ''.join(res)
```

**复杂度**：时间 O(n)，除结果外空间 O(1)。

## 易错点

- numRows = 1：周期 t = 0，`range(r, n, 0)` 会报错；按行模拟也会因为 r 一直是 0 而 step 来回翻转出错。必须先特判。
- 斜线上那个字符的下标是 `k + t − 2r`，只在中间行有。
- numRows ≥ len(s) 时结果就是原串，两种解法都能正确处理，不用特判。

## 面试追问

- **反过来，从之字形结果还原原串？** 按解法二的下标公式，把第 i 个输出字符放回它的原始位置。
- **怎么想到周期的？** 先画出 numRows = 3、4 的例子，标出每个字符的原始下标，规律很明显。

## Java 版

```java
public String convert(String s, int numRows) {
    if (numRows == 1) return s;
    StringBuilder[] rows = new StringBuilder[numRows];
    for (int i = 0; i < numRows; i++) rows[i] = new StringBuilder();
    int r = 0, step = 1;
    for (char c : s.toCharArray()) {
        rows[r].append(c);
        if (r == 0) step = 1;
        else if (r == numRows - 1) step = -1;
        r += step;
    }
    StringBuilder res = new StringBuilder();
    for (StringBuilder row : rows) res.append(row);
    return res.toString();
}
```

## 相关题

- [54. 螺旋矩阵](./lc54)
- [48. 旋转图像](./lc48)
