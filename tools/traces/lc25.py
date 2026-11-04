"""25. K 个一组翻转链表（k = 2）的执行过程。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import ListNode, Trace, build  # noqa: E402


def main():
    t = Trace("lc25", "25 K 个一组翻转链表 · k = 2")
    _, rest = build([1, 2, 3, 4, 5])
    dummy = ListNode("D")
    dummy.next = rest[0]
    nodes = [dummy] + rest
    k = 2
    pre = dummy
    t.list(nodes, {"pre": pre}, "加一个哑结点 D，这样第一组和后面各组的处理完全一样。pre 指向「上一组的尾巴」。")
    while True:
        end = pre
        for _ in range(k):
            end = end.next
            if end is None:
                break
        if end is None:
            t.list(nodes, {"pre": pre}, "剩下的结点不足 k 个，保持原样，结束。", hl=[pre.next])
            break
        start, nxt = pre.next, end.next
        t.list(nodes, {"pre": pre, "start": start, "end": end, "nxt": nxt}, f"找到一组 [{start.val}..{end.val}]，nxt 记住下一组的开头。", hl=[start, end])
        end.next = None
        prev, cur = None, start
        while cur:
            n2 = cur.next
            cur.next = prev
            prev, cur = cur, n2
        t.list(nodes, {"pre": pre, "start": start, "end": end, "nxt": nxt}, "把这一组单独断开，用 206 的方法原地反转。现在 end 是组头，start 是组尾。", hl=[start, end])
        pre.next = end
        start.next = nxt
        t.list(nodes, {"pre": pre, "start": start, "end": end, "nxt": nxt}, "接回去：pre.next = end，start.next = nxt。", hl=[pre, start])
        pre = start
        t.list(nodes, {"pre": pre}, f"pre 移到这一组的尾巴 {start.val}，准备处理下一组。")
    t.save()


if __name__ == "__main__":
    main()
