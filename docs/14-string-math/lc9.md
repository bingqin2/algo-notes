---
title: "9. 回文数"
lc: 9
slug: palindrome-number
difficulty: 简单
tier: C
source: "面试经典 150"
status: done
---
# 9. 回文数

> [力扣 9](https://leetcode.cn/problems/palindrome-number/) · 简单 · 来源：面试经典 150
>
> C 层：认得题型，说得出方法和关键点

## 识别信号

判断整数是不是回文，不转字符串：**只反转后一半**，和前一半比较。

## 关键点

- 负数、以及末尾是 0 的非零数（如 10）一定不是回文。
- 循环条件 `x > half`：停下时位数已经过半。偶数位比较 `x == half`，奇数位中间那位在 half 的末尾，比较 `x == half // 10`。
- 只反转一半也不会溢出。O(log x)。

```python
def isPalindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    half = 0
    while x > half:                        # 只反转后一半
        half = half * 10 + x % 10
        x //= 10
    return x == half or x == half // 10    # 奇数位时中间那位在 half 里
```

相关：[7. 整数反转](./lc7)、[234. 回文链表](../04-linked-list/lc234)
