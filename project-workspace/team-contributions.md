# Team Contributions

Fill in at the end. Name specific files, commits, ledger rows, or sections each person produced. "Helped with" is not enough.

| Person | Files or sections they produced | Ledger rows they verified | One thing they caught that the AI got wrong |
|---|---|---|---|
| Vinh Hoang (data owner) | `scripts/pull_data.py`, `data/raw/`, `data/clean/`, `api-manifest.md`, `data/variable-dictionary.md`; F2 rows in `evidence/failure-recovery-log.md`; F3 prediction + `model/leakage_test.py` + F3 rows (model card §6, failure log); Step 8 verification of `evidence/claim-ledger.csv`; `evidence/tool-check.md`; Step 3 plan review and the graded credential refusal (`ai-use-log.md`); team sync tooling (`tools/`, outside the submission) | All 11 (L1–L5, C1–C6), each recomputed from `data/raw/` with its source opened (Step 8) | Rejected the agent's first data-script plan as unclear (Step 3); by re-running the agent's script, caught that it erased the F2 evidence in `api-manifest.md` (fixed); in Step 8 found ledger C4 used inputs (2369/12224) that are not in the data |
| Yuhe Luo (research owner) | `skills/source-grounded-research/SKILL.md` + README; NotebookLM notebook "Pet-care - Warwick town vs Monroe town" and `evidence/notebooklm-transcript.md`; `evidence/corrected-brief.md` (F1); F1 and F4 rows in `evidence/failure-recovery-log.md`; claim-ledger rows L1–L5 and C1–C6; `evidence/step3-workflow-plan.md`; decision-frame measures table and prediction; README NotebookLM re-run commands | L1–L5 (citations opened, Q5 marked "not confirmed"); C1–C6 (F1 audit) | Marked NotebookLM's answer on NAICS 812910 vs 541940 (Q5) "not confirmed" because the cited CBP page does not define them; refuted the seeded brief's invented "4,491 pet-owning households" (C1) |
| Shiming Wan (model owner) | `model/fit_models.py`; `evidence/model-card.md` §1–5 and §7 (results, required study draft, feature importance, Warwick/Monroe residuals, limits); workbook 6.1–6.3 drafts | None yet | *(Shiming to fill in)* |

Percent of effort (should sum to 100) and any disagreement the instructor should know about:
