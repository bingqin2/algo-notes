<script setup lang="ts">
// 逐步播放算法执行过程。帧数据由 tools/traces/*.py 生成，放在 docs/public/viz/*.json。
// 支持三种画面：kind = "list"（链表）、"array"（数组 + 指针 + 窗口）、"tree"（二叉树）。
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps<{ src: string }>()

type ListFrame = {
  kind: 'list'
  vals: (number | string)[]
  next: (number | null)[]
  ptr: Record<string, number>
  hl?: number[]
  note: string
}
type ArrayFrame = {
  kind: 'array'
  cells: (number | string)[]
  ptr: Record<string, number>
  hl?: number[]
  window?: [number, number] | null
  extra?: string
  note: string
}
type TreeFrame = {
  kind: 'tree'
  nodes: { id: number; val: number | string; x: number; d: number }[]
  edges: [number, number][]
  ptr: Record<string, number>
  hl?: number[]
  dim?: number[]
  marks?: Record<string, string>
  extra?: string
  note: string
}
type Frame = ListFrame | ArrayFrame | TreeFrame

const title = ref('')
const frames = ref<Frame[]>([])
const i = ref(0)
const playing = ref(false)
const error = ref('')
let timer: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  try {
    const r = await fetch(withBase(props.src))
    const data = await r.json()
    title.value = data.title
    frames.value = data.frames
  } catch (e) {
    error.value = `加载失败：${props.src}`
  }
})
onBeforeUnmount(stop)

const f = computed(() => frames.value[i.value])
const W = 84 // 每个格子的水平间距
const BOX = 52

function stop() {
  playing.value = false
  if (timer) clearInterval(timer)
  timer = null
}
function toggle() {
  if (playing.value) return stop()
  if (i.value >= frames.value.length - 1) i.value = 0
  playing.value = true
  timer = setInterval(() => {
    if (i.value < frames.value.length - 1) i.value++
    else stop()
  }, 1100)
}
function step(d: number) {
  stop()
  i.value = Math.min(frames.value.length - 1, Math.max(0, i.value + d))
}

// 同一位置可能有多个指针，按位置分组后竖着排
const ptrGroups = computed(() => {
  const g: Record<number, string[]> = {}
  if (!f.value) return g
  for (const [name, pos] of Object.entries(f.value.ptr)) (g[pos] ??= []).push(name)
  return g
})
const count = computed(() => {
  if (!f.value) return 0
  if (f.value.kind === 'tree') return 0
  return f.value.kind === 'list' ? f.value.vals.length : f.value.cells.length
})
const showNull = computed(() => f.value?.kind === 'list' && ptrGroups.value[count.value] !== undefined)
// 二叉树：x 是中序序号，d 是深度
const TW = 50
const treeMaxX = computed(() => (f.value?.kind === 'tree' ? Math.max(0, ...f.value.nodes.map((n) => n.x)) : 0))
const treeMaxD = computed(() => (f.value?.kind === 'tree' ? Math.max(0, ...f.value.nodes.map((n) => n.d)) : 0))
const tx = (n: { x: number }) => 36 + n.x * TW
const ty = (n: { d: number }) => 44 + n.d * 72
const treeNode = (id: number) => (f.value as TreeFrame).nodes.find((n) => n.id === id)!
const treePtr = computed(() => {
  const g: Record<number, string[]> = {}
  if (f.value?.kind !== 'tree') return g
  for (const [name, id] of Object.entries(f.value.ptr)) (g[id] ??= []).push(name)
  return g
})
const width = computed(() => (f.value?.kind === 'tree' ? 72 + treeMaxX.value * TW : 24 + (count.value + 1) * W))
const maxPtr = computed(() => Math.max(1, ...Object.values(ptrGroups.value).map((a) => a.length)))
const height = computed(() =>
  f.value?.kind === 'tree' ? 96 + treeMaxD.value * 72 + 18 * Math.max(1, ...Object.values(treePtr.value).map((a) => a.length)) : 150 + maxPtr.value * 18,
)

function x(k: number) {
  return 24 + k * W
}
const Y = 56

function edgePath(a: number, b: number) {
  const x1 = x(a) + BOX
  const x2 = x(b)
  if (b === a + 1) return `M ${x1} ${Y + BOX / 2} L ${x2 - 4} ${Y + BOX / 2}`
  if (b < a) {
    // 向左的指针画在下方
    const s = x(a) + BOX / 2
    const t = x(b) + BOX / 2
    return `M ${s} ${Y + BOX} C ${s} ${Y + BOX + 38}, ${t} ${Y + BOX + 38}, ${t} ${Y + BOX + 6}`
  }
  const s = x(a) + BOX / 2
  const t = x(b) + BOX / 2
  return `M ${s} ${Y} C ${s} ${Y - 40}, ${t} ${Y - 40}, ${t} ${Y - 6}`
}
</script>

