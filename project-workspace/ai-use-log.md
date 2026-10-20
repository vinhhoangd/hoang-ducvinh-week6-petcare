# AI-Use Log

Keep this open all week. Add a row every time an agent proposes a command, a file change, or an answer you rely on. An agent saying "done" is never verification: the Verification column must name something you observed yourself.

**Agent used (agy or Codex):**

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
| Example only (delete): `nlm skill install agents --level project` | `.agents/skills/` in this folder | Teach the agent the NotebookLM commands | Overwrites an existing skill folder | Delete the folder and reinstall | Accept |
| | | | | | |

## AI-use records (tool, task, output, my decision, verification, limitation)

| Step | Tool / agent | Task or prompt (short) | Output or action proposed | Accepted / revised / rejected | How I verified it myself | Unresolved limitation |
|---|---|---|---|---|---|---|
| Example only (delete): 4 | codex | Write pull_data.py | Script that saved raw JSON | Revised: it printed the key in a log line; I removed that | Ran it; grep for the key in outputs found nothing | Untested when the API is down |
| | | | | | | |
