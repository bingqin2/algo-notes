# algo-notes：算法图解库

网页版（带动画）：https://bingqin2.github.io/algo-notes/

按数据结构和题型整理的面试核心题，每题所有解法 + 逐步可视化。网站用 VitePress 搭建，Markdown 在 GitHub 上也能直接读（动画需要在网站里看）。

## 本地运行

```bash
npm install
npm run dev
```

## 加一段动画

1. 在 `tools/traces/` 新建脚本，参考 `lc206.py`：在解法的关键步骤调用 `t.list(...)`（链表）或 `t.array(...)`（数组/字符串）。
2. 运行 `python3 tools/traces/你的脚本.py`，生成 `docs/public/viz/名字.json`。
3. 在题目页里写 `<StepPlayer src="/viz/名字.json" />`。

## 目录

- `docs/00-sorting/` … `docs/14-string-math/`：每个章节一个文件夹，`index.md` 是框架和题目表，其余每题一页
- `docs/.vitepress/theme/StepPlayer.vue`：播放组件
- `tools/viz.py`：记录执行过程的小工具
