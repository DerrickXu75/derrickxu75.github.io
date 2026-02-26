# Learnings Log

记录纠正、知识更新、最佳实践。

---

## [LRN-20260225-001] correction

**Logged**: 2026-02-25T22:18:00+08:00
**Priority**: medium
**Status**: promoted
**Area**: config

### Summary
模型测试时，GLM-5 是当前运行模型，评估报告应声明潜在利益冲突

### Details
当我自己（GLM-5）作为被测模型之一时，在评估报告中应该明确声明"当前运行模型是 GLM-5"，让用户知道潜在的利益冲突。

### Metadata
- Source: user_feedback
- Tags: bias, evaluation, transparency

### Promotion
- **Promoted to**: AGENTS.md (调度器模式)
- **Lesson**: 作为评估者时声明自己的身份和潜在偏见

---

## [LRN-20260225-002] best_practice

**Logged**: 2026-02-25T22:11:00+08:00
**Priority**: high
**Status**: promoted
**Area**: config

### Summary
主会话应该只做调度，耗时任务派发给子代理

### Details
用户反馈：执行任务会阻塞主会话，导致无法继续对话。解决方案是主会话只负责：
1. 问答（快速响应）
2. 规划和派发任务给子代理
3. 汇总结果

耗时任务（代码生成、研究、批量处理）全部派发给子代理并行执行。

### Metadata
- Source: user_feedback
- Tags: architecture, delegation, subagent

### Promotion
- **Promoted to**: AGENTS.md (调度器模式)

---