# MCP-Check 🛡️

A lightweight, zero-dependency security scanner for **MCP (Model Context Protocol)** server configurations.

As AI agents become more capable, they rely on MCP servers to interact with the real world. However, misconfigurations in `.mcp.json` or `claude_desktop_config.json` can expose sensitive data or introduce supply chain risks.

`mcp-check` is a CLI tool designed to audit your MCP configurations before deploying them to production.

## ✨ Features (Current MVP)

- **🔍 Secret Detection:** Automatically scans `env` variables for hardcoded secrets (e.g., `TOKEN`, `API_KEY`, `SECRET`) that should be managed via a secure vault.
- **⛓️ Supply Chain Protection:** Detects unpinned dependencies in `npx` or `uvx` commands (e.g., `npx -y some-package` without a specific version), preventing potential upstream poisoning attacks.

## 🚀 Quick Start

No installation required. Just run the script directly:

```bash
python scan.py test_config.json
Example Output
🛡️ Welcome to MCP Security Scanner (v1.0)
Scanning test_config.json ...

⚠️ [HIGH] Found plain text secret in server [github]!
   Variable: GITHUB_PERSONAL_ACCESS_TOKEN
   💡 Suggestion: Do not hardcode secrets. Use environment variables or a secret manager.

⚠️ [MEDIUM] Found unpinned dependency in server [github]!
   Package: @modelcontextprotocol/server-github
   💡 Suggestion: Pin specific versions (e.g., @1.0.0) to prevent supply chain attacks.

❌ Scan completed: 2 security issues found. Not ready for production!
🗺️ Roadmap
[ ] Add AST-based static analysis for MCP server code.
[ ] Support for scanning remote HTTP endpoints for authentication (OAuth).
[ ] CI/CD integration (GitHub Actions).
🤝 Contributing
 
This is an early-stage project. PRs, issues, and feature requests are highly welcome! Let's make the AI agent ecosystem safer together.
📄 License
MIT License
