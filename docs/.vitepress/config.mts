import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { fileURLToPath } from 'node:url'
import { buildSidebar } from './sidebar'

const docsDir = fileURLToPath(new URL('..', import.meta.url))

export default withMermaid(
  defineConfig({
    lang: 'zh-CN',
    title: '算法图解库',
    description: '按数据结构整理核心题，每题所有解法 + 逐步可视化',
    base: process.env.BASE ?? '/',
    lastUpdated: true,
    cleanUrls: true,
    themeConfig: {
      nav: [{ text: '首页', link: '/' }],
      sidebar: buildSidebar(docsDir),
      outline: { level: [2, 3], label: '本页目录' },
      search: { provider: 'local' },
      docFooter: { prev: '上一篇', next: '下一篇' },
    },
    mermaid: {},
  }),
)
