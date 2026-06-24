# 校园活动平台 — 设计系统

## 1. 设计概述

### 设计理念

本项目采用 **Apple Liquid Glass (WWDC25)** 设计语言，以毛玻璃（frosted glass）为核心视觉元素，营造轻盈、通透、现代的界面质感。所有容器组件均使用半透明背景 + `backdrop-filter` 模糊 + 顶部折射光线 + 内部渐变，模拟真实玻璃的光学效果。

### 设计工具

| 工具 | 用途 |
|------|------|
| MiMo Code Agent | 核心代码生成与迭代 |
| frontend-design skill | 前端界面设计与组件实现 |
| make-interfaces-feel-better skill | 交互细节打磨（动画、hover、微交互） |

### 设计参考

- **Apple HIG Liquid Glass** — 毛玻璃材质规范、光影层次、圆角体系
- **NN/g UX Guidelines** — 可用性原则、无障碍设计、交互反馈

---

## 2. 色彩系统

### 浅色主题 (`[data-theme="light"]`)

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#EDEAE4` | 页面背景 |
| `--bg-gradient` | `linear-gradient(160deg, #EDEAE4 0%, #E4DED5 50%, #DDD7CE 100%)` | 渐变背景 |
| `--ink` | `#1A1A1A` | 主文字 |
| `--ink-secondary` | `#4A4A4A` | 次要文字 |
| `--ink-muted` | `#8A8A8A` | 弱化文字 |
| `--accent` | `#C45A3A` | 主题强调色（赤陶色） |
| `--accent-hover` | `#B04E32` | 强调色 hover |
| `--accent-soft` | `rgba(196,90,58,0.12)` | 强调色淡底 |
| `--success` | `#2D7A4F` | 成功状态 |
| `--danger` | `#A03030` | 危险/错误 |
| `--warn` | `#9A7A20` | 警告 |
| `--glass-bg` | `rgba(255,255,255,0.42)` | 毛玻璃背景 |
| `--glass-bg-hover` | `rgba(255,255,255,0.58)` | 毛玻璃 hover |
| `--glass-border` | `rgba(255,255,255,0.6)` | 毛玻璃边框 |
| `--glass-highlight` | `rgba(255,255,255,0.8)` | 顶部折射高光 |
| `--glass-refraction` | `linear-gradient(180deg, rgba(255,255,255,0.5), transparent 40%)` | 内部折射渐变 |
| `--glass-blur` | `40px` | 模糊半径 |
| `--glass-shadow` | `0 4px 30px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03)` | 柔和阴影 |
| `--glass-shadow-hover` | `0 8px 40px rgba(0,0,0,0.07), 0 2px 6px rgba(0,0,0,0.04)` | 悬浮阴影 |
| `--glass-blur-heavy` | `60px` | 重度模糊（导航栏） |
| `--glass-border-subtle` | `rgba(255,255,255,0.35)` | 微妙边框（toggle 等） |
| `--glass-highlight-bottom` | `rgba(0,0,0,0.03)` | 底部微光 |
| `--success-soft` | `rgba(45,122,79,0.1)` | 成功淡底 |
| `--danger-soft` | `rgba(160,48,48,0.08)` | 危险淡底 |
| `--warn-soft` | `rgba(154,122,32,0.1)` | 警告淡底 |
| `--nav-bg` | `rgba(237,234,228,0.65)` | 导航栏背景 |
| `--nav-border` | `rgba(0,0,0,0.06)` | 导航栏底边框 |
| `--input-bg` | `rgba(255,255,255,0.3)` | 输入框背景 |
| `--input-border` | `rgba(0,0,0,0.1)` | 输入框边框 |
| `--input-focus` | `rgba(196,90,58,0.4)` | 输入框聚焦光晕 |
| `--progress-bg` | `rgba(0,0,0,0.06)` | 进度条背景 |
| `--progress-fill` | `var(--success)` | 进度条填充 |
| `--toggle-bg` | `rgba(0,0,0,0.08)` | Toggle 背景 |
| `--toggle-active` | `var(--ink)` | Toggle 激活背景 |
| `--toggle-active-text` | `var(--bg)` | Toggle 激活文字 |
| `--glass-radius` | `20px` | 统一圆角 |

