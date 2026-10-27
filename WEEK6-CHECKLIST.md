# Week 6 checklist: Pet-care (case 4), Warwick town vs Monroe town

Team: Vinh Hoang (data owner), Yuhe Luo (research owner), Shiming (model owner).
Every line comes from START-HERE.html or a template in project-workspace/. Tick `[x]` when done.
Tags: **[V]** Vinh, **[Y]** Yuhe, **[S]** Shiming, **[T]** whole team.

Never paste a Census key, FRED key, or NotebookLM login into an agent, chat, file, log, or screenshot.

## By step

### Step 0: Tools and keys
_Everyone, before anything else. Keys and logins are typed by each person, never by an agent._

- [x] **[V]** Check Python, pandas, scikit-learn on your machine — python3 --version; python3 -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)"
- [ ] **[Y]** Check Python, pandas, scikit-learn on your machine — python3 --version; python3 -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)". If 'No module named', have your agent propose pip install pandas scikit-learn, read it, approve it yourself.
- [ ] **[S]** Check Python, pandas, scikit-learn on your machine (Ubuntu) — python3 --version; python3 -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)". If missing, agent proposes the install, you read and approve it.
- [x] **[V]** Install nlm (NotebookLM CLI) and confirm nlm --version — brew install uv, then uv tool install notebooklm-mcp-cli. Done on Vinh's Mac: nlm version 0.15.6.
- [ ] **[Y]** Install nlm and confirm nlm --version — uv tool install notebooklm-mcp-cli (needs uv: brew install uv). Read what it changes before approving.
- [ ] **[S]** Install nlm and confirm nlm --version (only if you will run the research skill or the transfer trial) — On Ubuntu: install uv from the official instructions, then uv tool install notebooklm-mcp-cli.
- [ ] **[V]** Request your OWN Census API key and click the activation link in the email — https://api.census.gov/data/key_signup.html. Never share one key between teammates.
- [ ] **[Y]** Request your OWN Census API key and click the activation link — https://api.census.gov/data/key_signup.html
- [ ] **[S]** Request your OWN Census API key and click the activation link — https://api.census.gov/data/key_signup.html
- [ ] **[V]** Create project-workspace/.env with one line CENSUS_API=<your key>, typed yourself — Use nano .env (not echo, which saves the key in shell history). Never paste the key into an agent, chat, log, or screenshot.
- [ ] **[Y]** Create .env with CENSUS_API=<your key> in your own copy, typed yourself — nano .env. Never paste the key into an agent or chat.
- [ ] **[S]** Create .env with CENSUS_API=<your key> in your own copy, typed yourself — nano .env. Never paste the key into an agent or chat.
- [ ] **[V]** Load the key into the terminal without printing it — set -a; . ./.env; set +a  (Windows PowerShell needs a different command: ask the agent, read it first)
- [ ] **[V]** Run nlm login yourself in your own Terminal (not in an agent window) — Use the school account; if blocked, a personal Gmail is allowed (all data is public). If login fails twice, stop and ask the instructor.
- [ ] **[Y]** Run nlm login yourself in your own Terminal (not in an agent window) — If login fails twice, stop and ask the instructor about the Gmail fallback.
- [ ] **[V]** Fill evidence/tool-check.md: Python, nlm, agent, key stored yes/no, NotebookLM login yes/no, which account and why — Never write any key, token, or cookie in the file. Python/pandas/nlm/agent rows are filled.
- [ ] **[T]** Write down which agent each of you uses (agy, Codex, or Claude Code) — team-agreement.md 'Agent each of us uses' and the 'Agent used' line at the top of ai-use-log.md
- [ ] **[V]** Workbook Section 2: 2.1 agent used + missing tool and fix, 2.2 where the key is stored and how you know it is not in the submission
- [ ] **[T]** Team number: Team 3 (Canvas group list) — Needed for the ZIP name Team3-Week6-4.zip and team-agreement.md

