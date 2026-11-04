---
title: "5. 最长回文子串"
lc: 5
slug: longest-palindromic-substring
difficulty: 中等
tier: A
source: "Hot 100"
asked: "字节 ×2"
status: done
---
# 5. 最长回文子串

> [力扣 5](https://leetcode.cn/problems/longest-palindromic-substring/) · 近两年面经里出现在：**字节 ×2**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

最长回文子串（必须连续）。字节考了 2 次。要掌握三种：中心扩展（面试首选）、区间 DP（考 DP 思维）、Manacher（追问「能不能 O(n)」时说思路）。

## 解法一：中心扩展（面试首选）

**思路**：回文从中心向两边对称。枚举每个中心，向两边扩展到不再相等为止。中心有两种：一个字符（奇数长度）和两个字符之间（偶数长度）。

<StepPlayer src="/viz/lc5.json" />

```python
def longestPalindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l, r = l - 1, r + 1
        return l + 1, r            # 回文是 s[l+1:r]
    best = (0, 1)
    for i in range(len(s)):
        for l, r in (expand(i, i), expand(i, i + 1)):   # 奇数长度、偶数长度
            if r - l > best[1] - best[0]: best = (l, r)
    return s[best[0]:best[1]]
```

**复杂度**：时间 O(n²)，空间 O(1)。

## 解法二：区间 DP

**思路**：dp[i][j] = s[i..j] 是不是回文。如果 s[i] == s[j]，并且里面的 s[i+1..j−1] 是回文（或者长度不超过 3），那 s[i..j] 就是回文。

dp[i][j] 依赖 dp[i+1][j−1]（左下方），所以 i 要**从大到小**遍历。

```python
def longestPalindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, length = 0, 1
    for i in range(n - 1, -1, -1):        # i 从后往前，保证 dp[i+1][j-1] 已经算过
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 3 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if j - i + 1 > length: start, length = i, j - i + 1
    return s[start:start + length]
```

**复杂度**：时间 O(n²)，空间 O(n²)。

## 解法三：Manacher，O(n)

**思路**：

1. 在字符之间插入 `#`，把奇偶两种中心统一成一种。
2. p[i] = 以 i 为中心的回文半径。
3. 记录目前向右延伸最远的回文 [center − p, right]。如果 i 在它里面，i 关于 center 的对称点 j = 2·center − i 的回文半径可以直接借用（不超过 right − i），然后再继续往外扩展。

right 只会往右移动，所以总时间是 O(n)。

```python
def longestPalindrome(s):
    t = "#" + "#".join(s) + "#"
    n = len(t); p = [0] * n        # p[i]：以 i 为中心的回文半径（不含中心）
    center = right = 0
    for i in range(n):
        if i < right: p[i] = min(right - i, p[2 * center - i])   # 利用对称性
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1
        if i + p[i] > right: center, right = i, i + p[i]
    i = max(range(n), key=lambda k: p[k])
    start = (i - p[i]) // 2
    return s[start:start + p[i]]
```

**复杂度**：时间 O(n)，空间 O(n)。面试时讲清楚「利用对称性 + right 单调右移」就够了。

## 三种解法对比

| 解法 | 时间 | 空间 | 什么时候用 |
|---|---|---|---|
| 中心扩展 | O(n²) | O(1) | 默认写这个 |
| 区间 DP | O(n²) | O(n²) | 面试官想考 DP，或者后续要查询「任意子串是不是回文」（如 [131](/10-backtracking/lc131)） |
| Manacher | O(n) | O(n) | 追问最优复杂度时讲思路 |

## 易错点

- 只考虑了奇数长度的中心，`"cbbd"` 会得到 `"c"` 而不是 `"bb"`。
- 区间 DP 的遍历顺序错了，用到了还没算的 dp[i+1][j−1]。
- 子串和子序列混淆：最长回文**子序列**是 [516](./lc516)，状态转移不同。

## 面试追问

- **统计回文子串的个数？** [647](./lc647)：中心扩展时每扩展成功一次就计数加一。
- **最长回文子序列？** [516](./lc516)：dp[i][j] = s[i] == s[j] ? dp[i+1][j−1] + 2 : max(dp[i+1][j], dp[i][j−1])。
- **至少添加几个字符变成回文？** 等于 n 减去最长回文子序列的长度。

## Java 版

```java
public String longestPalindrome(String s) {
    int start = 0, end = 0;                  // 最长回文是 s[start, end)
    for (int i = 0; i < s.length(); i++) {
        for (int k = 0; k < 2; k++) {        // k = 0：奇数长度；k = 1：偶数长度
            int l = i, r = i + k;
            while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
            if (r - l - 1 > end - start) { start = l + 1; end = r; }
        }
    }
    return s.substring(start, end);
}
```

## 相关题

- [647. 回文子串](./lc647)
- [516. 最长回文子序列](./lc516)
- [131. 分割回文串](/10-backtracking/lc131)
