#!/usr/bin/env python3
"""
WeChat Article Studio - Setup Script

Run this once after installing the skill to:
1. Check Python version (3.10+ required)
2. Install Python dependencies (Pillow, numpy)
3. Guide user to create USER-PROFILE.md
4. Generate wechat_config.json from template
5. Run a self-test

Usage:
    python setup.py

Exit codes:
    0 = all checks passed
    1 = some checks failed, see output
"""

import sys
import os
import subprocess
import json
import shutil

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ok(msg):
    print(f"  {GREEN}[OK]{RESET} {msg}")


def fail(msg):
    print(f"  {RED}[FAIL]{RESET} {msg}")


def warn(msg):
    print(f"  {YELLOW}[WARN]{RESET} {msg}")


def info(msg):
    print(f"  {BLUE}[INFO]{RESET} {msg}")


def header(msg):
    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}  {msg}{RESET}")
    print(f"{BOLD}{'='*50}{RESET}")


def check_python_version():
    """Check Python >= 3.10"""
    header("1/5 检查 Python 版本")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 10:
        ok(f"Python {version_str} ({sys.executable})")
        return True
    else:
        fail(f"Python {version_str} 版本过低，需要 3.10+")
        info("请安装 Python 3.10 或更高版本: https://www.python.org/downloads/")
        return False


def check_pip():
    """Check pip is available"""
    header("2/5 检查 pip")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            check=True,
        )
        ok("pip 可用")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        fail("pip 不可用")
        info("请安装 pip: https://pip.pypa.io/en/stable/installation/")
        return False


def install_dependencies():
    """Install Pillow and numpy"""
    header("3/5 安装 Python 依赖")
    
    requirements_path = os.path.join(SKILL_DIR, "requirements.txt")
    
    # Check if already installed
    missing = []
    try:
        import PIL
        ok(f"Pillow {PIL.__version__} 已安装")
    except ImportError:
        missing.append("Pillow")
        warn("Pillow 未安装")
    
    try:
        import numpy
        ok(f"numpy {numpy.__version__} 已安装")
    except ImportError:
        missing.append("numpy")
        warn("numpy 未安装")
    
    if not missing:
        ok("所有依赖已就绪")
        return True
    
    info(f"正在安装: {', '.join(missing)}")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + missing,
            check=True,
            capture_output=True,
            text=True,
        )
        ok(f"安装成功: {', '.join(missing)}")
        return True
    except subprocess.CalledProcessError as e:
        fail(f"安装失败: {e.stderr}")
        info(f"请手动安装: {sys.executable} -m pip install {' '.join(missing)}")
        info("如果权限不足，尝试: python -m venv .venv && .venv/Scripts/pip install Pillow numpy")
        return False