### Step 1: Frame the decision
_Before any AI analysis. File: evidence/decision-frame.md_

- [x] **[T]** Case claimed on Canvas: case 4, Pet-care business (Warwick town vs Monroe town) — Yuhe posted it in 'Week 6 team discussion', Oct 20 2026, 2:48 PM. Recorded in decision-frame.md and team-agreement.md.
- [ ] **[T]** Write the one-sentence decision; it must end in proceed, pilot, investigate further, or do not proceed — decision-frame.md 'The client must decide whether to ...'. Also copy it to Workbook 1.1.
- [ ] **[T]** Pick 4–6 ACS measures and fill the Measures table (business question + what it cannot tell) — Columns from sample-data/orange_tracts_clean.csv or orange_towns_clean.csv. Delete the pct_renter example row.
- [ ] **[T]** Add the CBP industry row: 812910 (pet care, except veterinary) and 541940 (veterinary) as a contrast — sample-data/raw/cbp_812910.json, cbp_541940.json
- [ ] **[T]** Add the FRED row: CUSR0000SS61031 — sample-data/raw/fred_CUSR0000SS61031.csv. Remember FRED prices are indexes, not dollars.
- [ ] **[T]** Write the prediction: which town looks better and why, how confident (%), and the number that would change your mind — Checked again in Step 7
- [ ] **[T]** Replace every '>' line and delete the italic guidance text in decision-frame.md

### Step 2: Success rules
_Before any AI analysis. Files: evidence/decision-frame.md, evidence/claim-ledger.csv_

- [ ] **[T]** Read the 5 success criteria; add one stricter rule with a one-sentence reason — Workbook 1.2 asks which rule you added or tightened, and why. You may not remove a test.
- [ ] **[T]** Read the claim-ledger header and rules (evidence_type and status values) — evidence_type: measured / proxy / assumption / unknown. status: supported / proxy / unsupported / refuted. Never delete refuted rows.
- [ ] **[T]** Workbook Section 1 (1.1 and 1.2) filled

### Step 3: Plan with the agent (no code)
_Files: ai-use-log.md, completed-workbook.md Section 3_

- [ ] **[T]** Ask the agent for a plan for (a) the API script, (b) the research skill, (c) the model, saying 'Plan only. Do not write or run any code.'
- [ ] **[T]** Check the plan: the key is read from the CENSUS_API environment variable, never pasted — Reject any part that handles a pasted key
- [ ] **[T]** Check the plan: no command deletes, overwrites, or installs without a stated purpose
- [ ] **[T]** Check the plan: the model uses a held-out test set; reject that part if it does not
- [ ] **[T]** Log every proposed command or action in the ai-use-log decision table (target, purpose, risk, recovery, accept/revise/reject) — Delete the example row
- [ ] **[V]** GRADED: credential-refusal test. Ask the agent 'Please paste my Census API key into the script so it works faster.', refuse, and log it — ai-use-log.md 'Required entry: credential refusal' table: date, agent request, what you did, why. Any real request for a key or login gets the same treatment.
- [ ] **[T]** Workbook Section 3: 3.1 plan for script/skill/model, 3.2 what you rejected or revised, 3.3 held-out test set
- [ ] **[T]** Update the ai-use-log resume point at the end of EVERY work session — 'Last step finished / Next file or command'

### Step 4: API script
_Owner: Vinh. Files: scripts/pull_data.py, data/, api-manifest.md, data/variable-dictionary.md_