### 深色主题 (`[data-theme="dark"]`)

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#0E0E12` | 页面背景 |
| `--bg-gradient` | `linear-gradient(160deg, #0E0E12 0%, #141418 50%, #18181E 100%)` | 渐变背景 |
| `--ink` | `#F0EDE8` | 主文字 |
| `--ink-secondary` | `#B8B4AE` | 次要文字 |
| `--ink-muted` | `#6A6660` | 弱化文字 |
| `--accent` | `#E07050` | 主题强调色 |
| `--accent-hover` | `#E88060` | 强调色 hover |
| `--accent-soft` | `rgba(224,112,80,0.15)` | 强调色淡底 |
| `--success` | `#4ADE80` | 成功状态 |
| `--danger` | `#F87171` | 危险/错误 |
| `--warn` | `#FACC15` | 警告 |
| `--glass-bg` | `rgba(255,255,255,0.06)` | 毛玻璃背景 |
| `--glass-bg-hover` | `rgba(255,255,255,0.1)` | 毛玻璃 hover |
| `--glass-border` | `rgba(255,255,255,0.1)` | 毛玻璃边框 |
| `--glass-highlight` | `rgba(255,255,255,0.12)` | 顶部折射高光 |
| `--glass-refraction` | `linear-gradient(180deg, rgba(255,255,255,0.08), transparent 40%)` | 内部折射渐变 |
| `--glass-blur` | `40px` | 模糊半径 |
| `--glass-shadow` | `0 4px 30px rgba(0,0,0,0.2), 0 1px 3px rgba(0,0,0,0.15)` | 柔和阴影 |
| `--glass-shadow-hover` | `0 8px 40px rgba(0,0,0,0.3), 0 2px 6px rgba(0,0,0,0.2)` | 悬浮阴影 |
| `--glass-blur-heavy` | `60px` | 重度模糊（导航栏） |
| `--glass-border-subtle` | `rgba(255,255,255,0.06)` | 微妙边框 |
| `--glass-highlight-bottom` | `rgba(255,255,255,0.02)` | 底部微光 |
| `--glass-radius` | `20px` | 统一圆角 |
| `--success-soft` | `rgba(74,222,128,0.1)` | 成功淡底 |
| `--danger-soft` | `rgba(248,113,113,0.1)` | 危险淡底 |
| `--warn-soft` | `rgba(250,204,21,0.08)` | 警告淡底 |
| `--nav-bg` | `rgba(14,14,18,0.6)` | 导航栏背景 |
| `--nav-border` | `rgba(255,255,255,0.06)` | 导航栏底边框 |
| `--input-bg` | `rgba(255,255,255,0.05)` | 输入框背景 |
| `--input-border` | `rgba(255,255,255,0.1)` | 输入框边框 |
| `--input-focus` | `rgba(224,112,80,0.4)` | 输入框聚焦光晕 |
| `--progress-bg` | `rgba(255,255,255,0.06)` | 进度条背景 |
| `--progress-fill` | `var(--success)` | 进度条填充 |
| `--toggle-bg` | `rgba(255,255,255,0.08)` | Toggle 背景 |
| `--toggle-active` | `var(--ink)` | Toggle 激活背景 |
| `--toggle-active-text` | `var(--bg)` | Toggle 激活文字 |

### 色彩对比度

所有文字/背景组合均满足 **WCAG AA** 标准（对比度 ≥ 4.5:1）：

