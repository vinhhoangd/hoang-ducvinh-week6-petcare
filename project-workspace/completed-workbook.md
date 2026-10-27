# Completed Workbook (type your answers here)

Summarize here; put full detail in the files named in each section.

## Section 1. Frame (Steps 1 and 2)
1.1 The one decision the client must make (copy from `evidence/decision-frame.md`):

The client must decide whether to open a dog daycare with grooming, as the first step toward a full-service pet-care center, in Warwick town or Monroe town, and whether to proceed now or pilot it first.

1.2 Which success rule did you add or tighten, and why?

We added: any claim about how many households own pets, or how much they spend on pet care, is `unknown` unless it comes from our own primary research. Why: no public dataset in this project counts pets, and the seeded AI brief (C1) invents a pet-owner count.

## Section 2. Tool check (Step 0)
2.1 Which agent do you use, and which tool was missing at first? How did you fix it?

Vinh uses Claude Code (neither `agy` nor `codex` is installed). Python 3.12.8, pandas 2.2.2 and scikit-learn 1.5.0 were already there. `nlm` was missing ("command not found"). The agent read the tool's GitHub README, checked that the PyPI package links to the same repo, and explained the install and its disclaimer. Vinh then personally ran `brew install uv` and `uv tool install notebooklm-mcp-cli`, and `nlm --version` printed 0.15.6. *(Yuhe and Shiming: add your own agent and anything that was missing on your machines.)*

2.2 Where is your Census key stored, and how do you know it is not in your submission folder?

In `project-workspace/.env`, one line `CENSUS_API=…`, typed by Vinh in `nano`. Git ignores it (`.gitignore` lists `.env`; `git status --ignored` shows `!! project-workspace/.env`). A ZIP does not obey `.gitignore`, so at submission we delete `.env` from the copy and search the copy for the key. *(Record that zero-hit search result here at submission.)*

## Section 3. Plan review (Step 3)
3.1 What did the agent plan for (a) the script, (b) the research skill, (c) the model?

(a) `pull_data.py`: read the key from `CENSUS_API` only, download ACS 2023 tracts (92) and towns with margins of error, CBP 2022 for 812910 and 541940, and FRED CUSR0000SS61031. Save raw files unchanged, write clean tables and `api-manifest.md` with the key replaced by `<KEY>`, and stop if tracts ≠ 92 or the key appears in any output. (b) `SKILL.md`: check the NotebookLM login (a human logs in), create "Pet-care - Warwick town vs Monroe town", add 4 public primary sources with `nlm source add`, ask 5+ questions with `nlm notebook query`, record citations, add claims to the ledger as unconfirmed, never delete. (c) `fit_models.py`: predict tract median income with an unpruned tree, a depth-3 tree and a random forest on a 25% held-out split (seed 42), leaving out the income MOE and IDs. Print train/held-out R² and MAE, feature importance, Warwick/Monroe out-of-sample residuals, and the leakage test.

3.2 What did you reject or revise, and why? (Detail goes in `ai-use-log.md`.)

Rejected the first version of the script plan because it was unclear and hard to follow; I could not have explained it at the demo. The agent rewrote it as 6 plain steps with a table of the 5 downloads, and I accepted that. Accepted the skill plan on one condition: the exact `nlm skill install` option for Claude Code must be checked and shown to us before it runs. *(The credential-refusal test is recorded in the AI-use log.)*

3.3 Did the plan use a held-out test set? If not, what did you change?

Yes: 25% of tracts are set aside with a fixed seed (42) before training, and the models never see them. Nothing needed changing.

## Section 4. API script (Step 4)
4.1 Prediction: how many tract rows will the ACS request return?  Observed:

Prediction (Vinh, 2026-10-27 14:52, before running): **92** tract rows. Observed: **92** rows, HTTP 200 (run 2026-10-27, `api-manifest.md`); the clean table matches `sample-data/orange_tracts_clean.csv` value for value.

4.2 Name two columns in your clean table and say whether each is a count, a percent, or a dollar amount, and whether it has a margin of error.

`median_income` is a **dollar amount** (2023 inflation-adjusted) and **has a margin of error** (`median_income_moe`, e.g. Warwick town $117,680 ± $8,605). `pct_renter` is a **percent** we compute from two ACS counts (renter-occupied ÷ occupied homes × 100); its MOE was not downloaded, so it carries uncertainty we do not show. CBP `establishments` is a plain **count** of businesses with employees, with no margin of error.

## Section 5. Research skill (Step 5)
5.1 Which of the five cited answers did you mark "not confirmed", and what did the cited passage actually say?

5.2 What does the NotebookLM answer depend on that you chose (sources)? What could bias it?

## Section 6. Models (Step 6)
6.1 Prediction before running: held-out R2 for the unpruned tree, depth-3 tree, forest.

6.2 Observed (copy from model card). What surprised you?

6.3 In your own words: why can a forest look better on held-out data than one tree?

## Section 7. Break and verify (Steps 7 and 8)
7.1 For F1 to F4, one sentence each: what you predicted, what happened, the repair. (Detail in `evidence/failure-recovery-log.md`.)

7.2 How many ledger claims ended as supported / proxy / unsupported / refuted?

## Section 8. Transfer and reflection (Steps 9 and 10)
8.1 First confusing instruction found in the transfer trial, and your fix:

8.2 What would break first if the client actually used this pipeline next year?

8.3 Feynman check (three sentences or fewer, no jargon): why a precise-looking model score does not prove a recommendation.

## ADI501 only: summary of Step 11 artifacts
Source-quality memo decision (adopt / adopt with conditions / do not adopt):

The single numeric guardrail from your model-risk note:

The one number that would change your pilot decision:
