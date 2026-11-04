# Transfer Trial (Step 9)

| Item | Entry |
|---|---|
| Who ran it (not the author of the script) | Planned tester: Shiming Wan, on his Ubuntu laptop with his own key (`team-agreement.md`). He ticked "transfer trial" on the shared checklist on 2026-11-03 14:55 ET but sent no details of the run before submission. |
| Date and machine type (Mac / Windows) | Not recorded |
| Steps given to them (paste the README commands you handed over) | The "How to re-run this analysis" section of `README.md`: one-time `uv venv --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt`, then `source .venv/bin/activate && set -a; . ./.env; set +a && python scripts/pull_data.py` |
| Minutes to first success (rows downloaded, manifest written) | Not recorded |
| Every intervention you had to make (what you said or typed) | Not recorded |
| First confusing instruction | Not recorded |
| Your fix | Not recorded |
| Rerun result after the fix (minutes, interventions) | Not recorded |

We are submitting without trial measurements rather than writing numbers nobody observed. The only runs we can document are by the script's author (Vinh, on his MacBook, 2026-10-27 and twice on 2026-11-03: all 5 requests HTTP 200, 92 tracts, key absent from every output; see `api-manifest.md`), and those do not count as a transfer trial.

Never copy the helper's key into this file or into your folder.