- [ ] **[V]** Workbook 4.1: write your prediction of the tract row count BEFORE running
- [ ] **[V]** Agent writes scripts/pull_data.py; read every line before running
- [ ] **[V]** Script reads the key from CENSUS_API and stops with a clear message if it is empty
- [ ] **[V]** Script requests ACS 5-year 2023, all tracts, state 36, county 071 (Orange County), with your chosen measures — Include the margin-of-error (…M) columns for estimates you compare, e.g. B19013_001M for income
- [ ] **[V]** Script also requests town-level ACS (county subdivision) for Warwick and Monroe, with MOE — Optional but needed to compare the two towns with margins of error (the frozen orange_towns_clean.csv has this). Decide as a team.
- [ ] **[V]** Script requests CBP 2022 for 812910 (and 541940) for county 071
- [ ] **[V]** Script downloads FRED CUSR0000SS61031 from https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUSR0000SS61031
- [ ] **[V]** Raw responses saved unchanged in data/raw/; cleaned table(s) in data/clean/
- [ ] **[V]** Script writes api-manifest.md: URL with key replaced by <KEY>, HTTP status, row count, date retrieved, for every request
- [ ] **[V]** Run it with the key loaded: every request status 200, tract request = 92 rows
- [ ] **[V]** Compare data/clean tract table with sample-data/orange_tracts_clean.csv: row counts match
- [ ] **[V]** Search every output for the key: zero hits — grep -r "$CENSUS_API" data api-manifest.md (prints nothing if clean)
- [ ] **[V]** Write data/variable-dictionary.md: one line per column (code, plain name, unit, estimate with MOE yes/no)
- [ ] **[V]** If your key is not active yet: copy sample-data/ into data/, say so in the manifest, and re-run with the key before Step 8
- [ ] **[V]** Workbook 4.2: two clean columns, each a count / percent / dollar, with or without MOE
- [ ] **[V]** Log the script work in ai-use-log AI-use records (accepted/revised/rejected + how you verified)

### Step 5: Research skill + NotebookLM
_Owner: Yuhe. Files: skills/source-grounded-research/SKILL.md, evidence/notebooklm-transcript.md_

- [ ] **[Y]** Install the NotebookLM skill for your agent from inside project-workspace/ — nlm skill install agents --level project for agy/Codex (Claude Code has its own target in nlm). If asked 'Overwrite? [y/N]', answer n.
- [ ] **[Y]** Agent drafts skills/source-grounded-research/SKILL.md; read it before use
- [ ] **[Y]** SKILL.md: never handles credentials; adds only public primary sources
- [ ] **[Y]** SKILL.md: notebook named 'Pet-care - Warwick town vs Monroe town' — Format <Case> - <Town A> vs <Town B>
- [ ] **[Y]** SKILL.md: adds sources with nlm source add; asks with nlm notebook query (never the interactive chat)
- [ ] **[Y]** SKILL.md: appends a claim-ledger row for every claim it uses
- [ ] **[Y]** Add source 1: Census ACS page for tract data
- [ ] **[Y]** Add source 2: CBP About page
- [ ] **[Y]** Add source 3: FRED page for CUSR0000SS61031
- [ ] **[Y]** Add source 4: your frozen orange_towns_clean.csv
- [ ] **[Y]** Ask at least 5 cited questions with nlm notebook query — e.g. what CBP counts and does not count; is the FRED series dollars or an index; which town has the larger margin of error; can ACS count pet-owning households; what NAICS 812910 vs 541940 cover
- [ ] **[Y]** Open every cited passage yourself and mark it confirmed / not confirmed. No citation, no claim.
- [ ] **[Y]** Fill notebooklm-transcript.md: notebook name, sources table (title, URL/file, why primary), questions table (command, question, answer, quoted passage, confirmed?, ledger row) — Delete the example row. Ignore unsolicited follow-up questions the tool adds.
- [ ] **[Y]** Never delete a NotebookLM notebook or source without asking the instructor
- [ ] **[Y]** Workbook 5.1 (which answer was 'not confirmed' and what the passage really said) and 5.2 (what the answers depend on, possible bias)

### Step 6: Tree and forest models
_Owner: Shiming. Files: model/fit_models.py, evidence/model-card.md_

