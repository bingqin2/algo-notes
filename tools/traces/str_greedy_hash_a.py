"""字符串与数学、贪心与区间、哈希与前缀和 A 层的执行过程。"""
import heapq
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace  # noqa: E402


def lc525():
    nums = [0, 1, 1, 0, 1, 1, 1, 0]
    t = Trace("lc525", "525 连续数组 · 0 当成 -1 的前缀和")
    first = {0: -1}
    best = s = 0
    fmt = lambda: "first = {" + ", ".join(f"{k}: {v}" for k, v in first.items()) + "}"
    t.array(nums, {}, "把 0 看成 -1，「0 和 1 一样多」就变成「子数组和为 0」。前缀和 s 在 j 和 i 处相等，(j, i] 这段的和就是 0。", extra=f"s = 0，{fmt()}，best = 0")
    for i, x in enumerate(nums):
        s += 1 if x == 1 else -1
        if s in first:
            j = first[s]
            best = max(best, i - j)
            t.array(nums, {"i": i}, f"nums[{i}] = {x}，s = {s}。s 在下标 {j} 出现过，({j}, {i}] 这段 0 和 1 一样多，长度 {i - j}。不更新 first[{s}]，保留最早的位置。", hl=[i], window=(j + 1, i), extra=f"s = {s}，{fmt()}，best = {best}")
        else:
            first[s] = i
            t.array(nums, {"i": i}, f"nums[{i}] = {x}，s = {s}。第一次出现，记下 first[{s}] = {i}。", hl=[i], extra=f"s = {s}，{fmt()}，best = {best}")
    t.array(nums, {}, f"答案 {best}。一次遍历，O(n) 时间，哈希表最多 n + 1 个前缀和。", extra=f"best = {best}")
    t.save()


def lc128():
    nums = [100, 4, 200, 1, 3, 2]
    s = set(nums)
    t = Trace("lc128", "128 最长连续序列 · 只从起点开始数")
    t.array(nums, {}, "先把所有数放进哈希集合。x − 1 不在集合里，x 才是一段连续序列的起点，只从起点往后数。", extra=f"set = {sorted(s)}")
    best = 0
    for i, x in enumerate(nums):
        if x - 1 in s:
            t.array(nums, {"x": i}, f"{x} − 1 = {x - 1} 在集合里，{x} 不是起点，跳过。", hl=[i], extra=f"best = {best}")
            continue
        y = x
        while y + 1 in s:
            y += 1
        best = max(best, y - x + 1)
        run = [nums.index(v) for v in range(x, y + 1)]
        t.array(nums, {"x": i}, f"{x} 是起点，往后数 {x}…{y}，长度 {y - x + 1}。", hl=run, extra=f"best = {best}")
    t.array(nums, {}, f"答案 {best}。每个数最多在「往后数」里被访问一次（只有起点会开始数），总共 O(n)。", extra=f"best = {best}")
    t.save()


def lc56():
    iv = [[1, 3], [8, 10], [2, 6], [15, 18], [9, 12], [17, 20]]
    t = Trace("lc56", "56 合并区间 · 按起点排序")
    cells = lambda a: [f"{s},{e}" for s, e in a]
    t.array(cells(iv), {}, "先按起点排序。排完以后，能和当前区间重叠的只可能是结果里最后一个区间。", extra="res = []")
    iv.sort()
    t.array(cells(iv), {}, "排序后从左到右扫。", extra="res = []")
    res = []
    for i, (s, e) in enumerate(iv):
        if res and s <= res[-1][1]:
            old = res[-1][:]
            res[-1][1] = max(res[-1][1], e)
            msg = f"[{s},{e}] 的起点 {s} ≤ 上一个的终点 {old[1]}，重叠，合并成 {res[-1]}。"
        else:
            res.append([s, e])
            msg = f"[{s},{e}] 和上一个不重叠（或者 res 为空），直接放进结果。"
        t.array(cells(iv), {"i": i}, msg, hl=[i], extra=f"res = {res}")
    t.array(cells(iv), {}, f"结果 {res}。排序 O(n log n)，扫描 O(n)。", extra=f"res = {res}")
    t.save()


def lc871():
    target, fuel, st = 100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]
    t = Trace("lc871", "871 最低加油次数 · 大顶堆（格子里是「位置/油量」）")
    cells = [f"{p}/{f}" for p, f in st]
    heap, reach, i, stops = [], fuel, 0, 0
    ex = lambda: f"reach = {reach}，堆 = {sorted(-x for x in heap)[::-1]}，stops = {stops}"
    t.array(cells, {}, f"目标 {target}，初始油 {fuel}。换个想法：开过的加油站都先「存着」，真没油了，再回头从存着的里面挑油最多的加一次。", extra=ex())
    while reach < target:
        passed = []
        while i < len(st) and st[i][0] <= reach:
            heapq.heappush(heap, -st[i][1])
            passed.append(i)
            i += 1
        if passed:
            t.array(cells, {}, f"用现有的油最远到 {reach}，路过加油站 " + "、".join(str(st[k][0]) for k in passed) + "，油量先放进堆里。", hl=passed, extra=ex())
        if not heap:
            t.array(cells, {}, "堆空了还到不了终点，返回 -1。", extra=ex())
            break
        g = -heapq.heappop(heap)
        reach += g
        stops += 1
        t.array(cells, {}, f"到 {reach - g} 就没油了，从堆里取最多的 {g} 加上，最远到 {reach}。加油次数 {stops}。", extra=ex())
    t.array(cells, {}, f"reach = {reach} ≥ {target}，答案 {stops}。每个站进出堆各一次，O(n log n)。", extra=ex())
    t.save()


