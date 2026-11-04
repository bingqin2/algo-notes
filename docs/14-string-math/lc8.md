---
title: "8. 字符串转换整数 (atoi)"
lc: 8
slug: string-to-integer-atoi
difficulty: 中等
tier: C
source: "题型补强"
status: done
---
# 8. 字符串转换整数 (atoi)

> [力扣 8](https://leetcode.cn/problems/string-to-integer-atoi/) · 中等 · 来源：题型补强
>
> C 层：认得题型，说得出方法和关键点

## 识别信号

实现 atoi：跳过前导空格 → 读一个可选的正负号 → 读连续数字 → 超出 32 位范围就截断。按顺序模拟。

## 关键点

- 读到非数字字符就停（`"4193 with words"` 得到 4193）；一开始就不是数字返回 0。
- 每读一位就判断是否越界，越界直接返回 INT_MAX 或 INT_MIN，否则 Java 里会溢出。
- 也可以写成有限状态机（start / signed / number / end），面试时讲清思路就行。

```python
def myAtoi(s):
    INT_MAX, INT_MIN = 2 ** 31 - 1, -2 ** 31
    i, n = 0, len(s)
    while i < n and s[i] == " ":
        i += 1
    sign = 1
    if i < n and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1
    res = 0
    while i < n and s[i].isdigit():
        res = res * 10 + int(s[i])
        if sign * res > INT_MAX:           # 一超出范围就截断返回
            return INT_MAX
        if sign * res < INT_MIN:
            return INT_MIN
        i += 1
    return sign * res
```

相关：[7. 整数反转](./lc7)、[65. 有效数字](https://leetcode.cn/problems/valid-number/)
