#!/usr/bin/env python3
"""
Skill Discoverer - 自动搜索和推荐 ClawHub skills
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置 - 严格模式，只推荐高质量技能
CONFIG = {
    "interests": [
        "automation", "productivity", "workflow",
        "data", "analysis", "chart", "visualization",
        "git", "github", "code", "debug", "testing",
        "llm", "ai", "prompt", "rag", "embedding",
        "api", "webhook", "notification", "calendar", "email",
        "security", "audit", "auth",
        "backup", "monitoring"
    ],
    # 严格门槛 - 必须满足至少一项
    "min_downloads": 50,      # 下载量 ≥ 50
    "min_installs": 20,       # 安装量 ≥ 20
    "min_version": "0.1.0",   # 版本 ≥ 0.1.0（排除太早期）
    "min_summary_length": 50, # 描述至少 50 字符
    "max_recommendations": 3, # 少而精，每次最多 3 个
    # 推荐阈值
    "min_score": 5,           # 总分 ≥ 5 才推荐
}

STATE_DIR = Path(__file__).parent.parent / "state"
STATE_DIR.mkdir(exist_ok=True)

INSTALLED_FILE = STATE_DIR / "installed.json"
RECOMMENDED_FILE = STATE_DIR / "recommended.json"


def load_state(file: Path) -> set:
    """加载已记录的技能集合"""
    if file.exists():
        with open(file) as f:
            return set(json.load(f))
    return set()


def save_state(file: Path, data: set):
    """保存技能集合"""
    with open(file, "w") as f:
        json.dump(list(data), f, indent=2)


def clawhub_explore(limit=50, sort="newest"):
    """获取最新 skills"""
    try:
        result = subprocess.run(
            ["clawhub", "explore", "--limit", str(limit), "--sort", sort, "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            # 跳过可能的日志行，找到 JSON 开始
            lines = result.stdout.strip().split("\n")
            json_start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("{") or line.strip().startswith("["):
                    json_start = i
                    break
            json_str = "\n".join(lines[json_start:])
            data = json.loads(json_str)
            return data.get("items", [])
    except Exception as e:
        print(f"Error fetching skills: {e}", file=sys.stderr)
    return []


def clawhub_search(query: str, limit=20):
    """搜索特定关键词的 skills"""
    try:
        result = subprocess.run(
            ["clawhub", "search", query, "--limit", str(limit), "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            json_start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("["):
                    json_start = i
                    break
            json_str = "\n".join(lines[json_start:])
            return json.loads(json_str)
    except Exception as e:
        print(f"Error searching '{query}': {e}", file=sys.stderr)
    return []


def filter_skill(skill: dict, installed: set, recommended: set) -> dict | None:
    """过滤技能 - 严格模式，只推荐高质量的"""
    slug = skill.get("slug", "")
    
    # 跳过已安装或已推荐的
    if slug in installed or slug in recommended:
        return None
    
    stats = skill.get("stats", {})
    latest = skill.get("latestVersion", {})
    downloads = stats.get("downloads", 0)
    installs = stats.get("installsAllTime", 0)
    stars = stats.get("stars", 0)
    version = latest.get("version", "0.0.0")
    summary = skill.get("summary", "")
    
    # ===== 硬性门槛（必须满足） =====
    
    # 版本检查 - 排除太早期的
    if version < CONFIG["min_version"]:
        return None
    
    # 描述长度检查 - 必须有清晰说明
    if len(summary) < CONFIG["min_summary_length"]:
        return None
    
    # 必须有 changelog 或使用说明
    if not latest.get("changelog"):
        return None
    
    # 质量门槛 - 必须满足至少一项
    has_downloads = downloads >= CONFIG["min_downloads"]
    has_installs = installs >= CONFIG["min_installs"]
    has_stars = stars > 0
    
    if not (has_downloads or has_installs or has_stars):
        return None  # 都不满足，跳过
    
    # ===== 评分逻辑 =====
    score = 0
    
    # 下载量评分（权重最高）
    if downloads >= 200:
        score += 5
    elif downloads >= 100:
        score += 3
    elif downloads >= 50:
        score += 2
    elif downloads >= 20:
        score += 1
    
    # 安装量评分（真实用户数）
    if installs >= 100:
        score += 4
    elif installs >= 50:
        score += 3
    elif installs >= 20:
        score += 2
    elif installs >= 5:
        score += 1
    
    # Star 评分（用户认可）
    if stars >= 5:
        score += 3
    elif stars >= 2:
        score += 2
    elif stars >= 1:
        score += 1
    
    # 版本稳定性（1.0.0+ 表示稳定）
    if version >= "1.0.0":
        score += 2
    elif version >= "0.5.0":
        score += 1
    
    # 描述质量
    if "use when" in summary.lower() or "使用" in summary:
        score += 2  # 有清晰的使用说明
    elif len(summary) >= 100:
        score += 1  # 描述详细
    
    # 最近活跃（检查更新时间 - 时间戳是毫秒）
    import time
    now = time.time() * 1000
    updated_at = skill.get("updatedAt", 0)
    days_since_update = (now - updated_at) / (1000 * 60 * 60 * 24)
    if days_since_update <= 30:
        score += 2  # 30 天内有更新
    elif days_since_update <= 90:
        score += 1  # 90 天内有更新
    
    # 只推荐高分技能
    if score < CONFIG["min_score"]:
        return None
    
    return {
        **skill,
        "score": score,
        "reason": get_recommendation_reason(skill),
    }


def get_recommendation_reason(skill: dict) -> str:
    """生成推荐理由 - 突出高质量指标"""
    stats = skill.get("stats", {})
    latest = skill.get("latestVersion", {})
    reasons = []
    
    downloads = stats.get("downloads", 0)
    installs = stats.get("installsAllTime", 0)
    stars = stats.get("stars", 0)
    version = latest.get("version", "0.0.0")
    
    # 下载量（最直观的热度指标）
    if downloads >= 200:
        reasons.append(f"🔥 超热门 ({downloads} 下载)")
    elif downloads >= 100:
        reasons.append(f"🔥 热门 ({downloads} 下载)")
    elif downloads >= 50:
        reasons.append(f"热门 ({downloads} 下载)")
    
    # 安装量（真实用户数）
    if installs >= 50:
        reasons.append(f"✅ {installs} 人安装使用")
    elif installs >= 20:
        reasons.append(f"✅ {installs} 人安装")
    
    # Star（用户认可）
    if stars >= 5:
        reasons.append(f"⭐⭐⭐ 高评价 ({stars} 星)")
    elif stars >= 2:
        reasons.append(f"⭐⭐ 好评 ({stars} 星)")
    elif stars >= 1:
        reasons.append(f"⭐ 有好评 ({stars} 星)")
    
    # 版本稳定性
    if version >= "1.0.0":
        reasons.append("🏆 稳定版")
    
    # 检查匹配的关键词
    summary = skill.get("summary", "").lower()
    slug = skill.get("slug", "").lower()
    for interest in CONFIG["interests"][:5]:  # 只显示前几个匹配
        if interest in summary or interest in slug:
            reasons.append(f"📌 匹配：{interest}")
            break
    
    return " | ".join(reasons) if reasons else "高质量新技能"


def discover_skills():
    """主发现流程"""
    print("🔍 开始搜索新技能...", file=sys.stderr)
    
    installed = load_state(INSTALLED_FILE)
    recommended = load_state(RECOMMENDED_FILE)
    
    all_skills = []
    
    # 1. 获取最新的 skills
    print("  └─ 获取最新技能...", file=sys.stderr)
    new_skills = clawhub_explore(limit=100, sort="newest")
    for skill in new_skills:
        filtered = filter_skill(skill, installed, recommended)
        if filtered:
            all_skills.append(filtered)
    
    # 2. 按兴趣关键词搜索
    print(f"  └─ 按 {len(CONFIG['interests'])} 个关键词搜索...", file=sys.stderr)
    for keyword in CONFIG["interests"]:
        results = clawhub_search(keyword, limit=10)
        for skill in results:
            filtered = filter_skill(skill, installed, recommended)
            if filtered and filtered not in all_skills:
                all_skills.append(filtered)
    
    # 去重（按 slug）
    seen = set()
    unique_skills = []
    for skill in all_skills:
        if skill["slug"] not in seen:
            seen.add(skill["slug"])
            unique_skills.append(skill)
    
    # 按评分排序
    unique_skills.sort(key=lambda x: x["score"], reverse=True)
    
    # 取前 N 个推荐
    recommendations = unique_skills[:CONFIG["max_recommendations"]]
    
    print(f"\n✅ 找到 {len(recommendations)} 个推荐技能\n", file=sys.stderr)
    
    return recommendations


def format_recommendation(skill: dict) -> str:
    """格式化推荐消息"""
    stats = skill.get("stats", {})
    latest = skill.get("latestVersion", {})
    
    return f"""