def check_user_profile():
    """Check if USER-PROFILE.md exists and is filled"""
    header("4/5 检查账号配置")
    
    profile_path = os.path.join(SKILL_DIR, "USER-PROFILE.md")
    template_path = os.path.join(SKILL_DIR, "USER-PROFILE-TEMPLATE.md")
    
    if not os.path.exists(profile_path):
        if os.path.exists(template_path):
            shutil.copy(template_path, profile_path)
            warn("已从模板创建 USER-PROFILE.md，但还未填写")
        else:
            fail("USER-PROFILE-TEMPLATE.md 不存在，skill 安装可能不完整")
            return False
    
    # Check if profile is filled (no placeholder text)
    with open(profile_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    placeholders = ["替换为", "______", "你的职业", "你的AppID"]
    unfilled = [p for p in placeholders if p in content]
    
    if unfilled:
        warn(f"USER-PROFILE.md 存在但未填写完整（发现占位符: {', '.join(unfilled[:3])}）")
        print(f"""
  {BOLD}请填写 USER-PROFILE.md:{RESET}
  文件位置: {profile_path}

  {BOLD}必须填写的字段:{RESET}
  1. 你是谁（职业、正在做的事、专长）
  2. 目标用户（读者画像、痛点）
  3. 表达风格（期望的语气、不要的风格）
  4. 微信公众号信息（AppID、AppSecret、作者署名）

  填好后重新运行 setup.py 验证。
""")
        return False
    else:
        ok("USER-PROFILE.md 已填写")
        return True


def check_wechat_config():
    """Check if wechat_config.json exists and is configured"""
    header("5/5 检查微信配置")
    
    config_path = os.path.join(SKILL_DIR, "assets", "wechat_config.json")
    template_path = os.path.join(SKILL_DIR, "assets", "wechat_config.template.json")
    
    if not os.path.exists(config_path):
        if os.path.exists(template_path):
            shutil.copy(template_path, config_path)
            warn("已从模板创建 wechat_config.json，但还未配置")
        
        # Try to extract from USER-PROFILE.md
        profile_path = os.path.join(SKILL_DIR, "USER-PROFILE.md")
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = f.read()
            
            info("尝试从 USER-PROFILE.md 提取配置...")
            # Simple extraction - the AI will do this more intelligently
            # But we can at least check if the profile has the info
            if "wx" in profile.lower() and "app_id" not in profile.lower():
                info("请在 USER-PROFILE.md 第 6 节填写微信 AppID 和 AppSecret")
        
        print(f"""
  {BOLD}请配置 wechat_config.json:{RESET}
  文件位置: {config_path}

  {BOLD}必须填写的字段:{RESET}
  - wechat.app_id: 你的公众号 AppID
  - wechat.app_secret: 你的公众号 AppSecret
  - author: 作者署名

  获取方式: 微信公众平台 → 设置与开发 → 基本配置

  填好后重新运行 setup.py 验证。
""")
        return False
    
    # Check if config is filled
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    app_id = config.get("wechat", {}).get("app_id", "")
    if "替换为" in app_id or not app_id:
        warn("wechat_config.json 存在但 app_id 未配置")
        return False
    
    ok(f"wechat_config.json 已配置 (app_id: {app_id[:6]}...)")
    
    # Check article_count
    count = config.get("article_count", 0)
    if count == 0:
        info("article_count 未设置，首次发布将从第 1 篇开始")
    else:
        ok(f"当前原创篇数: 第 {count} 篇")
    
    return True


def run_self_test():
    """Run a quick self-test to verify scripts can import"""
    header("自测：脚本导入检查")
    
    scripts_dir = os.path.join(SKILL_DIR, "scripts")
    sys.path.insert(0, scripts_dir)
    
    results = []
    
    try:
        from wechat_template import WeChatTemplate
        ok("wechat_template.py 导入成功")
        
        # Test render
        t = WeChatTemplate(config_path=os.path.join(SKILL_DIR, "assets", "wechat_config.json"), theme="blue")
        html = t.render({
            "opening_text": "test",
            "sections": [
                {"type": "title", "text": "test"},
                {"type": "body", "paragraphs": ["hello"]},
            ],
        })
        assert len(html) > 100, "HTML too short"
        ok("模板渲染测试通过")
        results.append(True)
    except Exception as e:
        fail(f"wechat_template.py 导入失败: {e}")
        results.append(False)
    
    try:
        from wechat_publish import publish
        ok("wechat_publish.py 导入成功")
        results.append(True)
    except Exception as e:
        fail(f"wechat_publish.py 导入失败: {e}")
        results.append(False)
    
    try:
        import PIL.Image
        import numpy
        ok("process_images.py 依赖检查通过")
        results.append(True)
    except ImportError as e:
        fail(f"process_images.py 依赖缺失: {e}")
        results.append(False)
    
    return all(results)


def print_summary(results):
    """Print summary and next steps"""
    header("检查结果汇总")
    
    labels = [
        "Python 版本",
        "pip 可用",
        "Python 依赖",
        "USER-PROFILE.md",
        "wechat_config.json",
    ]
    
    all_passed = True
    for label, passed in zip(labels, results):
        if passed:
            ok(label)
        else:
            fail(label)
            all_passed = False
    
    print()
    if all_passed:
        print(f"  {GREEN}{BOLD}所有检查通过！可以开始使用了。{RESET}")
        print(f"""
  {BOLD}下一步:{RESET}
  告诉 AI: "帮我写一篇关于 XXX 的公众号文章"

  AI 会自动完成: 写作 → 配图 → 清洗 → 上传 → 小清新排版 → 发布到草稿箱
""")
    else:
        print(f"  {YELLOW}{BOLD}部分检查未通过，请按提示完成配置后重新运行 setup.py{RESET}")
        print(f"""
  运行命令: python {os.path.join(SKILL_DIR, 'scripts', 'setup.py')}
""")
    
    return all_passed


def main():
    print(f"\n{BOLD}微信公众号写作工作室 - 环境检查{RESET}")
    print(f"Skill 目录: {SKILL_DIR}")
    
    results = []
    results.append(check_python_version())
    results.append(check_pip())
    
    if results[-1]:  # Only try to install if pip is available
        results.append(install_dependencies())
    else:
        results.append(False)
    
    results.append(check_user_profile())
    results.append(check_wechat_config())
    
    # Only run self-test if deps are installed
    if results[2]:
        run_self_test()
    
    all_passed = print_summary(results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
