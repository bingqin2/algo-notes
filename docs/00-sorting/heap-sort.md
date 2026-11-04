---
title: "手写堆排序"
difficulty: 手写
tier: A
source: "手写"
asked: "腾讯"
status: done
---
# 手写堆排序

> 非力扣原题，面试手写题 · 近两年面经里出现在：**腾讯**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

被问「堆是怎么实现的」「优先队列底层是什么」，或者要求 O(n log n) 且 O(1) 额外空间。腾讯考过手写堆排序。

**堆就是用数组存的完全二叉树**：下标 i 的父结点是 (i − 1) / 2，孩子是 2i + 1 和 2i + 2。大顶堆要求每个结点 ≥ 它的孩子，所以堆顶是最大值。

## 解法一：下沉建堆 O(n)

**思路**：叶子本身就是堆。从**最后一个非叶子结点**（n / 2 − 1）开始往前，对每个结点做**下沉**：和较大的孩子比，比孩子小就交换，一直沉到合适的位置。

**为什么是 O(n) 而不是 O(n log n)**：大部分结点在底层，下沉的距离很短。高度为 h 的结点约有 n / 2^(h+1) 个，每个最多下沉 h 次，总和 Σ h · n / 2^(h+1) = O(n)。

## 解法二：逐个弹出堆顶

**思路**：堆顶是最大值，和最后一个元素交换，最大值就到了最终位置；堆的大小减 1，新的堆顶下沉。重复 n − 1 次。

<StepPlayer src="/viz/heap-sort.json" />

```python
def heap_sort(nums):
    n = len(nums)

    def sift_down(i, size):                # 大顶堆：把 nums[i] 往下沉到合适位置
        while True:
            big, l, r = i, 2 * i + 1, 2 * i + 2
            if l < size and nums[l] > nums[big]:
                big = l
            if r < size and nums[r] > nums[big]:
                big = r
            if big == i:
                return
            nums[i], nums[big] = nums[big], nums[i]
            i = big

    for i in range(n // 2 - 1, -1, -1):    # 建堆：从最后一个非叶子结点往前下沉，O(n)
        sift_down(i, n)
    for end in range(n - 1, 0, -1):        # 堆顶是最大值，换到末尾，堆变小 1
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)
    return nums
```

**复杂度**：时间 O(n log n)（建堆 O(n) + n 次下沉各 O(log n)），空间 O(1)。不稳定。

## 手写一个小顶堆（优先队列）

面试官问「堆怎么实现」时，写出 push（**上浮**）和 pop（**堆顶换成最后一个再下沉**）：

```python
class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[(i - 1) // 2] > a[i]:   # 上浮：比父结点小就交换
            a[i], a[(i - 1) // 2] = a[(i - 1) // 2], a[i]
            i = (i - 1) // 2

    def pop(self):
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last                    # 最后一个元素放到堆顶，再下沉
            i = 0
            while True:
                small, l, r = i, 2 * i + 1, 2 * i + 2
                if l < len(a) and a[l] < a[small]:
                    small = l
                if r < len(a) and a[r] < a[small]:
                    small = r
                if small == i:
                    break
                a[i], a[small] = a[small], a[i]
                i = small
        return top

    def __len__(self):
        return len(self.a)
```

push、pop 都是 O(log n)，取堆顶 O(1)。

## 三种 O(n log n) 排序对比

| | 快排 | 归并 | 堆排序 |
|---|---|---|---|
| 平均时间 | O(n log n) | O(n log n) | O(n log n) |
| 最坏时间 | O(n²) | O(n log n) | O(n log n) |
| 额外空间 | O(log n) 栈 | O(n) | O(1) |
| 稳定 | 否 | 是 | 否 |
| 实际速度 | 通常最快 | 中 | 较慢：跳着访问数组，缓存不友好 |

## 易错点

- 建堆从 0 开始往后下沉：不对，要从 n / 2 − 1 往前，保证下沉时孩子已经是堆。
- 下沉时只和左孩子比，或者没选较大的孩子交换。
- 排序阶段 sift_down 的 size 没有缩小：已经排好的元素又被换回堆里。
- 用大顶堆得到升序，用小顶堆得到降序，别搞反。

## 面试追问

- **Java 的 `PriorityQueue` 是怎么实现的？** 数组存的小顶堆，`offer` 上浮，`poll` 把最后一个元素放到堆顶再下沉，默认容量 11，满了扩容（小于 64 时翻倍加 2，否则加 50%）。不是线程安全的，并发用 `PriorityBlockingQueue`。
- **Top K 用堆怎么做？** 求前 k 大用大小为 k 的**小顶堆**，见 [347](../06-heap-topk/lc347)、[215](./lc215)。
- **数据流的中位数？** 一个大顶堆存较小的一半，一个小顶堆存较大的一半，见 [295](../06-heap-topk/lc295)。
- **堆删除任意元素？** 和最后一个交换后删掉，再对这个位置上浮或下沉（需要知道元素的下标，通常配一个哈希表）。

## Java 版

```java
public void heapSort(int[] a) {
    int n = a.length;
    for (int i = n / 2 - 1; i >= 0; i--) siftDown(a, i, n);
    for (int end = n - 1; end > 0; end--) {
        swap(a, 0, end);
        siftDown(a, 0, end);
    }
}

private void siftDown(int[] a, int i, int size) {
    while (true) {
        int big = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < size && a[l] > a[big]) big = l;
        if (r < size && a[r] > a[big]) big = r;
        if (big == i) return;
        swap(a, i, big);
        i = big;
    }
}

private void swap(int[] a, int i, int j) {
    int t = a[i]; a[i] = a[j]; a[j] = t;
}
```

## 相关题

- [215. 数组中的第 K 个最大元素](./lc215)
- [347. 前 K 个高频元素](../06-heap-topk/lc347)
- [295. 数据流的中位数](../06-heap-topk/lc295)
- [快速排序](./quick-sort)
