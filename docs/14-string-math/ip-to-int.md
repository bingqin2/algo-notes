---
title: "IP 地址与 32 位整数互转"
difficulty: 手写
tier: A
source: "手写"
asked: "腾讯 ×2"
status: done
---
# IP 地址与 32 位整数互转 / IP+端口打包成 64 位

> 非力扣原题，面试手写题 · 近两年面经里出现在：**腾讯 ×2**
>
> A 层：所有常见解法都要会，闭卷写出，能讲清追问

## 识别信号

IPv4 地址是 4 个 0~255 的数，每个正好 8 位，拼起来就是一个 32 位无符号整数。转换就是**移位和按位或**：`a << 24 | b << 16 | c << 8 | d`。面试的重点在**校验非法输入**和 **Java 没有无符号 int**。

## 解法一：按点分割 + 位移

**思路**：

- IP → 整数：按 `.` 分成 4 段，从左到右每段 `res = res << 8 | 段值`。
- 整数 → IP：依次取 `x >> 24`、`x >> 16`、`x >> 8`、`x` 的低 8 位（`& 0xFF`），用 `.` 连起来。

例：`192.168.1.1` = 192 × 2²⁴ + 168 × 2¹⁶ + 1 × 2⁸ + 1 = 3232235777。

```python
def ip_to_int(ip):
    res = 0
    for part in ip.split("."):
        res = res << 8 | int(part)
    return res
```

```python
def int_to_ip(x):
    return ".".join(str(x >> s & 0xFF) for s in (24, 16, 8, 0))
```

**复杂度**：O(1)（长度固定）。

## 解法二：校验非法输入

面试官会故意给各种坏输入，要逐条检查：

| 输入 | 问题 |
|---|---|
| `1.2.3`、`1.2.3.4.5` | 段数不是 4 |
| `1..2.3`、`1.2.3.` | 有空段 |
| `256.1.1.1` | 超过 255 |
| `01.1.1.1` | 前导 0（有些系统会当成八进制，一般规定不允许） |
| `1.2.3.a`、`+1.2.3.4`、` 1.2.3.4` | 有非数字字符（`int()` 会接受 `+1` 和空格，所以要自己逐字符检查） |

```python
def ip_to_int_strict(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError("必须是 4 段")
    res = 0
    for p in parts:
        if not p or len(p) > 3 or not all("0" <= c <= "9" for c in p):
            raise ValueError(f"非法段 {p!r}")
        if len(p) > 1 and p[0] == "0":
            raise ValueError(f"有前导 0：{p!r}")
        v = int(p)
        if v > 255:
            raise ValueError(f"超过 255：{p!r}")
        res = res << 8 | v
    return res
```

## 追问：IP + 端口打包成 64 位

端口是 0~65535，16 位。把 IP 放在高位、端口放在低 16 位，`ip << 16 | port`，一共 48 位，放进一个 64 位整数里。可以用来做哈希表的 key（比如连接表），比字符串 `"ip:port"` 省空间、比较也快。

```python
def pack(ip, port):
    if not 0 <= port <= 0xFFFF:
        raise ValueError("端口必须在 0~65535")
    return ip_to_int_strict(ip) << 16 | port   # 高 32 位 IP，低 16 位端口
```

```python
def unpack(x):
    return int_to_ip(x >> 16 & 0xFFFFFFFF), x & 0xFFFF
```

## 易错点

- **Java 用 int 存**：`200.0.0.0` 以上的 IP 大于 2³¹ − 1，int 会变成负数。用 long，或者用 int 存但输出时 `Integer.toUnsignedLong`。
- Java 里 `"1.2.3.".split("\\.")` 返回 3 段（末尾的空串被丢掉），要传 `limit = -1` 才能发现末尾的空段。
- 右移用 `>>`，long 的值是负数时会补 1：用 `>>>` 或者先 `& 0xFF`。
- 运算符优先级：Java 里 `<<` 比 `|` 优先级高，`res << 8 | v` 没问题；但 `+` 比 `<<` 高，`a << 8 + b` 是 `a << (8 + b)`。

## 面试追问

- **怎么判断一个 IP 是否在某个网段（CIDR，比如 `10.0.0.0/8`）里？** 掩码 `mask = ~0 << (32 − 8)`（取低 32 位），判断 `(ip & mask) == (网段 & mask)`。
- **大量 IP 段，查一个 IP 属于哪个段（IP 归属地查询）？** 把每段转成 [起始整数, 结束整数]，按起点排序，二分查找。
- **网络字节序？** 网络上传输用大端（高位在前），x86 是小端，C 里要用 `htonl` / `ntohl` 转换。
- **IPv6？** 128 位，Java 用两个 long 或 BigInteger；地址里还有 `::` 缩写要展开。

## Java 版

```java
public static long ipToLong(String ip) {
    String[] parts = ip.split("\\.", -1);              // -1：保留末尾空串，"1.2.3." 才会报错
    if (parts.length != 4) throw new IllegalArgumentException("必须是 4 段");
    long res = 0;
    for (String p : parts) {
        if (p.isEmpty() || p.length() > 3) throw new IllegalArgumentException(p);
        for (char c : p.toCharArray()) if (c < '0' || c > '9') throw new IllegalArgumentException(p);
        if (p.length() > 1 && p.charAt(0) == '0') throw new IllegalArgumentException("前导 0：" + p);
        int v = Integer.parseInt(p);
        if (v > 255) throw new IllegalArgumentException(p);
        res = res << 8 | v;
    }
    return res;                                        // 用 long：int 存不下 > 2^31 的 IP
}

public static String longToIp(long x) {
    return (x >>> 24 & 0xFF) + "." + (x >>> 16 & 0xFF) + "." + (x >>> 8 & 0xFF) + "." + (x & 0xFF);
}

public static long pack(String ip, int port) {
    if (port < 0 || port > 0xFFFF) throw new IllegalArgumentException("端口");
    return ipToLong(ip) << 16 | port;
}

public static String unpack(long x) {
    return longToIp(x >>> 16 & 0xFFFFFFFFL) + ":" + (x & 0xFFFF);
}
```

## 相关题

- [93. 复原 IP 地址](https://leetcode.cn/problems/restore-ip-addresses/)：同样的校验规则 + 回溯
- [468. 验证IP地址](https://leetcode.cn/problems/validate-ip-address/)
- [190. 颠倒二进制位](./lc190)、[191. 位1的个数](./lc191)：位运算
