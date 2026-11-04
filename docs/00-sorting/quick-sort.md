---
title: "手写快速排序（含三路划分）"
difficulty: 手写
tier: A
source: "手写"
asked: "美团 · 小红书 · 腾讯 · 帆软"
status: done
---
# 手写快速排序（含三路划分）

> 非力扣原题，面试手写题 · 近两年面经里出现在：**美团 · 小红书 · 腾讯 · 帆软**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

面试官说「手写一个排序」，或者要求 O(n log n) 且原地。快排是被要求手写最多的排序（近两年美团、小红书、腾讯、帆软都考过）。面试时通常这样推进：先写一个能跑的版本，再被追问**有序数组会怎样**、**大量重复元素会怎样**、**递归太深会怎样**。下面四个解法正好对应这几个问题。

核心思想：选一个**主元**，把数组划分成「小于主元」和「大于主元」两部分，主元落到最终位置，再递归排两边。

## 解法一：Lomuto 划分

**思路**：主元取最后一个元素。i 表示「小于主元的区域」的右边界，j 从左往右扫，遇到比主元小的就换到 i 的位置，i 右移。最后把主元换到 i。

<StepPlayer src="/viz/quick-sort.json" />

```python
def quick_sort(nums):
    def partition(lo, hi):
        pivot = nums[hi]                   # 取最后一个当主元
        i = lo                             # nums[lo..i-1] 都 < pivot
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]   # 主元放到最终位置
        return i

    def sort(lo, hi):
        if lo >= hi:
            return
        p = partition(lo, hi)
        sort(lo, p - 1)
        sort(p + 1, hi)

    sort(0, len(nums) - 1)
    return nums
```

**复杂度**：平均 O(n log n)，最坏 O(n²)（数组已经有序时，每次主元都是最大值，划分极不均匀）。空间 O(log n) ~ O(n)（递归栈）。

## 解法二：Hoare 双指针划分

**思路**：主元取中间元素。i 从左往右找 ≥ 主元的，j 从右往左找 ≤ 主元的，交换，直到 i、j 交错。结束时 [lo, j] 都 ≤ 主元，[i, hi] 都 ≥ 主元。

```python
def quick_sort(nums):
    def sort(lo, hi):
        if lo >= hi:
            return
        pivot = nums[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while nums[i] < pivot:         # 左边找一个 >= pivot 的
                i += 1
            while nums[j] > pivot:         # 右边找一个 <= pivot 的
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1
        sort(lo, j)                        # 结束时 j < i：[lo, j] 都 <= pivot，[i, hi] 都 >= pivot
        sort(i, hi)

    sort(0, len(nums) - 1)
    return nums
```

**复杂度**：和 Lomuto 同阶，但交换次数更少（大约是 Lomuto 的三分之一）。等于主元的元素会被分到两边，所以全部相等时也能均匀划分。

## 解法三：三路划分（大量重复元素）

**思路**：把数组分成三段：< 主元、= 主元、> 主元。等于主元的一整段不再参与递归。全是重复元素时一次划分就结束，O(n)。

- `nums[i] < pivot`：和 lt 交换，lt、i 都右移；
- `nums[i] > pivot`：和 gt 交换，gt 左移，**i 不动**（换过来的数还没看过）；
- 相等：i 右移。

```python
import random

def quick_sort(nums):
    def sort(lo, hi):
        if lo >= hi:
            return
        k = random.randint(lo, hi)         # 随机选主元，避免有序数组退化
        nums[lo], nums[k] = nums[k], nums[lo]
        pivot = nums[lo]
        lt, i, gt = lo, lo, hi             # [lo, lt) < pivot，[lt, i) == pivot，(gt, hi] > pivot
        while i <= gt:
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]
                lt += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1                    # 换过来的数还没看过，i 不动
            else:
                i += 1
        sort(lo, lt - 1)                   # 等于 pivot 的一整段不再参与递归
        sort(gt + 1, hi)

    sort(0, len(nums) - 1)
    return nums
```

