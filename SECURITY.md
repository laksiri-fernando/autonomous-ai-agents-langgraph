# Security Policy

## Supported Versions

We currently support the latest published version with security updates.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately by opening a [GitHub Security Advisory](https://github.com/<your-org>/autonomous-ai-agents-langgraph/security/advisories/new). Do **not** disclose it publicly via issues or discussions.

We will acknowledge receipt within 48 hours and provide an estimated timeline for a fix. We ask that you refrain from public disclosure until a patch is released.

## Security Considerations

This project uses large language models (LLMs) and the LangGraph framework. Be aware of the following risks:

- **Prompt Injection**: Malicious input may manipulate LLM behavior. Sanitize and validate all user-provided input before passing it to the model.
- **API Key Leakage**: The `.env` file and any secrets must never be committed to version control. The `.gitignore` already excludes `.env` — verify this before pushing.
- **Tool/Function Execution**: LangGraph agents can invoke tools and functions. Ensure that any custom tools exposed to the agent do not allow arbitrary code execution, file system access, or network calls unless strictly necessary and sandboxed.
- **Data Privacy**: LLM calls may send data to third-party APIs (e.g., OpenAI). Do not pass sensitive, personal, or confidential data unless you control the endpoint and have appropriate data processing agreements in place.
- **Dependency Vulnerabilities**: Regularly audit dependencies with `pip-audit` or `pip list --outdated` and apply security patches promptly.

## Responsible Disclosure

We will credit researchers who responsibly report vulnerabilities in the advisory metadata (unless they wish to remain anonymous). We aim to release fixes within 14 days of confirmation for critical issues.
