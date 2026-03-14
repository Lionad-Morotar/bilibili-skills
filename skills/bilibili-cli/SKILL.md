---
name: bilibili-cli
description: 使用 bili CLI 工具与 Bilibili 交互，获取视频信息、下载音频、搜索内容、管理收藏和互动。当用户提到 Bilibili、视频下载、B站搜索、BV号解析、字幕提取、音频切分、一键三连等场景时触发。支持批量操作和结构化输出（YAML/JSON）。
---

# Bilibili CLI Skill

通过 [bilibili-cli](https://github.com/jackwener/bilibili-cli) 工具在终端与 Bilibili 交互。

部分复杂需求借助了 [bilibili-api](https://nemo2011.github.io/bilibili-api) 项目，当 bilibili-cli 无法实现部分功能时，参考：

* [bilibili-api usage](./references/bili-api.md)

## Prerequisites

确保已安装 bilibili-cli 以及已登录：

```bash
bili status
# 正常情况下会输出已登录用户信息
✅ 已登录：仿生狮子  (UID: 6626299)
```

如果没有安装：

```bash
uv tool install bilibili-cli
# 或带音频功能
uv tool install "bilibili-cli[audio]"
```

首次使用需登录：
```bash
bili login      # 扫码登录
bili status     # 检查登录状态
```

## Core Workflows

### 1. 获取视频信息

```bash
# 基本信息
bili video <BV号>

# 带字幕（纯文本）
bili video <BV号> --subtitle

# 带时间轴的字幕
bili video <BV号> --subtitle-timeline

# 导出为 SRT 格式
bili video <BV号> -st --subtitle-format srt

# AI 摘要
bili video <BV号> --ai

# 热门评论
bili video <BV号> --comments

# 相关推荐视频
bili video <BV号> --related
```

**结构化输出**（推荐用于后续处理）：
```bash
bili video <BV号> --yaml
bili video <BV号> --json
```

### 2. 搜索与发现

```bash
# 搜索视频
bili search "关键词" --type video --max 10

# 搜索用户
bili search "用户名"

# 热门视频
bili hot --page 1 --max 20

# 全站排行榜（3天/7天）
bili rank --day 3 --max 30
bili rank --day 7 --max 50

# 动态时间线
bili feed
```

### 3. 用户相关

```bash
# UP主资料
bili user <UID>
bili user "用户名"      # 按名称搜索

# UP主视频列表
bili user-videos <UID> --max 20

# 当前登录用户信息
bili whoami
bili whoami --yaml
```

### 4. 音频下载与处理

```bash
# 下载音频并切分为 25 秒 WAV 片段（ASR-ready）
bili audio <BV号>

# 自定义片段时长
bili audio <BV号> --segment 60

# 下载完整音频，不切分
bili audio <BV号> --no-split

# 指定输出目录
bili audio <BV号> -o ~/Downloads/
```

### 5. 互动操作

```bash
# 点赞
bili like <BV号>

# 投币
bili coin <BV号>

# 一键三连（点赞+投币+收藏）
bili triple <BV号>
```

### 6. 收藏与列表管理

```bash
# 查看收藏夹列表
bili favorites

# 查看指定收藏夹内容
bili favorites <收藏夹ID> --page 1

# 稍后再看
bili watch-later

# 观看历史
bili history

# 关注列表
bili following

# 取消关注
bili unfollow <UID>
```

### 7. 动态管理

```bash
# 发布纯文本动态
bili dynamic-post "动态内容"

# 查看自己发布的动态
bili my-dynamics

# 删除动态
bili dynamic-delete <动态ID>
```

## Output Formats

### 默认输出
- TTY（终端）：富文本格式，带颜色
- 非 TTY：自动使用 YAML

### 显式指定格式
```bash
# 结构化 YAML（推荐，token效率高）
bili <command> --yaml

# JSON 格式
bili <command> --json

# 富文本（强制）
bili <command> --format rich
```

### 环境变量
```bash
OUTPUT=yaml      # 默认 YAML
OUTPUT=json      # 默认 JSON
OUTPUT=rich      # 默认富文本
OUTPUT=auto      # 自动检测
```

## Structured Data Schema

所有 `--yaml` / `--json` 输出使用统一信封格式：

```yaml
ok: true
schema_version: "1.0"
data:
  video: {...}
  subtitle: {...}
  comments: [...]
  ai_summary: "..."
error: null
```

**数据路径映射：**

| 命令 | 数据路径 |
|------|---------|
| `bili video` | `data.video`, `data.subtitle`, `data.ai_summary`, `data.comments`, `data.related` |
| `bili hot` / `rank` | `data.items` |
| `bili search` | 标准化的用户/视频列表 |
| 写操作（like/coin等） | 标准化结果 |

## Error Codes

| 错误码 | 含义 | 解决方案 |
|-------|------|---------|
| `not_authenticated` | 需要登录 | 运行 `bili login` |
| `permission_denied` | 权限不足 | 检查账号权限 |
| `invalid_input` | 输入无效 | 检查 BV 号格式（BV + 10位字母数字）|
| `network_error` | 网络错误 | 检查网络连接/代理 |
| `upstream_error` | 上游错误 | Bilibili 服务异常，稍后重试 |
| `not_found` | 资源不存在 | 检查视频/用户是否存在 |
| `rate_limited` | 请求过于频繁 | 减少 `--max` 参数，等待后重试 |
| `internal_error` | 内部错误 | 重新登录或联系开发者 |

## Best Practices

1. **优先使用结构化输出**：在自动化脚本中使用 `--yaml` 或 `--json` 便于解析
2. **批量操作添加延迟**：避免触发 rate limit
3. **音频切分用于 ASR**：`--segment` 参数配合 Whisper 等工具使用
4. **字幕导出**：使用 `--subtitle-format srt` 生成标准字幕文件

## Examples

### 示例 1：获取视频完整信息
```bash
bili video BV1xx411c7mD --subtitle --comments --ai --yaml
```

### 示例 2：批量获取热门视频
```bash
bili hot --page 1 --max 50 --yaml
```

### 示例 3：搜索并筛选
```bash
bili search "Python教程" --type video --max 10 --yaml
```

### 示例 4：下载音频用于语音识别
```bash
bili audio BV1xx411c7mD --segment 30 -o ./audio/
```

### 示例 5：获取 UP 主最近视频
```bash
# 先搜索 UID
bili user "老番茄"
# 然后用 UID 获取视频
bili user-videos <uid> --max 20 --yaml
```


