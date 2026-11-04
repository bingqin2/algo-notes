import fs from 'node:fs'
import path from 'node:path'

// 目录按文件夹名排序（01-xxx、02-xxx…），每个文件夹的 index.md 是章节总览。
// 标题取 frontmatter 的 title，没有就取第一个 # 标题。
export function titleOf(file: string): string {
  const s = fs.readFileSync(file, 'utf8')
  const fm = s.match(/^---\n([\s\S]*?)\n---/)
  if (fm) {
    const t = fm[1].match(/^title:\s*(.+)$/m)
    if (t) return t[1].trim().replace(/^["']|["']$/g, '')
  }
  const h = s.match(/^#\s+(.+)$/m)
  return h ? h[1].trim() : path.basename(file, '.md')
}

export function buildSidebar(docsDir: string) {
  const dirs = fs
    .readdirSync(docsDir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !e.name.startsWith('.') && e.name !== 'public')
    .filter((e) => fs.existsSync(path.join(docsDir, e.name, 'index.md')))
    .map((e) => e.name)
    .sort()
  return dirs.map((d) => {
    const dir = path.join(docsDir, d)
    const files = fs.readdirSync(dir).filter((f) => f.endsWith('.md') && f !== 'index.md').sort()
    return {
      text: titleOf(path.join(dir, 'index.md')),
      collapsed: true,
      items: [
        { text: '总览', link: `/${d}/` },
        ...files.map((f) => ({ text: titleOf(path.join(dir, f)), link: `/${d}/${f.replace(/\.md$/, '')}` })),
      ],
    }
  })
}
