"""206. 反转链表：迭代 + 递归两种解法的执行过程。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from viz import Trace, build  # noqa: E402


def iterative():
    t = Trace("lc206-iter", "206 反转链表 · 迭代（三指针）")
    head, nodes = build([1, 2, 3, 4, 5])
    prev, cur = None, head
    t.list(nodes, {"prev": prev, "cur": cur}, "初始：prev = ∅，cur = head。目标是把每条 next 掉头。")
    while cur:
        nxt = cur.next
        t.list(nodes, {"prev": prev, "cur": cur, "nxt": nxt}, f"先用 nxt 记住 {cur.val} 的下一个结点，否则掉头后就找不回来了。", hl=[cur])
        cur.next = prev
        t.list(nodes, {"prev": prev, "cur": cur, "nxt": nxt}, f"cur.next = prev：{cur.val} 的指针掉头，指向 {prev.val if prev else '∅'}。", hl=[cur])
        prev, cur = cur, nxt
        t.list(nodes, {"prev": prev, "cur": cur}, "prev、cur 各前进一步。")
    t.list(nodes, {"prev(新头)": prev, "cur": cur}, "cur 走到 ∅，循环结束，prev 就是新的头结点。")
    t.save()


def recursive():
    t = Trace("lc206-rec", "206 反转链表 · 递归（后序）")
    head, nodes = build([1, 2, 3, 4, 5])

    def rev(node, depth):
        if node is None or node.next is None:
            t.list(nodes, {"node": node}, f"递归到底：{node.val} 是最后一个结点，直接返回它作为新头。", hl=[node])
            return node
        t.list(nodes, {"node": node}, f"第 {depth} 层：先把 {node.val} 后面的部分整体反转（递归下去）。", hl=[node])
        new_head = rev(node.next, depth + 1)
        node.next.next = node
        t.list(nodes, {"node": node, "newHead": new_head}, f"回到第 {depth} 层：node.next.next = node，让 {node.next.val} 指回 {node.val}。", hl=[node, node.next])
        node.next = None
        t.list(nodes, {"node": node, "newHead": new_head}, f"node.next = ∅，断开 {node.val} 原来向后的指针，避免成环。", hl=[node])
        return new_head

    rev(head, 1)
    t.save()


if __name__ == "__main__":
    iterative()
    recursive()
