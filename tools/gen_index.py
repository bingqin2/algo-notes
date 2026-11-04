"""根据题目页的 frontmatter 重新生成：
- 每个章节 index.md 里「核心题目」以下的部分（上面手写的「核心框架」保留）
- docs/core300.md 总览和进度

改了题目页的 status（todo → done）或 tier 之后运行：python3 tools/gen_index.py
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
MARK = "<!-- 以下由 tools/gen_index.py 生成，不要手改 -->"
TIERS = {"A": "A 层 · 面经高频", "B": "B 层 · 必会", "C": "C 层 · 认得题型"}
TIER_RULE = {
    "A": "所有常见解法都要会，闭卷写出，能讲清追问。每周轮一遍。",
    "B": "掌握最优解法，20 分钟内写出。每两周一遍。",
    "C": "看到题能说出用什么方法、难点在哪。考前过一遍。",
}


def fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    d = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            d[k.strip()] = v.strip().strip('"')
    return d


def sort_key(p):
    return (p["tier"], int(p.get("lc", 10**6)), p["file"])


chapters = sorted(d for d in DOCS.iterdir() if d.is_dir() and re.match(r"\d\d-", d.name))
allp = []
for ch in chapters:
    idx = ch / "index.md"
    name = re.search(r"^#\s+(.+)$", idx.read_text(), re.M).group(1)
    probs = []
    for f in ch.glob("*.md"):
        if f.name == "index.md":
            continue
        d = fm(f.read_text())
        d.update(file=f.stem, chapter=ch.name, chname=name)
        probs.append(d)
    probs.sort(key=sort_key)
    allp += probs

    def row(p):
        done = "✅" if p.get("status") == "done" else ""
        return f"| [{p['title']}](./{p['file']}) | {p['tier']} | {p.get('difficulty', '')} | {p.get('source', '')} | {p.get('asked', '')} | {done} |"

    body = []
    for t in "ABC":
        rows = [row(p) for p in probs if p["tier"] == t]
        if rows:
            body.append(f"### {TIERS[t]}（{len(rows)} 题）\n\n| 题目 | 层级 | 难度 | 来源 | 近两年面经 | 完成 |\n|---|---|---|---|---|---|\n" + "\n".join(rows))
    done = sum(p.get("status") == "done" for p in probs)
    text = idx.read_text()
    head = text.split(MARK)[0] if MARK in text else re.split(r"^## 核心题目", text, flags=re.M)[0]
    idx.write_text(head.rstrip() + f"\n\n{MARK}\n\n## 核心题目\n\n本章 {len(probs)} 题，已完成 {done} 题。层级和来源的含义见[核心 300 题](/core300)。\n\n" + "\n\n".join(body) + "\n")

# ---------- 总览 ----------
by_tier = Counter(p["tier"] for p in allp)
done_tier = Counter(p["tier"] for p in allp if p.get("status") == "done")
src = Counter()
for p in allp:
    src[p.get("source", "").split(" · ")[0]] += 1
by_ch = defaultdict(Counter)
for p in allp:
    by_ch[(p["chapter"], p["chname"])][p["tier"]] += 1

out = [f"""# 核心 300 题

一共 **{len(allp)}** 题，包含完整的 LeetCode 热题 100。每题一个页面，按章节归类，按层级决定投入多少。

## 进度

| 层级 | 要求 | 题数 | 已完成 |
|---|---|---|---|"""]
for t in "ABC":
    out.append(f"| {TIERS[t]} | {TIER_RULE[t]} | {by_tier[t]} | {done_tier[t]} |")
out.append(f"| **合计** | | **{len(allp)}** | **{sum(done_tier.values())}** |")
out.append("""
## 300 题是怎么来的

| 来源 | 题数 | 说明 |
|---|---|---|""")
desc = {
    "Hot 100": "力扣「LeetCode 热题 100」全部收录",
    "面试经典 150": "力扣「面试经典 150 题」里不在 Hot 100 的题",
    "面经": "近两年后端面经里出现、但不在上面两张题单里的题",
    "手写": "非力扣原题，面试常让手写：排序、限流器、线程池、singleflight 等",
    "题型补强": "Hot 100 覆盖薄的题型：单调栈、二分答案、前缀和与差分、并查集、最短路、状态机 DP、背包、区间 DP 等",
}
for k in ["Hot 100", "面试经典 150", "面经", "手写", "题型补强"]:
    out.append(f"| {k} | {src[k]} | {desc[k]} |")
out.append("""
分层规则：近两年面经里出现过的题和手写题进 A 层，再补几道 Hot 100 里最经典的题；剩下的题里，简单题、非 Hot 100 的困难题和部分偏门的中等题进 C 层，其余进 B 层。

## 各章节分布

| 章节 | A | B | C | 合计 |
|---|---|---|---|---|""")
for (ch, name), c in sorted(by_ch.items()):
    out.append(f"| [{name}](/{ch}/) | {c['A']} | {c['B']} | {c['C']} | {sum(c.values())} |")
for t in "ABC":
    out.append(f"\n## {TIERS[t]}\n\n::: details 展开 {by_tier[t]} 道题\n\n| 题目 | 章节 | 难度 | 来源 | 完成 |\n|---|---|---|---|---|")
    for p in sorted((p for p in allp if p["tier"] == t), key=lambda p: (p["chapter"], int(p.get("lc", 10**6)))):
        out.append(f"| [{p['title']}](/{p['chapter']}/{p['file']}) | {p['chname']} | {p.get('difficulty', '')} | {p.get('source', '')} | {'✅' if p.get('status') == 'done' else ''} |")
    out.append("\n:::")
(DOCS / "core300.md").write_text("\n".join(out) + "\n")
print(f"{len(allp)} 题：", dict(by_tier), "已完成", sum(done_tier.values()))