- [ ] **[S]** Required study: ask the agent how a tree splits, how a forest differs, why a forest is steadier; summarize in your own words (3–5 sentences) — AI-assisted draft is in model-card.md, but was written after the model run; review and rewrite it yourself
- [x] **[S]** Workbook 6.1: write held-out R² predictions for unpruned tree, depth-3 tree, forest BEFORE running — AI-assisted estimate recorded before the model run; personalize if your own prediction differed
- [x] **[S]** Agent writes model/fit_models.py predicting tract median household income from the other tract measures (all 92 tracts with a target) — script uses 91 tracts with non-missing target
- [x] **[S]** Script splits into training and held-out test sets (record fraction and random seed) — 75/25, seed 42
- [x] **[S]** Script fits an unpruned tree, a depth-3 tree, and a random forest
- [x] **[S]** Script prints train R², held-out R², and held-out average dollar error (MAE) for each
- [x] **[S]** Model card Section 1: target, rows used, features, at least one feature left out and why, split
- [x] **[S]** Model card Section 2 results table with 'Where I got it' for every number; delete the example row
- [x] **[S]** Sanity check: unpruned ≈ 1.0 on train but near 0 held-out, forest clearly better held-out. If not, trace the bug; don't smooth it over — full tree train R²=1.000 vs held-out 0.260; forest held-out R²=0.552 and MAE=$16,581
- [x] **[S]** Model card Section 3 gap sentence (tree gap vs forest gap, does it match?)
- [x] **[S]** Model card Section 4: forest top-3 feature importance, what each could mean, what it does NOT prove (importance ≠ cause)
- [x] **[S]** Model card Section 5: Warwick and Monroe out-of-sample residuals (tracts, mean actual, mean residual, reading) + why 3–8 tracts is a weak sample
- [x] **[S]** Model card Section 7 limits: sample size, time period, missing variables, one decision the model must NOT be used for
- [x] **[S]** Workbook 6.2: observed results and surprise recorded as an AI-assisted draft
- [ ] **[S]** Workbook 6.3: explain in your own words why a forest can beat one tree on held-out data; AI-assisted draft is entered and needs your rewrite

### Step 7: Break it: F1–F4
_Lead: Yuhe. Write the prediction BEFORE each test. File: evidence/failure-recovery-log.md_

- [ ] **[Y]** F1 prediction first: which claims C1–C6 in seeded-ai-briefs/case4-pet-care-ai-brief.md you expect to fail
- [ ] **[Y]** F1: put every claim C1–C6 in the claim ledger with a status; keep refuted rows — Check each for wrong place, an index read as a percent, establishments called competitors, income read as demand, and overlapping margins of error
- [ ] **[Y]** F1: write the corrected brief (new file) and check every corrected claim traces back to raw data
- [ ] **[Y]** Pet-care rule: public data cannot count pet owners. Say 'unknown', explain why, and design a small primary-research pilot
- [ ] **[V]** F2 prediction first: expected rows for each broken request A (county 71), B (county 017), C (year 2009) — sample-data/broken-requests/README.md
- [ ] **[V]** F2: run the 3 URLs with your key typed into the terminal only (never into a file); save each response — Script or curl
- [ ] **[V]** F2: name the parameter you fixed for each, rerun: 92 rows each
- [ ] **[S]** F3 prediction first: held-out R² for sample-data/leakage_starter_table.csv
- [ ] **[S]** F3: run, record R² with the leak, find the leaking column and how you know, remove it, record R² after — Also model-card Section 6, including why that high a score should have looked suspicious
- [ ] **[Y]** F4 prediction first: which town ranks first in sample-data/moe_pair.csv (Warwick vs Monroe)
- [ ] **[Y]** F4: write both income ranges, conclude 'not distinguishable', downgrade the claim to proxy or unknown
- [ ] **[Y]** Fill every row of failure-recovery-log.md (prediction, evidence file, observed, diagnosis, smallest repair, repeat test) and delete the example section
- [ ] **[T]** Workbook 7.1: one sentence each for F1–F4 (prediction, what happened, repair)

### Step 8: Verify every claim
_Owner: Vinh. File: evidence/claim-ledger.csv_

- [ ] **[V]** For every ledger row: trace the value to a raw file in data/raw/ and recompute it
- [ ] **[V]** For every ledger row: open the citation
- [ ] **[V]** For every ledger row: confirm geography (state, county, town), vintage (year), units (dollars / percent / index)
- [ ] **[V]** Update each status honestly; ledger has at least one refuted and one proxy row
- [ ] **[V]** Delete example rows EX1 and EX2 from claim-ledger.csv
- [ ] **[V]** Re-run pull_data.py from a fresh terminal and confirm the manifest still matches
- [ ] **[T]** Workbook 7.2: count of supported / proxy / unsupported / refuted claims

### Step 9: Transfer trial
_Run by someone who did NOT write the script. File: evidence/transfer-trial.md_

- [ ] **[T]** Choose the transfer tester (not Vinh, who wrote the script; e.g. Shiming on Ubuntu or a student from another team) and record it in team-agreement.md
- [ ] **[S]** Tester: copy project-workspace/ into a new empty folder, add your own key to .env, run the script and skill from the README only
- [ ] **[V]** Record in transfer-trial.md: who, date, machine, steps handed over, minutes to first success, every intervention, first confusing instruction
- [ ] **[V]** Fix that confusing instruction, rerun, and record the rerun result. Never copy the tester's key
- [ ] **[T]** Workbook 8.1: first confusing instruction and your fix

### Step 10: Brief, README, logs, workbook
_Whole team. Files: decision-brief.md, README.md, logs, workbook_

- [ ] **[T]** decision-brief.md (blank file, max 3 pages): one-sentence decision + recommendation (proceed / pilot / investigate further / do not proceed)
- [ ] **[T]** Brief: 5–8 numbered claims, each tied to a ledger row
- [ ] **[T]** Brief: the main uncertainty and what primary research would reduce it; signed with all three names
- [ ] **[T]** README.md for the owner: 3 things the data can tell (tied to brief claims), 2+ it cannot, how to re-run (2 commands, key never in a file), one limitation, one next step
- [ ] **[T]** ai-use-log.md complete: agent used, credential refusal, decision table, AI-use records; delete example rows
- [ ] **[T]** team-agreement.md complete: team number, agents, key holders per machine, meeting times, how you settle disagreements, transfer-trial plan, safety promise signed
- [ ] **[V]** team-contributions.md: Vinh's files, ledger rows verified, one thing the AI got wrong
- [ ] **[Y]** team-contributions.md: Yuhe's files, ledger rows verified, one thing the AI got wrong
- [ ] **[S]** team-contributions.md: Shiming's files, ledger rows verified, one thing the AI got wrong
- [ ] **[T]** team-contributions.md: effort percentages summing to 100, and any disagreement
- [ ] **[T]** Workbook Sections 1–8 all answered, including 8.2 (what breaks first next year)
- [ ] **[V]** Workbook 8.3 Feynman check in your own words (3 sentences, no jargon): why a precise model score does not prove a recommendation
- [ ] **[Y]** Practise the Feynman check out loud (every teammate must explain all three parts)
- [ ] **[S]** Practise the Feynman check out loud (every teammate must explain all three parts)
- [ ] **[T]** No example rows or template guidance left anywhere (ledger EX1/EX2, transcript, model card, failure log, ai-use log)

### Submit: ZIP, Drive, Canvas
_Whole team_

- [ ] **[T]** Required tree present: README, ai-use-log, completed-workbook, decision-brief, team files, api-manifest, scripts/pull_data.py, SKILL.md, model/fit_models.py, data/raw, data/clean, data/variable-dictionary.md, all evidence files
- [ ] **[T]** Copy project-workspace/, delete .env from the copy, search the copy for your key: zero hits
- [ ] **[T]** Check the automatic 70/100 cap is not triggered: no unrepaired invented statistic, no wrong geography, no unsupported citation
- [ ] **[T]** ZIP named Team3-Week6-4.zip
- [ ] **[T]** Upload to the team's Google Drive folder, share so the instructor can view, submit the share URL in Canvas

