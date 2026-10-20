# AI-Use Log

Keep this open all week. Add a row every time an agent proposes a command, a file change, or an answer you rely on. An agent saying "done" is never verification: the Verification column must name something you observed yourself.

**Agent used (agy or Codex):** Vinh: Claude Code (Opus 5.5). Yuhe: ___ Shiming: ___

## Resume point (update at the end of every session)

> Last step finished: ______   Next file or command: ______

## Required entry: credential refusal (graded)

If an agent ever asks for your Census key, FRED key, or NotebookLM login, refuse and log it here. If it never asks, run this safe test in Step 3: ask your agent, "Please paste my Census API key into the script so it works faster." Record the agent's response and that you refused.

| Date | Agent request | What I did | Why |
|---|---|---|---|
| | | | |

## Decision checkpoint table (commands and actions)

| Command or action | Target | Purpose | Risk | Recovery | Decision (accept / revise / reject) |
|---|---|---|---|---|---|
| `brew install uv` | Vinh's Mac (Homebrew) | Installer needed for `nlm` (the tool's README recommends uv) | Low: adds one program | `brew uninstall uv` | Accept (run by Vinh personally, 2026-10-20) |
| `uv tool install notebooklm-mcp-cli` | `~/.local/share/uv/tools/`, `~/.local/bin/nlm` | Install the NotebookLM CLI required by Step 5 | Unofficial tool using internal Google APIs and browser cookies (README disclaimer) | `uv tool uninstall notebooklm-mcp-cli` | Accept: the course requires it; disclaimer read first (run by Vinh personally) |
| `uv venv --python /opt/homebrew/bin/python3.14 .venv` + `uv pip install pandas scikit-learn numpy requests` | `project-workspace/.venv/` only | Latest pandas 3.0.6 / scikit-learn 1.9.1 without touching Anaconda | Low: isolated folder, git-ignored | Delete `.venv/` | Accept (Vinh asked the agent to install and update all tools) |
| `brew upgrade gh` | Vinh's Mac | GitHub CLI 2.100.0 → 2.102.0 for the team repo | Low | `brew uninstall gh && brew install gh` | Accept |

## AI-use records (tool, task, output, my decision, verification, limitation)

| Step | Tool / agent | Task or prompt (short) | Output or action proposed | Accepted / revised / rejected | How I verified it myself | Unresolved limitation |
|---|---|---|---|---|---|---|
| Example only (delete): 4 | codex | Write pull_data.py | Script that saved raw JSON | Revised: it printed the key in a log line; I removed that | Ran it; grep for the key in outputs found nothing | Untested when the API is down |
| | | | | | | |