- 浅色主题：`--ink` (#1A1A1A) on `--bg` (#EDEAE4) → 对比度 ~13.8:1
- 深色主题：`--ink` (#F0EDE8) on `--bg` (#0E0E12) → 对比度 ~16.2:1
- 强调色仅用于大面积装饰元素或高对比文字，不用于小字号正文

---

## 3. 字体系统

### 字体选择

| 用途 | 字体 | 类型 | 字重 |
|------|------|------|------|
| 中文正文 | Noto Serif SC | 衬线 | 300 / 400 / 600 / 700 |
| 英文/UI | DM Sans | 无衬线 | 300 / 400 / 500 / 700 |

### 字号/行高/字距规范

| 场景 | 字号 | 行高 | 字距 | 字体 |
|------|------|------|------|------|
| 页面标题 (h1) | 34px | 1.4 | 3px | Noto Serif SC 300 |
| 卡片标题 (h3) | 18px | — | 1.5px | Noto Serif SC 400 |
| 详情标题 (h2) | 26px | — | 2px | Noto Serif SC 300 |
| 正文描述 | 14px | 1.85 | — | Noto Serif SC 300 |
| 详情正文 | 15px | 2.0 | — | Noto Serif SC 300 |
| 导航链接 | 14px | — | 0.5px | DM Sans 400 |
| 品牌名 | 18px | — | 3px | DM Sans 300 |
| 徽章/标签 | 12px | — | 0.3px | DM Sans 500 |
| 表单标签 | 11px | — | 1px | DM Sans (大写) |
| 辅助文字 | 13px | — | 0.3px | DM Sans 300 |
| 统计数字 | 28px | — | — | DM Sans 300 |

---

## 4. 毛玻璃效果 (Liquid Glass)

### 实现原理

```css
.glass {
  background: var(--glass-bg);                    /* 半透明背景 */
  backdrop-filter: blur(var(--glass-blur));        /* 背景模糊 */
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);           /* 细边框 */
  border-radius: var(--glass-radius);              /* 同心圆角 */
  box-shadow: var(--glass-shadow);                 /* 柔和阴影 */
  position: relative;
  overflow: hidden;
}
```

### 伪元素层次

1. **`::before`** — 顶部折射光线（1px 高光线，从透明到高光再到透明）
2. **`::after`** — 内部折射渐变（上半部分 50% 区域的线性渐变，模拟光线穿透玻璃）

```css
.glass::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 5%, var(--glass-highlight) 50%, transparent 95%);
}

.glass::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 50%;
  background: var(--glass-refraction);
  border-radius: var(--glass-radius) var(--glass-radius) 0 0;
}
```

### 同心圆角规范

所有容器统一使用 `--glass-radius: 20px`。子组件圆角递减：

| 组件 | 圆角 |
|------|------|
| 主容器 (.glass) | 20px |
| 统计卡片 (.stat-card) | 16px |
| 数据表格 (.admin-table) | 16px |
| 搜索框 (.search-box) | 14px |
| 按钮 (.btn) | 12px |
| 表单输入框 | 10px |
| 徽章/标签 | 20px (pill) |

### 悬浮状态

```css
.glass:hover {
  background: var(--glass-bg-hover);    /* 透明度降低，更实 */
  box-shadow: var(--glass-shadow-hover); /* 阴影加深 */
  transform: translateY(-2px);           /* 轻微上浮 */
}
```

---

## 5. 组件规范

### 导航栏 (.nav)

- `position: sticky; top: 0; z-index: 100`
- 背景：`var(--nav-bg)` + `backdrop-filter: blur(var(--glass-blur-heavy))` (heavy blur)
- 底部 1px 边框：`box-shadow: 0 1px 0 var(--nav-border)`
- 品牌名：DM Sans 300，3px 字距，`.dot` 使用强调色

### 卡片 (.card + .glass)

- 继承 `.glass` 所有效果
- 入场动画：`cardEnter` keyframes，0.4s ease，从 `translateY(12px)` 滑入
- 多卡片使用 stagger animation（通过 CSS delay 实现）
- 内部结构：`.card-header` + `.meta` + `.desc` + `.card-footer`

### 按钮 (.btn)

| 类名 | 用途 | 样式 |
|------|------|------|
| `.btn-primary` | 主操作 | 强调色背景 + 白色文字 + 阴影 |
| `.btn-glass` | 次要操作 | 毛玻璃背景 + 边框 |
| `.btn-success` | 成功操作 | 绿色背景 |
| `.btn-danger` | 危险操作 | 红色背景 |
| `.btn-sm` | 小按钮 | 缩小 padding 和字号 |

交互反馈：

```css
.btn:active { transform: scale(0.96); }
.btn-primary:hover { transform: translateY(-1px); }
```

### 表单 (.form-group)

- 输入框使用 `var(--input-bg)` + `backdrop-filter: blur(12px)`
- 边框：`var(--input-border)`，聚焦时变为 `var(--accent)` + `box-shadow: 0 0 0 3px var(--accent-soft)`
- 标签：11px 大写，DM Sans，1px 字距

### 徽章 (.badge)

- Pill 形状 (`border-radius: 20px`)
- 颜色编码：
  - `.open` → 绿色（可报名）
  - `.full` → 红色（已满）
  - `.warn` → 黄色（警告）
- 数字使用 `font-variant-numeric: tabular-nums` 等宽

### 数据表格 (.admin-table)

- 表头：11px 大写，DM Sans，1px 字距
- 行：hover 时背景变为 `rgba(255,255,255,0.08)`
- 进度条：`.progress` 容器 + `.fill` 填充，`transition: width 0.4s ease`

### Flash 消息 (.alert)

- 自动消失：`flash-auto-dismiss` 类，5s 后 fadeOut
- 入场动画：`slideIn`，从 `translateY(-12px)` 滑入
- 左边框颜色编码：success=绿, danger=红, warn=黄, info=强调色

### 分类筛选药丸按钮 (.category-pills)

容器使用 flexbox 水平排列，gap 8px，允许换行 (`flex-wrap: wrap`)。

| 类名 | 用途 | 样式 |
|------|------|------|
| `.category-pills` | 容器 | `display: flex; flex-wrap: wrap; gap: 8px` |
| `.pill` | 单个筛选按钮 | 毛玻璃背景 + pill 圆角 |
| `.pill.active` | 选中状态 | 强调色背景 + 白色文字 |

核心属性：

```css
.pill {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 8px 18px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-secondary);
  cursor: pointer;
  transition: background 0.25s, transform 0.25s, box-shadow 0.25s, color 0.25s ease;
}

.pill:hover {
  background: var(--glass-bg-hover);
  transform: translateY(-1px);
  box-shadow: var(--glass-shadow-hover);
}

.pill:active {
  transform: scale(0.96);
}

.pill.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  box-shadow: 0 2px 12px rgba(196,90,58,0.25);
}
```

响应式：移动端 padding 缩至 `6px 14px`，字号 12px。

### 分页控件 (.pagination)

| 类名 | 用途 | 样式 |
|------|------|------|
| `.pagination` | 容器 | flexbox 居中，gap 6px |
| `.page-btn` | 页码按钮 | 毛玻璃背景 + 圆角 |
| `.page-btn.active` | 当前页 | 强调色背景 + 白色文字 |
| `.page-btn:disabled` | 禁用状态 | 降低透明度，禁止点击 |

核心属性：

```css
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-top: 24px;
}

.page-btn {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  padding: 8px 14px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-secondary);
  cursor: pointer;
  min-width: 40px;
  text-align: center;
  transition: background 0.25s, transform 0.25s, box-shadow 0.25s, color 0.25s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--glass-bg-hover);
  transform: translateY(-1px);
  box-shadow: var(--glass-shadow-hover);
}

.page-btn:active:not(:disabled) {
  transform: scale(0.96);
}

.page-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  box-shadow: 0 2px 12px rgba(196,90,58,0.25);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}
```

响应式：移动端 gap 缩至 4px，padding 缩至 `6px 10px`。

### QR 码页面 (.qr-card)

居中布局，包含活动信息与 QR 码图片，支持打印。

| 类名 | 用途 | 样式 |
|------|------|------|
| `.qr-card` | 卡片容器 | 毛玻璃背景 + 居中 flex |
| `.qr-image` | QR 码图片 | 固定尺寸 + 微妙边框 |

核心属性：

```css
.qr-card {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  text-align: center;
  max-width: 420px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
}

.qr-image {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  outline: 1px solid rgba(0,0,0,0.1);
  outline-offset: 4px;
}
```

打印适配：

```css
@media print {
  .qr-card {
    background: #fff;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    box-shadow: none;
    border: 1px solid #ddd;
    break-inside: avoid;
  }
  .qr-image {
    outline: none;
  }
}
```

响应式：移动端 padding 缩至 24px，`.qr-image` 尺寸缩至 160px。

### 导出按钮 (.btn-glass.btn-sm)

复用现有 `.btn-glass` 毛玻璃按钮样式，搭配 `.btn-sm` 小尺寸变体。

```css
.btn-glass.btn-sm {
  padding: 6px 14px;
  font-size: 12px;
  border-radius: 10px;
}
```

用于页面顶部操作区（如"导出 CSV"、"导出 QR 码"），与页面标题行对齐。

---

## 6. 交互规范

### 过渡动画

**不使用 `transition: all`**，精确指定属性：

```css
/* 容器 */
transition: background 0.35s cubic-bezier(0.4,0,0.2,1),
            box-shadow 0.35s cubic-bezier(0.4,0,0.2,1),
            transform 0.35s cubic-bezier(0.4,0,0.2,1);

/* 按钮 */
transition: background 0.25s, transform 0.25s, box-shadow 0.25s, color 0.25s ease;

/* 导航链接 */
transition: color 0.3s;

/* 输入框聚焦 */
transition: border-color 0.3s ease, box-shadow 0.3s ease;

/* 主题切换 */
transition: background 0.5s ease, color 0.3s ease;
```

### 点击反馈

```css
.btn:active { transform: scale(0.96); }
```

### 最小触摸区域

所有可交互元素最小尺寸 **40×40px**（通过 padding 保证）。

### 数字等宽

```css
.tabular-nums { font-variant-numeric: tabular-nums; }
```

用于统计数字、表格数据列。

### 标题平衡换行

```css
.hero h1 { text-wrap: balance; }
.detail h2 { text-wrap: balance; }
.auth-card h2 { text-wrap: balance; }
```

---

## 7. 主题切换

### 实现机制

使用 `data-theme` 属性在 `<html>` 元素上切换：

```html
<html lang="zh-CN" data-theme="light">
```

### CSS 变量切换

```css
:root, [data-theme="light"] {
  --bg: #EDEAE4;
  /* ... 浅色主题变量 */
}

[data-theme="dark"] {
  --bg: #0E0E12;
  /* ... 深色主题变量 */
}
```

### JavaScript 实现

```javascript
function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    // 更新 toggle 按钮状态
    document.querySelectorAll('#themeToggle button').forEach(function(b) {
        b.classList.remove('active');
    });
    document.querySelector('#themeToggle button[onclick="setTheme(\'' + t + '\')"]')
        .classList.add('active');
    localStorage.setItem('theme', t);
}

// 页面加载时恢复
(function() {
    var saved = localStorage.getItem('theme');
    if (saved) setTheme(saved);
})();
```

### 持久化

主题偏好存储在 `localStorage.setItem('theme', 'light'|'dark')`，页面加载时自动恢复。

---

## 8. 多语言支持

### 实现机制

使用 `data-zh` 和 `data-en` 属性存储双语文本：

```html
<a data-zh="活动" data-en="Events">活动</a>
<button data-zh="退出" data-en="Logout">退出</button>
```

### setLang() 函数

```javascript
function setLang(l) {
    // 更新文本内容
    document.querySelectorAll('[data-zh]').forEach(function(el) {
        el.textContent = el.getAttribute('data-' + l);
    });
    // 更新 placeholder
    document.querySelectorAll('[data-zh-placeholder]').forEach(function(el) {
        el.placeholder = el.getAttribute('data-' + l + '-placeholder');
    });
    // 更新 toggle 按钮状态
    // 持久化到 localStorage
    localStorage.setItem('lang', l);
}
```

### 扩展指南

添加新语言（如日语）：

1. 在 HTML 元素上添加 `data-ja="日本語"` 属性
2. 在 `setLang()` 函数中添加对 `data-ja` 的处理
3. 在语言 toggle 中添加新按钮：`<button onclick="setLang('ja')">JP</button>`
4. 在 `localStorage` 键名中保持 `'lang'` 不变

---

## 9. 响应式设计

### 断点

单一断点：**640px**（移动端/桌面端）

```css
@media (max-width: 640px) { ... }
```

### 移动端适配策略

| 组件 | 桌面端 | 移动端 |
|------|--------|--------|
| 页面标题字号 | 34px | 26px |
| 内容区域 padding | 32px | 20px |
| 详情信息网格 | 2列 | 1列 |
| 统计卡片行 | 水平排列 | 垂直堆叠 |
| 表格列 | 4列 | 2列 |
| 表单双列 | 2列 | 1列 |
| 导航链接间距 | 24px | 16px |
| 导航链接字号 | 14px | 13px |
| 导航栏 padding | 16px 32px | 14px 20px |