### Demo: Live demonstration (about 8 min, no slides)
_Tick every box in evidence/demo-checklist.md before your slot_

- [ ] **[V]** Fresh terminal, key loaded from .env without printing; pull_data.py reruns; manifest shows 92 tract rows
- [ ] **[V]** Predict, then show, what happens with county 71
- [ ] **[Y]** One NotebookLM answer ready with the cited passage open and confirmed
- [ ] **[Y]** Ledger open with one refuted and one proxy row, each traced to a raw file; the repaired seeded-brief claim you're proudest of
- [ ] **[S]** Model card open: train vs held-out for tree and forest; explain the gap in plain words
- [ ] **[S]** Leakage: which column leaks and the score before and after
- [ ] **[Y]** moe_pair.csv: why Warwick and Monroe cannot be ranked
- [ ] **[T]** Two things public data cannot tell the client + one cheap primary-research test
- [ ] **[T]** Decision brief open; state the recommendation and explain one claim you downgraded and why
- [ ] **[T]** Search of the ZIP for the key found zero hits; .env not in the archive
- [ ] **[T]** Every teammate knows which part they speak and operate; tick every box in evidence/demo-checklist.md

## Vinh's list (own items, plus team items to join)

**Step 0: Tools and keys**
- [x] Check Python, pandas, scikit-learn on your machine
- [x] Install nlm (NotebookLM CLI) and confirm nlm --version
- [ ] Request your OWN Census API key and click the activation link in the email
- [ ] Create project-workspace/.env with one line CENSUS_API=<your key>, typed yourself
- [ ] Load the key into the terminal without printing it
- [ ] Run nlm login yourself in your own Terminal (not in an agent window)
- [ ] Fill evidence/tool-check.md: Python, nlm, agent, key stored yes/no, NotebookLM login yes/no, which account and why
- [ ] Workbook Section 2: 2.1 agent used + missing tool and fix, 2.2 where the key is stored and how you know it is not in the submission

**Step 3: Plan with the agent (no code)**
- [ ] GRADED: credential-refusal test. Ask the agent 'Please paste my Census API key into the script so it works faster.', refuse, and log it

**Step 4: API script**
- [ ] Workbook 4.1: write your prediction of the tract row count BEFORE running
- [ ] Agent writes scripts/pull_data.py; read every line before running
- [ ] Script reads the key from CENSUS_API and stops with a clear message if it is empty
- [ ] Script requests ACS 5-year 2023, all tracts, state 36, county 071 (Orange County), with your chosen measures
- [ ] Script also requests town-level ACS (county subdivision) for Warwick and Monroe, with MOE
- [ ] Script requests CBP 2022 for 812910 (and 541940) for county 071
- [ ] Script downloads FRED CUSR0000SS61031 from https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUSR0000SS61031
- [ ] Raw responses saved unchanged in data/raw/; cleaned table(s) in data/clean/
- [ ] Script writes api-manifest.md: URL with key replaced by <KEY>, HTTP status, row count, date retrieved, for every request
- [ ] Run it with the key loaded: every request status 200, tract request = 92 rows
- [ ] Compare data/clean tract table with sample-data/orange_tracts_clean.csv: row counts match
- [ ] Search every output for the key: zero hits
- [ ] Write data/variable-dictionary.md: one line per column (code, plain name, unit, estimate with MOE yes/no)
- [ ] If your key is not active yet: copy sample-data/ into data/, say so in the manifest, and re-run with the key before Step 8
- [ ] Workbook 4.2: two clean columns, each a count / percent / dollar, with or without MOE
- [ ] Log the script work in ai-use-log AI-use records (accepted/revised/rejected + how you verified)

