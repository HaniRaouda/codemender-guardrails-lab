# Antigravity Agent Engineering Standards

## 1. Secrets & Credentials Policy
- NEVER hardcode secrets, API keys (e.g. AIzaSy...), tokens, or passwords in source files.
- ALWAYS retrieve secrets dynamically from environment variables using `process.env.GEMINI_API_KEY` or `os.environ.get('GEMINI_API_KEY')`.
- If a pre-commit check fails due to secret detection, immediately refactor the code to read from environment variables.

## 2. Database Security
- Parameterize all dynamic database queries. Never concatenate user input directly into SQL strings.