**复杂度**：平均 O(n log n)；重复元素越多越快。这里也加了随机主元。

## 解法四：随机化选主元 + 只对短的一边递归

**思路**：

- **随机选主元**：避免有序输入导致的最坏情况。最坏仍是 O(n²)，但概率极低，期望 O(n log n)。
- **只对较短的一边递归，较长的一边用循环**：递归深度最多 O(log n)，不会栈溢出。

```python
import random

def quick_sort(nums):
    def partition(lo, hi):
        k = random.randint(lo, hi)
        nums[k], nums[hi] = nums[hi], nums[k]   # 随机主元换到末尾，再用 Lomuto
        pivot, i = nums[hi], lo
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        return i

    def sort(lo, hi):
        while lo < hi:                     # 只对较短的一边递归，栈深度 O(log n)
            p = partition(lo, hi)
            if p - lo < hi - p:
                sort(lo, p - 1)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p - 1

    sort(0, len(nums) - 1)
    return nums
```

**复杂度**：期望时间 O(n log n)，栈深度 O(log n)。

## 四种写法对比

| 写法 | 解决的问题 | 记忆点 |
|---|---|---|
| Lomuto | 最好写 | 主元在末尾，i 是「小于区」的边界 |
| Hoare | 交换少，重复元素也能均匀划分 | 两个指针相向，`i <= j` 时交换；递归 [lo, j] 和 [i, hi] |
| 三路划分 | 大量重复元素 | lt、i、gt 三个指针；和 gt 交换后 i 不动 |
| 随机 + 短边递归 | 有序输入、栈溢出 | 随机下标换到末尾；循环处理长的一边 |

## 易错点

- Hoare 写法递归成 `sort(lo, i − 1)` 和 `sort(i, hi)`，或者内层 while 用 `<=`：会越界或死循环。
- Lomuto 里比较用 `<=`：全部相等时每次划分都极不均匀，退化成 O(n²)。
- 三路划分和 gt 交换后把 i 也右移了：换过来的元素没被检查。
- 只说「快排 O(n log n)」：要说清楚是平均，最坏 O(n²)，以及怎么避免。

## 面试追问

- **快排稳定吗？** 不稳定：交换会打乱相等元素的相对顺序。
- **为什么实际中快排通常比归并快？** 原地、顺序访问内存、缓存友好；归并需要额外数组和拷贝。
- **JDK 的 `Arrays.sort` 用的什么？** 基本类型用双轴快排（两个主元，分三段）；对象数组用 TimSort（归并 + 插入排序，稳定）。小数组（几十个元素以下）都改用插入排序。
- **只要第 k 大？** 快速选择：划分后只递归一边，期望 O(n)，见 [215](./lc215)。
- **颜色分类（75）？** 就是三路划分，主元固定为 1，见 [75](../01-array-two-pointers/lc75)。

## Java 版（随机主元 + 三路划分）

```java
public void quickSort(int[] a) {
    sort(a, 0, a.length - 1);
}

private void sort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int k = ThreadLocalRandom.current().nextInt(lo, hi + 1);   // 随机主元
    swap(a, lo, k);
    int pivot = a[lo], lt = lo, i = lo, gt = hi;               // 三路划分
    while (i <= gt) {
        if (a[i] < pivot) swap(a, lt++, i++);
        else if (a[i] > pivot) swap(a, i, gt--);
        else i++;
    }
    sort(a, lo, lt - 1);
    sort(a, gt + 1, hi);
}

private void swap(int[] a, int i, int j) {
    int t = a[i]; a[i] = a[j]; a[j] = t;
}
```

## 相关题

- [215. 数组中的第 K 个最大元素](./lc215)
- [75. 颜色分类](../01-array-two-pointers/lc75)
- [归并排序](./merge-sort)
- [堆排序](./heap-sort)