<template>
  <div class="sp">
    <div v-if="error" class="sp-err">{{ error }}</div>
    <template v-else-if="f">
      <div class="sp-head">
        <strong>{{ title }}</strong>
        <span class="sp-count">第 {{ i + 1 }} / {{ frames.length }} 步</span>
      </div>
      <div class="sp-canvas">
        <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`" role="img" :aria-label="f.note">
          <defs>
            <marker id="sp-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" class="sp-arrowhead" />
            </marker>
          </defs>

          <!-- 二叉树 -->
          <template v-if="f.kind === 'tree'">
            <line
              v-for="([a, b], k) in f.edges"
              :key="'te' + k"
              :x1="tx(treeNode(a))" :y1="ty(treeNode(a))" :x2="tx(treeNode(b))" :y2="ty(treeNode(b))"
              class="sp-tedge"
            />
            <g v-for="n in f.nodes" :key="'tn' + n.id" :class="{ 'sp-dim': f.dim?.includes(n.id) }">
              <circle :cx="tx(n)" :cy="ty(n)" r="19" :class="['sp-box', { hl: f.hl?.includes(n.id) }]" />
              <text :x="tx(n)" :y="ty(n) + 6" class="sp-val">{{ n.val }}</text>
              <text v-if="f.marks?.[n.id]" :x="tx(n)" :y="ty(n) - 26" class="sp-mark">{{ f.marks[n.id] }}</text>
            </g>
            <template v-for="(names, id) in treePtr" :key="'tp' + id">
              <text v-for="(nm, r) in names" :key="nm" :x="tx(treeNode(Number(id)))" :y="ty(treeNode(Number(id))) + 36 + r * 16" class="sp-ptr">↑ {{ nm }}</text>
            </template>
          </template>

          <!-- 数组的窗口 -->
          <rect
            v-if="f.kind === 'array' && f.window"
            :x="x(f.window[0]) - 6"
            :y="Y - 6"
            :width="x(f.window[1]) - x(f.window[0]) + BOX + 12"
            :height="BOX + 12"
            rx="10"
            class="sp-window"
          />

          <!-- 链表的边 -->
          <template v-if="f.kind === 'list'">
            <template v-for="(nx, k) in f.next" :key="'e' + k">
              <path v-if="nx !== null" :d="edgePath(k, nx)" class="sp-edge" marker-end="url(#sp-arrow)" />
            </template>
          </template>

          <!-- 格子 -->
          <g v-for="k in count" :key="'n' + k">
            <rect :x="x(k - 1)" :y="Y" :width="BOX" :height="BOX" rx="8" :class="['sp-box', { hl: f.hl?.includes(k - 1) }]" />
            <text :x="x(k - 1) + BOX / 2" :y="Y + BOX / 2 + 6" class="sp-val">
              {{ f.kind === 'list' ? f.vals[k - 1] : f.cells[k - 1] }}
            </text>
            <text v-if="f.kind === 'array'" :x="x(k - 1) + BOX / 2" :y="Y - 10" class="sp-idx">{{ k - 1 }}</text>
          </g>
          <g v-if="showNull">
            <text :x="x(count) + BOX / 2" :y="Y + BOX / 2 + 6" class="sp-null">∅</text>
          </g>

          <!-- 指针标签（链表、数组） -->
          <template v-for="(names, pos) in (f.kind === 'tree' ? {} : ptrGroups)" :key="'p' + pos">
            <text
              v-for="(nm, r) in names"
              :key="nm"
              :x="x(Number(pos)) + BOX / 2"
              :y="Y + BOX + (f.kind === 'list' ? 58 : 24) + r * 18"
              class="sp-ptr"
            >
              ↑ {{ nm }}
            </text>
          </template>
        </svg>
      </div>
      <p class="sp-note">{{ f.note }}</p>
      <p v-if="f.kind !== 'list' && f.extra" class="sp-extra">{{ f.extra }}</p>
      <div class="sp-ctrl">
        <button @click="i = 0; stop()">⏮</button>
        <button @click="step(-1)">上一步</button>
        <button class="primary" @click="toggle">{{ playing ? '暂停' : '播放' }}</button>
        <button @click="step(1)">下一步</button>
        <input type="range" min="0" :max="frames.length - 1" v-model.number="i" @input="stop" aria-label="跳到某一步" />
      </div>
    </template>
    <div v-else class="sp-err">加载中…</div>
  </div>
</template>

<style scoped>
.sp {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 14px 16px;
  margin: 16px 0;
  background: var(--vp-c-bg-soft);
}
.sp-head { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; font-size: 14px; }
.sp-count { color: var(--vp-c-text-2); font-variant-numeric: tabular-nums; }
.sp-canvas { overflow-x: auto; margin: 8px 0; }
.sp-box { fill: var(--vp-c-bg); stroke: var(--vp-c-text-3); stroke-width: 1.5; transition: fill 0.2s; }
.sp-box.hl { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 2.5; }
.sp-val { text-anchor: middle; font-size: 17px; font-weight: 600; fill: var(--vp-c-text-1); }
.sp-idx { text-anchor: middle; font-size: 11px; fill: var(--vp-c-text-3); }
.sp-null { text-anchor: middle; font-size: 20px; fill: var(--vp-c-text-3); }
.sp-edge { fill: none; stroke: var(--vp-c-text-2); stroke-width: 1.8; }
.sp-arrowhead { fill: var(--vp-c-text-2); }
.sp-ptr { text-anchor: middle; font-size: 13px; font-weight: 600; fill: var(--vp-c-brand-1); }
.sp-tedge { stroke: var(--vp-c-text-3); stroke-width: 1.6; }
.sp-mark { text-anchor: middle; font-size: 12px; font-weight: 600; fill: var(--vp-c-brand-2); font-family: var(--vp-font-family-mono); }
.sp-dim { opacity: 0.3; }
.sp-window { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-2); stroke-dasharray: 4 3; }
.sp-note { margin: 4px 0; font-size: 14px; min-height: 2.6em; }
.sp-extra { margin: 0 0 4px; font-size: 13px; color: var(--vp-c-text-2); font-family: var(--vp-font-family-mono); }
.sp-ctrl { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.sp-ctrl button {
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 3px 12px;
  font-size: 13px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
}
.sp-ctrl button.primary { background: var(--vp-c-brand-1); color: var(--vp-c-white); border-color: var(--vp-c-brand-1); }
.sp-ctrl input { flex: 1; min-width: 120px; }
.sp-err { color: var(--vp-c-text-2); font-size: 14px; }
</style>
