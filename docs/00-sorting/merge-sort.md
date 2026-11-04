---
title: "手写归并排序"
difficulty: 手写
tier: A
source: "手写"
asked: "腾讯"
status: done
---
# 手写归并排序（含原地归并追问）

> 非力扣原题，面试手写题 · 近两年面经里出现在：**腾讯**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

要求**稳定**排序、**链表**排序、或者统计**逆序对**。归并排序任何输入都是 O(n log n)，代价是 O(n) 的额外空间。

核心思想：把数组分成两半，**各自排好**（递归），再把两个有序数组**合并**。

## 解法一：自顶向下递归

**思路**：sort(lo, hi) 先排 [lo, mid] 和 [mid+1, hi]，再合并。合并时把这一段复制到 tmp，用两个指针从 tmp 的两半里每次取较小的放回原数组。

<StepPlayer src="/viz/merge-sort.json" />

```python
def merge_sort(nums):
    tmp = [0] * len(nums)

    def sort(lo, hi):                      # 排序 nums[lo..hi]
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid + 1, hi)
        if nums[mid] <= nums[mid + 1]:     # 已经有序，省掉合并
            return
        tmp[lo:hi + 1] = nums[lo:hi + 1]
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if j > hi or (i <= mid and tmp[i] <= tmp[j]):   # <= 保证稳定
                nums[k] = tmp[i]
                i += 1
            else:
                nums[k] = tmp[j]
                j += 1

    sort(0, len(nums) - 1)
    return nums
```

**复杂度**：时间 O(n log n)（log n 层，每层合并 O(n)），空间 O(n)（tmp）+ O(log n)（递归栈）。

两个细节：

- `tmp[i] <= tmp[j]` 取左边：相等时左边的先放，保证**稳定**。
- `nums[mid] <= nums[mid + 1]` 时两半已经整体有序，跳过合并。对几乎有序的数组很有效。

## 解法二：自底向上迭代

**思路**：不递归。先把相邻的长度为 1 的段两两合并，再合并长度为 2 的，再 4、8……直到整个数组。

```python
def merge_sort(nums):
    n = len(nums)
    width = 1
    while width < n:                       # 每轮把长度为 width 的相邻两段合并
        for lo in range(0, n - width, 2 * width):
            mid, hi = lo + width - 1, min(lo + 2 * width - 1, n - 1)
            left, right = nums[lo:mid + 1], nums[mid + 1:hi + 1]
            i = j = 0
            for k in range(lo, hi + 1):
                if j == len(right) or (i < len(left) and left[i] <= right[j]):
                    nums[k] = left[i]
                    i += 1
                else:
                    nums[k] = right[j]
                    j += 1
        width *= 2
    return nums
```

**复杂度**：时间 O(n log n)，空间 O(n)，没有递归栈。链表排序（[148](../04-linked-list/lc148)）要求 O(1) 空间时，就是用这个思路：按步长 1、2、4… 拆分、合并链表。

## 解法三：逆序对计数（归并的应用）

**问题**：数组中 i < j 且 nums[i] > nums[j] 的对数（剑指 Offer 51）。

**思路**：合并时，如果右半边的 tmp[j] 先被放入，说明左半边剩下的 tmp[i..mid] 都比它大，它们和 tmp[j] 各组成一个逆序对，一次加上 `mid − i + 1` 个。

```python
def reverse_pairs(nums):               # 剑指 Offer 51：数组中的逆序对
    nums = nums[:]
    tmp = [0] * len(nums)

    def sort(lo, hi):
        if lo >= hi:
            return 0
        mid = (lo + hi) // 2
        cnt = sort(lo, mid) + sort(mid + 1, hi)
        tmp[lo:hi + 1] = nums[lo:hi + 1]
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if j > hi or (i <= mid and tmp[i] <= tmp[j]):
                nums[k] = tmp[i]
                i += 1
            else:
                nums[k] = tmp[j]
                j += 1
                cnt += mid - i + 1         # 左半边剩下的都比 tmp[j] 大
        return cnt

    return sort(0, len(nums) - 1)
```

**复杂度**：O(n log n)。暴力是 O(n²)。

## 易错点

- 合并时用 `<` 取左边：相等时右边先放，变成不稳定排序。
- 每次合并都新建临时数组：能用，但慢；提前开好一个 tmp 复用。
- 计算 mid 用 `(lo + hi) / 2`：Java 里 lo + hi 可能溢出，写 `lo + (hi − lo) / 2`。
- 逆序对的计数要在**右边元素先放入**时加，不是左边。

## 面试追问

- **归并和快排怎么选？** 要稳定、要最坏 O(n log n)、数据是链表或在磁盘上：归并。要原地、平均更快：快排。
- **能不能不用额外数组（原地归并）？** 数组上可以用「手摇算法」：合并时找到右半边开头一段比 nums[i] 小的元素，用三次反转把这段和它前面的左半边元素整体旋转过来。只用 O(1) 额外空间，但简单实现最坏 O(n²)，实际很少用；面试能说出思路和代价即可。链表上的归并天然只改指针，额外空间 O(1)，见 [148](../04-linked-list/lc148)。
- **外部排序（数据比内存大）？** 分块读入内存排好写回磁盘，再对 k 个有序文件做 k 路归并（用小顶堆选最小值）。
- **合并 k 个有序链表？** 两两归并或小顶堆，见 [23](../04-linked-list/lc23)。
- **类似的「合并时顺便统计」？** 计算右侧小于当前元素的个数（315）、翻转对（493）都是这个套路。

## Java 版

```java
public void mergeSort(int[] a) {
    sort(a, 0, a.length - 1, new int[a.length]);
}

private void sort(int[] a, int lo, int hi, int[] tmp) {
    if (lo >= hi) return;
    int mid = lo + (hi - lo) / 2;
    sort(a, lo, mid, tmp);
    sort(a, mid + 1, hi, tmp);
    if (a[mid] <= a[mid + 1]) return;
    System.arraycopy(a, lo, tmp, lo, hi - lo + 1);
    int i = lo, j = mid + 1;
    for (int k = lo; k <= hi; k++) {
        if (j > hi || (i <= mid && tmp[i] <= tmp[j])) a[k] = tmp[i++];
        else a[k] = tmp[j++];
    }
}
```

## 相关题

- [148. 排序链表](../04-linked-list/lc148)
- [23. 合并 K 个升序链表](../04-linked-list/lc23)
- [88. 合并两个有序数组](../01-array-two-pointers/lc88)
- [快速排序](./quick-sort)
