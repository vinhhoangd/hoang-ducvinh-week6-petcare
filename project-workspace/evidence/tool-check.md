# Tool Check (Step 0)

Do NOT write any key, token, or cookie in this file. Writing only that a key exists is fine.

| Tool | Command I ran | Output (version line only) | If it was missing, what I did |
|---|---|---|---|
| Python | `python3 --version` | `Python 3.12.8` | Already installed. |
| pandas / scikit-learn | `python3 -c "import pandas, sklearn; ..."` | `pandas 2.2.2 scikit-learn 1.5.0` | Already installed. |
| nlm | `nlm --version` | `nlm version 0.15.6` | Was "command not found". The agent read the README of github.com/jacob-bd/gemini-notebook-mcp-cli and checked that PyPI package `notebooklm-mcp-cli` links to that repo. It explained the install and its disclaimer (unofficial, uses internal Google APIs and browser cookies). Vinh then personally ran `brew install uv` (uv 0.13.4) and `uv tool install notebooklm-mcp-cli` on 2026-10-20. It installs into its own environment, and nothing else in Python changed. |
| Agent (agy or codex) | `claude --version` (Claude Code desktop app) | Claude Code, model Opus 5.5 | Neither `agy` nor `codex` is installed. We use Claude Code as the agent, the same as Weeks 3–5. |
| Census key stored in `.env` (yes/no, never the value) | `set -a; . ./.env; set +a` | **Yes** (2026-10-20). The agent confirmed only that the file has one `CENSUS_API=` line with a 40-character value; the key was never printed or shown to it | Vinh typed the key in `nano .env` personally. Git ignores `.env` (`git status --ignored` shows `!! project-workspace/.env`) |
| NotebookLM login (yes/no) | `nlm login` run by me in my own terminal | **Yes.** `nlm login --check` on 2026-10-20 printed "✓ Authentication valid!", profile `default` | Vinh ran `nlm login` personally and signed in in the browser. The agent ran only the read-only `--check`, which shows no cookies |

Account used for NotebookLM (school or personal Gmail, and why): School account (the student Google account). It worked on the first try, so the personal-Gmail fallback was not needed.