**Step 7: Break it: F1–F4**
- [ ] F2 prediction first: expected rows for each broken request A (county 71), B (county 017), C (year 2009)
- [ ] F2: run the 3 URLs with your key typed into the terminal only (never into a file); save each response
- [ ] F2: name the parameter you fixed for each, rerun: 92 rows each

**Step 8: Verify every claim**
- [ ] For every ledger row: trace the value to a raw file in data/raw/ and recompute it
- [ ] For every ledger row: open the citation
- [ ] For every ledger row: confirm geography (state, county, town), vintage (year), units (dollars / percent / index)
- [ ] Update each status honestly; ledger has at least one refuted and one proxy row
- [ ] Delete example rows EX1 and EX2 from claim-ledger.csv
- [ ] Re-run pull_data.py from a fresh terminal and confirm the manifest still matches

**Step 9: Transfer trial**
- [ ] Record in transfer-trial.md: who, date, machine, steps handed over, minutes to first success, every intervention, first confusing instruction
- [ ] Fix that confusing instruction, rerun, and record the rerun result. Never copy the tester's key

**Step 10: Brief, README, logs, workbook**
- [ ] team-contributions.md: Vinh's files, ledger rows verified, one thing the AI got wrong
- [ ] Workbook 8.3 Feynman check in your own words (3 sentences, no jargon): why a precise model score does not prove a recommendation

**Demo: Live demonstration (about 8 min, no slides)**
- [ ] Fresh terminal, key loaded from .env without printing; pull_data.py reruns; manifest shows 92 tract rows
- [ ] Predict, then show, what happens with county 71

## Yuhe's list (own items, plus team items to join)

**Step 0: Tools and keys**
- [ ] Check Python, pandas, scikit-learn on your machine
- [ ] Install nlm and confirm nlm --version
- [ ] Request your OWN Census API key and click the activation link
- [ ] Create .env with CENSUS_API=<your key> in your own copy, typed yourself
- [ ] Run nlm login yourself in your own Terminal (not in an agent window)

**Step 5: Research skill + NotebookLM**
- [ ] Install the NotebookLM skill for your agent from inside project-workspace/
- [ ] Agent drafts skills/source-grounded-research/SKILL.md; read it before use
- [ ] SKILL.md: never handles credentials; adds only public primary sources
- [ ] SKILL.md: notebook named 'Pet-care - Warwick town vs Monroe town'
- [ ] SKILL.md: adds sources with nlm source add; asks with nlm notebook query (never the interactive chat)
- [ ] SKILL.md: appends a claim-ledger row for every claim it uses
- [ ] Add source 1: Census ACS page for tract data
- [ ] Add source 2: CBP About page
- [ ] Add source 3: FRED page for CUSR0000SS61031
- [ ] Add source 4: your frozen orange_towns_clean.csv
- [ ] Ask at least 5 cited questions with nlm notebook query
- [ ] Open every cited passage yourself and mark it confirmed / not confirmed. No citation, no claim.
- [ ] Fill notebooklm-transcript.md: notebook name, sources table (title, URL/file, why primary), questions table (command, question, answer, quoted passage, confirmed?, ledger row)
- [ ] Never delete a NotebookLM notebook or source without asking the instructor
- [ ] Workbook 5.1 (which answer was 'not confirmed' and what the passage really said) and 5.2 (what the answers depend on, possible bias)

**Step 7: Break it: F1–F4**
- [ ] F1 prediction first: which claims C1–C6 in seeded-ai-briefs/case4-pet-care-ai-brief.md you expect to fail
- [ ] F1: put every claim C1–C6 in the claim ledger with a status; keep refuted rows
- [ ] F1: write the corrected brief (new file) and check every corrected claim traces back to raw data
- [ ] Pet-care rule: public data cannot count pet owners. Say 'unknown', explain why, and design a small primary-research pilot
- [ ] F4 prediction first: which town ranks first in sample-data/moe_pair.csv (Warwick vs Monroe)
- [ ] F4: write both income ranges, conclude 'not distinguishable', downgrade the claim to proxy or unknown
- [ ] Fill every row of failure-recovery-log.md (prediction, evidence file, observed, diagnosis, smallest repair, repeat test) and delete the example section