def lc253():
    iv = [[0, 30], [5, 10], [15, 20], [10, 25], [26, 35]]
    iv.sort()
    t = Trace("lc253", "253 会议室 II · 小顶堆存结束时间")
    cells = [f"{s},{e}" for s, e in iv]
    ends = []
    t.array(cells, {}, "按开始时间排序。堆里放每间正在用的会议室什么时候空出来，堆顶是最早空出来的那间。", extra="堆 = []，房间数 = 0")
    for i, (s, e) in enumerate(iv):
        if ends and ends[0] <= s:
            old = ends[0]
            heapq.heapreplace(ends, e)
            msg = f"[{s},{e}] 开始时，最早空出来的房间 {old} 点就空了（{old} ≤ {s}），复用这一间，结束时间改成 {e}。"
        else:
            msg = f"[{s},{e}] 开始时没有空房间" + (f"（最早 {ends[0]} 点才空）" if ends else "") + "，新开一间。"
            heapq.heappush(ends, e)
        t.array(cells, {"i": i}, msg, hl=[i], extra=f"堆 = {sorted(ends)}，房间数 = {len(ends)}")
    t.array(cells, {}, f"堆的大小就是同时需要的最多房间数：{len(ends)}。O(n log n)。", extra=f"房间数 = {len(ends)}")
    t.save()


def lc470():
    t = Trace("lc470", "470 用 Rand7 实现 Rand10 · 拒绝采样")
    raw = [[r * 7 + c + 1 for c in range(7)] for r in range(7)]
    t.grid(raw, "调用两次 rand7：第一次选行，第二次选列。49 个格子每个概率都是 1/49，格子里写的是 (行−1)×7 + 列。")
    mapped = [[(v - 1) % 10 + 1 if v <= 40 else "×" for v in row] for row in raw]
    tone = [[4 if v > 40 else 0 for v in row] for row in raw]
    t.grid(mapped, "只用前 40 个格子，按 (x−1) % 10 + 1 映射到 1..10；41..49 拒绝（红色），重新来。", tone=tone)
    hl = [(r, c) for r in range(7) for c in range(7) if raw[r][c] <= 40 and (raw[r][c] - 1) % 10 + 1 == 3]
    t.grid(mapped, "每个数字正好对应 4 个格子，比如 3 对应这 4 格。所以每个数字的概率都是 4/40 = 1/10。", hl=hl, tone=tone)
    tone2 = [[4 if v > 40 else (1 if v <= 40 else 0) for v in row] for row in raw]
    t.grid(mapped, "每一轮成功概率 40/49，期望 49/40 ≈ 1.23 轮，也就是平均 2.45 次 rand7。被拒绝的 9 个格子本身也是均匀的 1..9，可以接着利用，见页面里的优化写法。", tone=tone2)
    t.save()


def lc415():
    a, b = "4567", "789"
    n = max(len(a), len(b)) + 1
    pad = lambda s: [""] * (n - len(s)) + list(s)
    t = Trace("lc415", "415 字符串相加 · 从低位模拟进位")
    res = [""] * n
    t.grid([pad(a), pad(b), res], "两个指针从末尾往前走，一位一位加，记住进位。第三行是结果。", extra="carry = 0")
    i, j, carry, k = len(a) - 1, len(b) - 1, 0, n - 1
    while i >= 0 or j >= 0 or carry:
        x = int(a[i]) if i >= 0 else 0
        y = int(b[j]) if j >= 0 else 0
        s = x + y + carry
        res[k] = str(s % 10)
        t.grid([pad(a), pad(b), res], f"{x} + {y} + 进位 {carry} = {s}，这一位写 {s % 10}，进位 {s // 10}。" + ("（有一边已经走完，当 0 算）" if i < 0 or j < 0 else ""), hl=[(0, k), (1, k), (2, k)], extra=f"carry = {s // 10}")
        carry = s // 10
        i, j, k = i - 1, j - 1, k - 1
    t.grid([pad(a), pad(b), res], f"两个指针都走完、进位也是 0 才停。结果 {''.join(res)}，O(max(m, n))。", extra="carry = 0")
    t.save()


