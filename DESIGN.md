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
| `--ink-secondary` | `#3A3A3A` | 次要文字 |
| `--ink-muted` | `#5A5A5A` | 弱化文字 |
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
| `--ink-secondary` | `#C8C4BE` | 次要文字 |
| `--ink-muted` | `#9A9690` | 弱化文字 |
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

伪元素仅应用于 `.nav.glass`、`.stat-card.glass`、`.detail.glass`，不应用于 `.card.glass`（卡片组件已移除装饰性伪元素）。

1. **`::before`** — 顶部折射光线（1px 高光线，从透明到高光再到透明）
2. **`::after`** — 内部折射渐变（上半部分 50% 区域的线性渐变，模拟光线穿透玻璃）

```css
.nav.glass::before,
.stat-card.glass::before,
.detail.glass::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 5%, var(--glass-highlight) 50%, transparent 95%);
}

.nav.glass::after,
.detail.glass::after {
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

- 继承 `.glass` 效果，但移除装饰性边框和伪元素：
  - `border: none`（无边框，更干净的外观）
  - 不使用 `::before` / `::after` 伪元素（去除顶部折射光线和内部折射渐变）
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
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
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
  padding: 10px 14px;
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

### QR 码页面 (.checkin-card + .qr-image-wrap)

居中布局，复用 `.checkin-card.glass` 容器，包含活动信息与 QR 码图片。

| 类名 | 用途 | 样式 |
|------|------|------|
| `.checkin-card` | 卡片容器 | 毛玻璃背景 + 居中 flex |
| `.qr-image-wrap` | QR 码图片容器 | margin 20px + z-index 2 |
| `.qr-code-label` | 签到码标签 | 11px DM Sans，ink-muted |
| `.qr-code-value` | 签到码数值 | 28px DM Sans 300，letter-spacing 4px |

核心属性：

```css
.checkin-card {
  padding: 44px 32px;
  max-width: 380px;
  width: 100%;
  text-align: center;
}

.qr-image-wrap {
  margin: 20px 0;
  position: relative;
  z-index: 2;
}
```

打印适配：

```css
@media print {
  .nav, .site-footer, .card-link { display: none !important; }
  body { background: #fff !important; }
  .glass {
    background: none !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
    border: 1px solid #ddd !important;
  }
  .glass::before, .glass::after { display: none !important; }
}
```

响应式：移动端 padding 缩至 24px。

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

## 8. 多语言支持（i18n 系统）

### 架构概述

项目采用 **服务端 i18n 字典 + Jinja2 全局函数** 的方案，取代早期的 `data-zh`/`data-en` 属性方案。核心文件为 `app/translations.py`，包含 120+ 条翻译条目。

### translations.py 结构

```python
# app/translations.py
TRANSLATIONS = {
    "活动": "Events",
    "报名": "Register",
    "取消报名": "Cancel",
    "签到": "Check In",
    # ... 120+ 条目
}

CATEGORY_MAP = {
    "学术": "Academic", "体育": "Sports", "文艺": "Arts",
    "社交": "Social", "志愿服务": "Volunteer", "其他": "Other",
}
```

### Jinja2 context_processor 注册

在 `create_app()` 中通过 `context_processor` 注入翻译函数：

```python
from app.translations import TRANSLATIONS, CATEGORY_MAP

@app.context_processor
def inject_translations():
    def t(zh):
        return TRANSLATIONS.get(zh, zh)
    def t_category(zh):
        return CATEGORY_MAP.get(zh, zh)
    return dict(t=t, t_category=t_category)
```

### 模板使用方式

```html
<!-- 静态文本使用 t() 函数 -->
<a href="{{ url_for('event.list_events') }}">{{ t("活动") }}</a>
<button>{{ t("报名") }}</button>

<!-- 分类名使用 t_category() -->
<span>{{ t_category(event.category) }}</span>
```

### 双语数据库字段

Event 模型新增 `title_en`、`description_en`、`location_en` 字段，用于预翻译的英文内容：

```python
class Event(db.Model):
    title = db.Column(db.String(200), nullable=False)          # 中文标题
    title_en = db.Column(db.String(200))                        # 英文标题
    description = db.Column(db.Text)                            # 中文描述
    description_en = db.Column(db.Text)                         # 英文描述
    location = db.Column(db.String(200))                        # 中文地点
    location_en = db.Column(db.String(200))                     # 英文地点
```

在 `seed.py` 中预填充英文翻译。`t()` 函数通过 `context_processor` 注入，接收中文文本返回翻译结果（闭包实现），不依赖 `lang` 参数、cookie 或 session。

---

## 8b. CSS 架构规则

### 全局 vs 局部规则

CSS 采用 **全局选择器列表** 统一规则，避免逐元素重复声明：

```css
/* 字体层次：衬线用于标题和正文，无衬线用于 UI 元素 */
h1, h2, h3, h4, h5, h6,
.detail-body, .desc, .hero p {
    font-family: "Noto Serif SC", "Songti SC", serif;
}

.nav, .btn, .badge, .pill, .page-btn, .stat-card label,
.form-label, .admin-table th, .footer {
    font-family: "DM Sans", "Noto Serif SC", sans-serif;
}

/* 数字等宽 */
body, td, th, p, li, .stat-number, .badge, .rate {
    font-variant-numeric: tabular-nums;
}

/* 标题平衡换行 */
h1, h2, h3, h4, h5, h6 {
    text-wrap: balance;
}

/* 容器居中 */
.report-body, .main-content, .container {
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
```

### 设计原则

- **一处声明，全局生效**：一个选择器列表覆盖所有适用元素，不为每个组件单独写 `font-family`
- **font-family 层次**：衬线（Noto Serif SC）用于标题/正文/描述，无衬线（DM Sans）用于导航/按钮/标签/表格
- **tabular-nums 全局**：所有数字显示区域使用等宽数字，避免布局跳动
- **text-wrap: balance**：所有标题使用平衡换行，避免单字成行

---

## 8c. Translation API

### POST /api/translate

翻译 API 端点，支持中英双向翻译。CSRF 豁免，供前端异步调用。

```python
# app/translate.py
csrf.exempt(translate_bp)

@translate_bp.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "missing 'text' field"}), 400

    text = data['text']
    target = data.get('target', 'en')

    zh_en = {"学术": "Academic", "体育": "Sports", "文艺": "Arts", ...}
    en_zh = {v: k for k, v in zh_en.items()}

    if target == "en":
        result = zh_en.get(text, text)
    else:
        result = en_zh.get(text, text)

    return jsonify({"original": text, "translated": result, "target": target})
```

### GET /api/events

返回活动列表的双语 JSON，供外部集成或前端 AJAX 使用：

```python
@app.route('/api/events')
def api_events():
    events = Event.query.order_by(Event.start_time.desc()).all()
    return jsonify([{
        "id": e.id,
        "title": {"zh": e.title, "en": e.title_en or e.title},
        "description": {"zh": e.description, "en": e.description_en or e.description},
        "location": {"zh": e.location, "en": e.location_en or e.location},
        "category": {"zh": e.category, "en": e.category},
        "max_participants": e.max_participants,
        "registered_count": e.registered_count,
    } for e in events])
```

---

## 9. 响应式设计

### 断点

两个断点：**768px**（平板）和 **640px**（手机）

```css
@media (max-width: 768px) { ... }
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
