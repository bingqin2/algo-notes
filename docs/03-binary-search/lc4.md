---
title: "4. 寻找两个正序数组的中位数"
lc: 4
slug: median-of-two-sorted-arrays
difficulty: 困难
tier: B
source: "Hot 100"
asked: "高频经典"
status: done
---
# 4. 寻找两个正序数组的中位数

> [力扣 4](https://leetcode.cn/problems/median-of-two-sorted-arrays/) · 近两年面经里出现在：**高频经典**
>
> B 层：掌握最优解法，20 分钟内写出

## 识别信号

两个有序数组的中位数，要求 O(log(m+n))：不合并，而是二分**划分位置**：在两个数组上各切一刀，使左半部分的元素个数等于总数的一半，并且左半部分的最大值 ≤ 右半部分的最小值。

## 解法一：合并 O(m+n)

**思路**：归并两个有序数组，取中间的一个或两个。只需要走到中间就能停，不必合并完。

```python
def findMedianSortedArrays(nums1, nums2):
    merged, i, j = [], 0, 0
    while i < len(nums1) or j < len(nums2):
        if j == len(nums2) or (i < len(nums1) and nums1[i] <= nums2[j]):
            merged.append(nums1[i]); i += 1
        else:
            merged.append(nums2[j]); j += 1
    n = len(merged)
    return merged[n // 2] if n % 2 else (merged[n // 2 - 1] + merged[n // 2]) / 2
```

**复杂度**：时间 O(m + n)，空间 O(m + n)（只记录中间两个数可以做到 O(1)）。

## 解法二：二分划分 O(log min(m,n))

**思路**：

- 在**短**数组 nums1 上二分 i（左边取 i 个），nums2 左边就取 `j = half − i` 个，`half = (m + n + 1) // 2`。
- 划分正确的条件：`nums1[i−1] ≤ nums2[j]` 且 `nums2[j−1] ≤ nums1[i]`。
- `nums1[i−1] > nums2[j]`：nums1 取多了，i 减小；`nums2[j−1] > nums1[i]`：nums1 取少了，i 增大。
- 越界的位置用 ±∞ 代替。
- 总数为奇数：中位数是左半部分的最大值；偶数：左边最大和右边最小的平均。

<StepPlayer src="/viz/lc4.json" />

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1        # 在短的数组上二分
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2                # 左半部分的元素个数
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2                 # nums1 左边取 i 个
        j = half - i                       # nums2 左边取 j 个
        l1 = nums1[i - 1] if i > 0 else float("-inf")
        r1 = nums1[i] if i < m else float("inf")
        l2 = nums2[j - 1] if j > 0 else float("-inf")
        r2 = nums2[j] if j < n else float("inf")
        if l1 > r2:                        # nums1 左边取多了
            hi = i - 1
        elif l2 > r1:                      # nums1 左边取少了
            lo = i + 1
        else:
            if (m + n) % 2:
                return max(l1, l2)
            return (max(l1, l2) + min(r1, r2)) / 2
```

**复杂度**：时间 O(log min(m, n))，空间 O(1)。

## 易错点

- 不在短数组上二分：j 可能变成负数或超过 n。
- `half = (m + n + 1) // 2`：让奇数时左半部分多一个，中位数就是左半部分的最大值。
- 二分范围是 `[0, m]`（i 可以取 0 和 m），不是 `[0, m − 1]`。

**另一种 O(log(m+n)) 解法**：求第 k 小：每次比较两个数组的第 k/2 个元素，较小的那一边前 k/2 个一定不是第 k 小，排除掉，k 减半。

## 相关题

- [295. 数据流的中位数](../06-heap-topk/lc295)
- [88. 合并两个有序数组](../01-array-two-pointers/lc88)
