# Skill Discoverer 配置

## 搜索策略

### 兴趣领域（按优先级）
1. **效率工具** - automation, productivity, workflow
2. **数据分析** - data, analysis, chart, visualization
3. **开发工具** - git, github, code, debug, testing
4. **AI 增强** - llm, ai, prompt, rag, embedding
5. **系统集成** - api, webhook, notification, calendar, email
6. **安全** - security, audit, permission, auth

### 搜索关键词
```
automation
productivity
github
git
data-analysis
visualization
llm
ai-assistant
api-integration
notification
calendar
security
backup
monitoring
```

### 过滤规则（严格模式）

**必须满足至少一项：**
- ⭐ 下载量 ≥ 50
- ⭐ 安装量 ≥ 20
- ⭐ 有 Star（任何数量）

**必须满足：**
- ✅ 版本 ≥ 0.1.0（排除太早期的）
- ✅ Summary 长度 ≥ 50 字符（有清晰说明）
- ✅ 有 changelog 或使用说明

**优先推荐（加分项）：**
- 🏆 下载量 ≥ 100（+3 分）
- 🏆 安装量 ≥ 50（+2 分）
- 🏆 有 Star（+2 分）
- 🏆 版本 ≥ 1.0.0（稳定版，+1 分）
- 🏆 最近 30 天有更新（+1 分）

**推荐阈值：**
- 总分 ≥ 5 分 才推荐
- 每次最多推荐 3 个（少而精）

---

## 推荐流程

1. **发现** - 每 2 小时搜索一次
2. **筛选** - 按上述规则过滤
3. **推荐** - 飞书发送推荐卡片：
   ```
   🆕 新 Skill 发现
   
   名称：xxx
   描述：...
   版本：1.2.3
   下载量：123
   评分：⭐⭐⭐⭐
   
   [安装] [忽略] [稍后]
   ```
4. **执行** - 用户回复"安装" → 自动 `clawhub install`
5. **配置** - 如需配置，通知用户

---

## 已安装追踪

记录已安装/已推荐的 skill，避免重复：
- `installed_skills.json` - 已安装的
- `recommended_skills.json` - 已推荐过的

---

## 运行模式

- **心跳模式** - 每 2 小时检查一次（推荐）
- **手动触发** - 用户说"找找新技能"
- **启动扫描** - agent 启动时先扫一波
