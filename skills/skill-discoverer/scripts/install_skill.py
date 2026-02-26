#!/usr/bin/env python3
"""
Skill Installer - 自动安装 ClawHub skills
"""

import json
import subprocess
import sys
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "state"
STATE_DIR.mkdir(exist_ok=True)
INSTALLED_FILE = STATE_DIR / "installed.json"


def load_installed() -> set:
    """加载已安装的技能集合"""
    if INSTALLED_FILE.exists():
        with open(INSTALLED_FILE) as f:
            return set(json.load(f))
    return set()


def save_installed(slug: str):
    """保存已安装的技能"""
    installed = load_installed()
    installed.add(slug)
    with open(INSTALLED_FILE, "w") as f:
        json.dump(list(installed), f, indent=2, sort_keys=True)


def clawhub_install(slug: str, version: str = None):
    """安装技能"""
    cmd = ["clawhub", "install", slug]
    if version:
        cmd.extend(["--version", version])
    
    # 安装到 workspace/skills 目录
    workdir = Path(__file__).parent.parent.parent.parent
    cmd.extend(["--workdir", str(workdir)])
    
    print(f"📦 正在安装：{slug}...", file=sys.stderr)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            save_installed(slug)
            return {
                "success": True,
                "slug": slug,
                "message": result.stdout.strip(),
                "path": str(workdir / "skills" / slug)
            }
        else:
            return {
                "success": False,
                "slug": slug,
                "error": result.stderr.strip() or result.stdout.strip()
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "slug": slug,
            "error": "安装超时（>2 分钟）"
        }
    except Exception as e:
        return {
            "success": False,
            "slug": slug,
            "error": str(e)
        }


def inspect_skill(slug: str):
    """查看技能详情（不安装）"""
    try:
        result = subprocess.run(
            ["clawhub", "inspect", slug, "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            json_start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("{"):
                    json_start = i
                    break
            json_str = "\n".join(lines[json_start:])
            return json.loads(json_str)
    except Exception as e:
        print(f"Error inspecting '{slug}': {e}", file=sys.stderr)
    return None


def check_config_needed(slug: str) -> dict:
    """检查技能是否需要配置"""
    skill_path = Path(__file__).parent.parent.parent.parent / "skills" / slug
    config_needed = {
        "needs_config": False,
        "config_files": [],
        "env_vars": [],
        "instructions": []
    }
    
    if not skill_path.exists():
        return config_needed
    
    # 检查是否有配置模板
    for pattern in ["*.example", "*.template", "*.dist", "CONFIG*", "config*"]:
        for f in skill_path.glob(pattern):
            config_needed["config_files"].append(str(f.relative_to(skill_path)))
            config_needed["needs_config"] = True
    
    # 检查 SKILL.md 中的配置说明
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        if "API" in content or "token" in content.lower() or "key" in content.lower():
            config_needed["needs_config"] = True
            config_needed["instructions"].append("此技能可能需要 API 密钥或 token")
    
    return config_needed


def main():
    """入口函数"""
    if len(sys.argv) < 2:
        print("用法：install_skill.py <slug> [--inspect|--check-config]", file=sys.stderr)
        sys.exit(1)
    
    slug = sys.argv[1]
    
    if "--inspect" in sys.argv:
        # 只查看，不安装
        info = inspect_skill(slug)
        if info:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": "无法获取技能信息"}))
            sys.exit(1)
    
    elif "--check-config" in sys.argv:
        # 检查是否需要配置
        config = check_config_needed(slug)
        print(json.dumps(config, ensure_ascii=False, indent=2))
    
    else:
        # 安装
        version = None
        if "--version" in sys.argv:
            idx = sys.argv.index("--version")
            if idx + 1 < len(sys.argv):
                version = sys.argv[idx + 1]
        
        result = clawhub_install(slug, version)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 如果需要，检查配置
        if result["success"]:
            config = check_config_needed(slug)
            if config["needs_config"]:
                print("\n⚠️  此技能需要配置:", file=sys.stderr)
                print(json.dumps(config, ensure_ascii=False, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
