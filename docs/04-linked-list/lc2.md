---
title: "2. 两数相加"
lc: 2
slug: add-two-numbers
difficulty: 中等
tier: B
source: "Hot 100"
status: done
---
# 2. 两数相加

> [力扣 2](https://leetcode.cn/problems/add-two-numbers/) · 中等 · 来源：Hot 100
>
> B 层：掌握最优解法，20 分钟内写出

## 识别信号

两个链表表示的大数相加，**低位在前**：按位相加、处理进位，和字符串相加（[415](../14-string-math/lc415)）一样。

## 最优解法

**思路**：哑结点 + 尾指针。两个链表、进位三者有一个没处理完就继续：当前位 = 两个数位 + 进位，`divmod` 得到新的进位和这一位。

```python
def addTwoNumbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        s = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, d = divmod(s, 10)
        tail.next = ListNode(d)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next
```

**复杂度**：时间 O(max(m, n))，空间 O(1)（不算结果）。

## 易错点

- 循环条件漏了 `or carry`：最高位的进位丢失（`5 + 5 = 10` 得到 `0`）。
- 两个链表长度不同，短的走完了要当 0 处理。

## 相关题

- [445. 两数相加 II](./lc445)：高位在前
- [415. 字符串相加](../14-string-math/lc415)