def lc43():
    a, b = "123", "45"
    m, n = len(a), len(b)
    pos = [0] * (m + n)
    t = Trace("lc43", "43 字符串相乘 · a[i] × b[j] 落在 pos[i+j] 和 pos[i+j+1]")
    rows = lambda: [[""] * n + list(a), [""] * m + list(b), pos[:]]
    t.grid(rows(), "结果最多 m + n 位（第三行）。a 的第 i 位乘 b 的第 j 位，乘积的个位在 pos[i+j+1]，进位加到 pos[i+j]。前两行右对齐只是为了好看。", extra="pos = " + str(pos))
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            p = int(a[i]) * int(b[j]) + pos[i + j + 1]
            old = pos[i + j + 1]
            pos[i + j + 1] = p % 10
            pos[i + j] += p // 10
            t.grid(rows(), f"a[{i}] × b[{j}] = {a[i]} × {b[j]} = {int(a[i]) * int(b[j])}，加上 pos[{i + j + 1}] 原来的 {old} 得 {p}：pos[{i + j + 1}] = {p % 10}，pos[{i + j}] += {p // 10}。", hl=[(0, n + i), (1, m + j), (2, i + j), (2, i + j + 1)], extra="pos = " + str(pos))
    t.grid(rows(), f"去掉前导 0：{''.join(map(str, pos)).lstrip('0')}（123 × 45 = 5535）。O(mn)。", extra="pos = " + str(pos))
    t.save()


def lc50():
    x0, n = 3, 13
    bits = [int(c) for c in reversed(bin(n)[2:])]
    t = Trace("lc50", f"50 Pow(x, n) · 迭代快速幂，算 3^13（13 = 0b1101）")
    t.array(bits, {}, "把 n 写成二进制（格子从低位到高位）。3^13 = 3^8 × 3^4 × 3^1：只要乘上二进制位是 1 的那些 3^(2^k)。", extra="res = 1，x = 3")
    res, x = 1, x0
    for k, bit in enumerate(bits):
        if bit:
            res *= x
            msg = f"第 {k} 位是 1，res 乘上 x = 3^{2 ** k} = {x}，res = {res}。"
        else:
            msg = f"第 {k} 位是 0，res 不变。"
        x2 = x * x
        t.array(bits, {"k": k}, msg + f" 然后 x 自乘：3^{2 ** (k + 1)} = {x2}。", hl=[k], extra=f"res = {res}，x = {x2}")
        x = x2
    t.array(bits, {}, f"res = {res} = 3^13。循环次数是 n 的二进制位数，O(log n)。", extra=f"res = {res}")
    t.save()


def lc443():
    chars = list("aa") + list("b" * 12) + ["c"]
    t = Trace("lc443", "443 压缩字符串 · 读写双指针")
    t.array(chars, {"read": 0, "write": 0}, "read 找一段相同字符的结尾，write 往前面写压缩结果。write 永远不会超过 read，所以能原地写。", extra="")
    write = read = 0
    n = len(chars)
    while read < n:
        start = read
        while read < n and chars[read] == chars[start]:
            read += 1
        cnt = read - start
        t.array(chars, {"start": start, "read": min(read, n - 1) if read < n else n - 1, "write": write}, f"从 {start} 开始的一段 '{chars[start]}' 有 {cnt} 个" + ("（read 到了末尾）" if read == n else f"，read 停在 {read}") + "。", window=(start, read - 1), extra=f"write = {write}")
        hl = [write]
        chars[write] = chars[start]
        write += 1
        if cnt > 1:
            for d in str(cnt):
                chars[write] = d
                hl.append(write)
                write += 1
        t.array(chars, {"write": write if write < n else n - 1}, f"写入 '{chars[start]}'" + (f" 和次数 {''.join(str(cnt))}（多位数要一位一位写）" if cnt > 1 else "（只有 1 个不写次数）") + f"，write 移到 {write}。", hl=hl, extra=f"write = {write}")
    t.array(chars, {}, f"返回 write = {write}，前 {write} 个就是压缩结果 {''.join(chars[:write])}。O(n) 时间，O(1) 额外空间。", window=(0, write - 1), extra=f"返回 {write}")
    t.save()


def lc384():
    a = [1, 2, 3, 4, 5]
    rng = random.Random(4)
    t = Trace("lc384", "384 打乱数组 · Fisher–Yates")
    n = len(a)
    t.array(a, {}, "从最后一个位置往前：在 [0, i] 里随机选一个 j，和 i 交换，位置 i 就定下来了。框出来的是可选范围。", extra="")
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        a[i], a[j] = a[j], a[i]
        t.array(a, {"i": i, "j": j}, f"在 [0, {i}] 里选到 j = {j}，交换 a[{i}] 和 a[{j}]。现在 a[{i}] = {a[i]}：剩下 {i + 1} 个数里每个落到这里的概率都是 1/{i + 1}。" if i != j else f"在 [0, {i}] 里选到 j = {i} 自己，不动（这也是一种可能，不能漏）。", hl=[i, j], window=(0, i), extra=f"已定下：下标 {i}..{n - 1}")
    t.array(a, {}, f"结果 {a}。一共 n × (n−1) × … × 1 = n! 种等可能的选择路径，正好对应 n! 种排列，每种 1/n!。", extra="")
    t.save()


if __name__ == "__main__":
    for f in (lc525, lc128, lc56, lc871, lc253, lc470, lc415, lc43, lc50, lc443, lc384):
        f()
