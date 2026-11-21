import json
import sys

# 1. 接收命令行参数（支持扫描任意配置文件）
# 如果用户运行 python scan.py xxx.json，就用 xxx.json；如果没写，默认用 test_config.json
target_file = sys.argv[1] if len(sys.argv) > 1 else 'test_config.json'

print(f"🛡️ 欢迎使用 MCP 安全安检仪 (第一版)")
print(f"正在扫描 {target_file} ...\n")

try:
    with open(target_file, 'r', encoding='utf-8') as file:
        config_data = json.load(file)
except Exception as e:
    print(f"❌ 读取配置文件失败，请检查文件路径。错误信息：{e}")
    sys.exit(1)

found_issues = 0
servers = config_data.get("mcpServers", {})

for server_name, server_info in servers.items():
    # 规则 1：寻找明文密码
    env_vars = server_info.get("env", {})
    for key, value in env_vars.items():
        if any(keyword in key.upper() for keyword in ["TOKEN", "KEY", "SECRET"]):
            if len(str(value)) > 5:
                print(f"⚠️ [高危警告] 在服务 [{server_name}] 中发现明文密钥！")
                print(f"   变量名: {key}")
                print("   💡 修复建议：请勿将敏感信息硬编码在配置文件中，请使用环境变量或密钥管理器。\n")
                found_issues += 1
                
    # 规则 2：寻找未锁定版本的供应链风险
    command = server_info.get("command", "")
    args = server_info.get("args", [])
    if command in ["npx", "uvx"] and "-y" in args:
        try:
            pkg_index = args.index("-y") + 1
            package_name = args[pkg_index]
            if "@" not in package_name[1:]: 
                print(f"⚠️ [中危警告] 在服务 [{server_name}] 中发现未固定版本的依赖！")
                print(f"   当前包名: {package_name}")
                print("   💡 修复建议：请在包名后指定具体的版本号（如 @1.0.0），防止上游代码被投毒导致供应链攻击。\n")
                found_issues += 1
        except IndexError:
            pass

# 3. 汇报总结
if found_issues > 0:
    print(f"❌ 扫描结束：共发现 {found_issues} 个安全漏洞。不符合生产环境要求！")
    sys.exit(1) # 返回非0状态码，方便以后接入 CI/CD
else:
    print("✅ 扫描结束：未发现明显的高危漏洞。")