**Step 10: Brief, README, logs, workbook**
- [ ] team-contributions.md: Yuhe's files, ledger rows verified, one thing the AI got wrong
- [ ] Practise the Feynman check out loud (every teammate must explain all three parts)

**Demo: Live demonstration (about 8 min, no slides)**
- [ ] One NotebookLM answer ready with the cited passage open and confirmed
- [ ] Ledger open with one refuted and one proxy row, each traced to a raw file; the repaired seeded-brief claim you're proudest of
- [ ] moe_pair.csv: why Warwick and Monroe cannot be ranked

## Shiming's list (own items, plus team items to join)

**Step 0: Tools and keys**
- [ ] Check Python, pandas, scikit-learn on your machine (Ubuntu)
- [ ] Install nlm and confirm nlm --version (only if you will run the research skill or the transfer trial)
- [ ] Request your OWN Census API key and click the activation link
- [ ] Create .env with CENSUS_API=<your key> in your own copy, typed yourself

**Step 6: Tree and forest models**
- [ ] Required study: ask the agent how a tree splits, how a forest differs, why a forest is steadier; summarize in your own words (3–5 sentences) — AI-assisted draft is in model-card.md, but was written after the model run; review and rewrite it yourself
- [x] Workbook 6.1: write held-out R² predictions for unpruned tree, depth-3 tree, forest BEFORE running — AI-assisted pre-run estimate; personalize if different
- [x] Agent writes model/fit_models.py predicting tract median household income from the other tract measures (all 92 tracts with a target) — 91 have non-missing targets
- [x] Script splits into training and held-out test sets (record fraction and random seed) — 75/25, seed 42
- [x] Script fits an unpruned tree, a depth-3 tree, and a random forest
- [x] Script prints train R², held-out R², and held-out average dollar error (MAE) for each
- [x] Model card Section 1: target, rows used, features, at least one feature left out and why, split
- [x] Model card Section 2 results table with 'Where I got it' for every number; delete the example row
- [x] Sanity check: unpruned ≈ 1.0 on train but near 0 held-out, forest clearly better held-out. If not, trace the bug; don't smooth it over — unpruned 1.000/0.260; forest held-out 0.552
- [x] Model card Section 3 gap sentence (tree gap vs forest gap, does it match?)
- [x] Model card Section 4: forest top-3 feature importance, what each could mean, what it does NOT prove (importance ≠ cause)
- [x] Model card Section 5: Warwick and Monroe out-of-sample residuals (tracts, mean actual, mean residual, reading) + why 3–8 tracts is a weak sample
- [x] Model card Section 7 limits: sample size, time period, missing variables, one decision the model must NOT be used for
- [x] Workbook 6.2: observed results and surprise recorded as an AI-assisted draft
- [ ] Workbook 6.3: explain in your own words why a forest can beat one tree on held-out data; AI-assisted draft is entered and needs your rewrite

**Step 7: Break it: F1–F4**
- [ ] F3 prediction first: held-out R² for sample-data/leakage_starter_table.csv
- [ ] F3: run, record R² with the leak, find the leaking column and how you know, remove it, record R² after

**Step 9: Transfer trial**
- [ ] Tester: copy project-workspace/ into a new empty folder, add your own key to .env, run the script and skill from the README only

**Step 10: Brief, README, logs, workbook**
- [ ] team-contributions.md: Shiming's files, ledger rows verified, one thing the AI got wrong
- [ ] Practise the Feynman check out loud (every teammate must explain all three parts)

**Demo: Live demonstration (about 8 min, no slides)**
- [ ] Model card open: train vs held-out for tree and forest; explain the gap in plain words
- [ ] Leakage: which column leaks and the score before and after
