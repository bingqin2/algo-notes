---
title: "7. 整数反转"
lc: 7
slug: reverse-integer
difficulty: 中等
tier: C
source: "题型补强"
status: done
---
# 7. 整数反转

> [力扣 7](https://leetcode.cn/problems/reverse-integer/) · 中等 · 来源：题型补强
>
> C 层：认得题型，说得出方法和关键点

## 识别信号

反转整数，超出 32 位范围返回 0，而且假设环境不能存 64 位整数：每次乘 10 之前先判断会不会溢出。

## 关键点

- 条件 `res > (INT_MAX − d) // 10` 时乘 10 加 d 就会溢出。常见写法 `res > INT_MAX / 10` 也对：res 正好等于 INT_MAX / 10 时，原数是 10 位且最高位只能是 1 或 2，d 不会超过 7。
- Python 用绝对值处理再补符号；Java 里 `%` 对负数返回负数，可以不取绝对值，正负分别判断上下界。

```python
def reverse(x):
    INT_MAX = 2 ** 31 - 1
    sign = -1 if x < 0 else 1
    x, res = abs(x), 0
    while x:
        d = x % 10
        x //= 10
        if res > (INT_MAX - d) // 10:      # 乘 10 加 d 之前判断会不会溢出
            return 0
        res = res * 10 + d
    return sign * res
```

相关：[8. 字符串转换整数](./lc8)、[9. 回文数](./lc9)