━━━━━━━━━━━━━━━━━━━━
🆕 新 Skill 推荐

📦 名称：{skill.get('displayName', skill.get('slug'))}
🏷️  ID：`{skill.get('slug')}`

📝 描述：
{skill.get('summary', '无描述')[:200]}{'...' if len(skill.get('summary', '')) > 200 else ''}

📊 统计：
   • 版本：{latest.get('version', '?')}
   • 下载：{stats.get('downloads', 0)}
   • 安装：{stats.get('installsAllTime', 0)}
   • 评分：{'⭐' * min(5, stats.get('stars', 0) + (1 if stats.get('downloads', 0) > 50 else 0))}

💡 推荐理由：{skill.get('reason', '新发现')}

━━━━━━━━━━━━━━━━━━━━
回复「安装」自动安装此技能
回复「忽略」跳过此技能
回复「详情」查看完整信息
"""


def main():
    """入口函数"""
    recommendations = discover_skills()
    
    if not recommendations:
        print("✨ 暂无新技能推荐")
        return
    
    # 输出为 JSON 供主 agent 处理
    output = {
        "timestamp": datetime.now().isoformat(),
        "count": len(recommendations),
        "skills": recommendations
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 同时输出人类可读格式
    print("\n" + "="*50, file=sys.stderr)
    for skill in recommendations:
        print(format_recommendation(skill), file=sys.stderr)


if __name__ == "__main__":
    main()
