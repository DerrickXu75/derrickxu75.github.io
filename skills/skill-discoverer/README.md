# 🤖 Skill Discoverer - 技能发现者

**自动发现、推荐和安装 ClawHub 新技能，持续提升 Agent 能力**

---

## 🚀 快速开始

### 1. 测试搜索

```bash
python3 ~/.openclaw/workspace/skills/skill-discoverer/scripts/discover_skills.py
```

### 2. 安装推荐的技能

```bash
python3 ~/.openclaw/workspace/skills/skill-discoverer/scripts/install_skill.py <skill-slug>
```

### 3. 启用自动发现

在 `HEARTBEAT.md` 中添加：

```markdown
- 每 2 小时运行 skill-discoverer 搜索新技能
```

---

## 📊 测试结果

刚才的搜索找到了：

| 技能 | 下载量 | 评分 | 说明 |
|------|--------|------|------|
| `elasticsearch-openclaw` | 0 | ⭐⭐⭐ | ES 9.x 完整参考 |
| `duckduckgo-search-1-0-0` | 119 | ⭐⭐⭐⭐ | 隐私搜索，无需 API |
| `ebook-to-md` | 27 | ⭐⭐⭐ | PDF/电子书转 Markdown |

---

## 💬 与主 Agent 交互

### 用户触发

```
用户：找找有什么新技能
大黑：🔍 正在搜索...

发现 3 个推荐：
1. DuckDuckGo Search - 隐私搜索工具
2. eBook to MD - 电子书转换
3. Elasticsearch - 搜索集成

要安装哪个？回复数字或"全部"
```

### 用户确认

```
用户：安装 1 和 2
大黑：📦 正在安装...
✅ DuckDuckGo Search 已安装
✅ eBook to MD 已安装

这两个技能无需额外配置，可以直接使用。
```

---

## 🔧 配置

编辑 `CONFIG.md` 自定义：
- 兴趣领域
- 搜索关键词
- 过滤规则

---

## 📁 文件结构

```
skill-discoverer/
├── SKILL.md              # 技能说明
├── CONFIG.md             # 搜索策略配置
├── README.md             # 本文档
├── scripts/
│   ├── discover_skills.py  # 搜索脚本
│   └── install_skill.py    # 安装脚本
└── state/
    ├── installed.json      # 已安装记录
    └── recommended.json    # 已推荐记录
```

---

## 🎯 下一步

1. **测试安装一个技能**
   ```bash
   python3 ~/.openclaw/workspace/skills/skill-discoverer/scripts/install_skill.py duckduckgo-search-1-0-0
   ```

2. **配置自动运行**
   - 编辑 `HEARTBEAT.md`
   - 添加定时搜索任务

3. **自定义搜索策略**
   - 编辑 `CONFIG.md`
   - 添加你感兴趣的关键词

---

## 📝 日志

- 2026-02-25: 初始版本创建
- 搜索测试成功，找到 3 个推荐技能
