"""链表 A 层题的执行过程：141/142、19、92、143。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import ListNode, Trace, build  # noqa: E402


def lc142():
    t = Trace("lc142", "141 / 142 环形链表 · 快慢指针")
    head, nodes = build([1, 2, 3, 4, 5, 6])
    nodes[-1].next = nodes[2]          # 6 → 3，入环点是 3
    slow = fast = head
    t.list(nodes, {"slow": slow, "fast": fast}, "6 指回 3，形成环。slow 每次走一步，fast 每次走两步。")
    while True:
        slow, fast = slow.next, fast.next.next
        t.list(nodes, {"slow": slow, "fast": fast}, f"slow 到 {slow.val}，fast 到 {fast.val}。", hl=[slow, fast])
        if slow is fast:
            t.list(nodes, {"slow=fast": slow}, f"在 {slow.val} 相遇，说明有环（141 到这里就可以返回 true）。", hl=[slow])
            break
    p = head
    t.list(nodes, {"p": p, "slow": slow}, "142：让 p 从头出发，slow 从相遇点出发，两个都每次走一步。", hl=[p, slow])
    while p is not slow:
        p, slow = p.next, slow.next
        t.list(nodes, {"p": p, "slow": slow}, f"p 到 {p.val}，slow 到 {slow.val}。", hl=[p, slow])
    t.list(nodes, {"入环点": p}, f"再次相遇的 {p.val} 就是入环点。原因：头到入口的距离 = 相遇点再走到入口的距离（差整数圈）。", hl=[p])
    t.save()


def lc19():
    t = Trace("lc19", "19 删除倒数第 N 个结点 · n = 2")
    _, rest = build([1, 2, 3, 4, 5])
    dummy = ListNode("D", rest[0])
    nodes = [dummy] + rest
    fast = slow = dummy
    t.list(nodes, {"fast": fast, "slow": slow}, "加哑结点，这样删除头结点也不用特判。fast 和 slow 都从哑结点出发。")
    for k in range(2):
        fast = fast.next
        t.list(nodes, {"fast": fast, "slow": slow}, f"fast 先走 {k + 1} 步。", hl=[fast])
    while fast.next:
        fast, slow = fast.next, slow.next
        t.list(nodes, {"fast": fast, "slow": slow}, "两个一起走，始终相隔 n 步。", hl=[fast, slow])
    t.list(nodes, {"fast": fast, "slow": slow}, f"fast 到了最后一个结点，slow 正好在待删结点 {slow.next.val} 的前一个。", hl=[slow, slow.next])
    slow.next = slow.next.next
    t.list(nodes, {"slow": slow}, "slow.next = slow.next.next，删掉倒数第 2 个。", hl=[slow])
    t.save()


def lc92():
    t = Trace("lc92", "92 反转链表 II · left = 2，right = 5（头插法）")
    _, rest = build([1, 2, 3, 4, 5, 6])
    dummy = ListNode("D", rest[0])
    nodes = [dummy] + rest
    pre = dummy
    for _ in range(1):
        pre = pre.next
    cur = pre.next
    t.list(nodes, {"pre": pre, "cur": cur}, "pre 停在区间前一个结点（1），cur 是区间第一个结点（2）。cur 会一直指向 2，它最后会变成区间的尾巴。", hl=[pre, cur])
    for _ in range(5 - 2):
        nxt = cur.next
        t.list(nodes, {"pre": pre, "cur": cur, "nxt": nxt}, f"把 cur 后面的 {nxt.val} 摘下来。", hl=[nxt])
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
        t.list(nodes, {"pre": pre, "cur": cur, "nxt": nxt}, f"把 {nxt.val} 插到 pre 后面（头插）。", hl=[nxt])
    t.list(nodes, {"pre": pre, "cur": cur}, "做了 right − left 次头插，区间变成 5 4 3 2，一次遍历完成。")
    t.save()


def lc143():
    t = Trace("lc143", "143 重排链表 · 找中点 + 反转后半 + 交错合并")
    head, nodes = build([1, 2, 3, 4, 5, 6])
    slow = fast = head
    t.list(nodes, {"slow": slow, "fast": fast}, "第一步：快慢指针找中点。")
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
        t.list(nodes, {"slow": slow, "fast": fast}, "slow 走一步，fast 走两步。", hl=[slow, fast])
    second = slow.next
    slow.next = None
    t.list(nodes, {"前半尾": slow, "second": second}, f"slow 停在 {slow.val}，从这里断开：前半 1–{slow.val}，后半 {second.val}–6。", hl=[slow, second])
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next
    t.list(nodes, {"head": head, "后半新头": prev}, "第二步：用 206 的方法反转后半，得到 6 → 5 → 4。", hl=[prev])
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next, second.next = second, n1
        t.list(nodes, {"first": first, "second": second}, f"第三步：交错合并，{first.val} → {second.val} → {n1.val if n1 else '∅'}。", hl=[first, second])
        first, second = n1, n2
    t.list(nodes, {"head": head}, "完成：1 → 6 → 2 → 5 → 3 → 4。")
    t.save()


if __name__ == "__main__":
    lc142(); lc19(); lc92(); lc143()
