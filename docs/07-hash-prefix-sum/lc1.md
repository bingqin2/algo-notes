---
title: "1. 两数之和"
lc: 1
slug: two-sum
difficulty: 简单
tier: C
source: "Hot 100"
asked: "高频经典"
status: done
---
# 1. 两数之和

> [力扣 1](https://leetcode.cn/problems/two-sum/) · 近两年面经里出现在：**高频经典**
>
> C 层：认得题型，说得出方法和关键点

## 识别信号

找两个数的和等于 target：对每个数 x，问「target − x 出现过没有」，用**哈希表**把查找变成 O(1)。

## 解法一：哈希表一次遍历

**思路**：边遍历边查：先查 `target − x` 在不在哈希表里，在就返回；不在就把 x 和它的下标放进去。先查再放，保证不会用同一个元素两次。

<StepPlayer src="/viz/lc1.json" />

```python
def twoSum(nums, target):
    seen = {}                              # 值 → 下标
    for i, x in enumerate(nums):
        if target - x in seen:             # 先查再放，避免用到自己
            return [seen[target - x], i]
        seen[x] = i
    return []
```

**复杂度**：时间 O(n)，空间 O(n)。

## 易错点

- 先放再查：`[3, 3]`、target = 6 时没问题，但 `[3]`、target = 6 会错误地用到自己。
- 暴力两层循环 O(n²)；排序 + 双指针 O(n log n)，但排序后下标变了，要额外记录原下标。

**追问**：数组有序？用[双指针](../01-array-two-pointers/lc167)，O(1) 空间。要所有不重复的组合？见[三数之和](../01-array-two-pointers/lc15)的去重方法。

## 相关题

- [167. 两数之和 II](../01-array-two-pointers/lc167)
- [15. 三数之和](../01-array-two-pointers/lc15)
- [560. 和为 K 的子数组](./lc560)：同样是「查之前出现过的值」
