---
name: source-grounded-research
description: Standard operating procedure for executing source-grounded research using NotebookLM CLI (nlm), verifying citations against primary public sources, and logging evidence.
version: 1.0.0
---

# Source-Grounded Research Skill

## Purpose
This skill defines the standardized protocol for conducting grounded research for **Case 4: Pet-care Daycare (Warwick town vs Monroe town)** using the `nlm` CLI. All factual assertions must be grounded in verified primary sources with explicit quotations.

## Governance & Security Rules
1. **Zero Credential Exposure**: Never handle, prompt for, store, or log Google credentials, session cookies, or tokens. Rely strictly on the human user's local terminal session verified via `nlm login --check`.
2. **Primary Public Sources Only**: Ingest only official government/statistical agency documentation or frozen local data. Unvetted third-party blogs or secondary summaries are prohibited.
3. **Non-Interactive Querying**: Always use `nlm notebook query <notebook-id> "<prompt>"` for reproducible, one-shot answers. Never launch interactive REPL sessions (`nlm chat start`).
4. **No Deletions**: Never run delete commands (`nlm notebook delete`, `nlm source delete`) without explicit human and instructor approval.
5. **No Citation, No Claim**: An answer without a verifiable quotation from the primary source is considered unconfirmed and cannot be entered as verified evidence.

---

## Workflow Steps

### Step 1: Pre-flight Authentication Check
Verify authentication status without exposing credentials:
```bash
nlm login --check
```

### Step 2: Create Standardized Notebook
Create the project notebook using the required naming convention `<Case> - <Town A> vs <Town B>`:
```bash
nlm notebook create "Pet-care - Warwick town vs Monroe town"
```
Record the returned `Notebook ID`. Optionally set an alias:
```bash
nlm alias set petcare <notebook-id>
```

### Step 3: Ingest 4 Primary Sources
Add the 4 public primary sources:

1. **Source 1 (ACS Methodology)**:
   ```bash
   nlm source add <notebook-id> --url "https://www.census.gov/programs-surveys/acs/about.html"
   ```
2. **Source 2 (CBP Scope & Employer Definition)**:
   ```bash
   nlm source add <notebook-id> --url "https://www.census.gov/programs-surveys/cbp/about.html"
   ```
3. **Source 3 (FRED Pet Inflation Price Index)**:
   ```bash
   nlm source add <notebook-id> --url "https://fred.stlouisfed.org/series/CUSR0000SS61031"
   ```
4. **Source 4 (Frozen Local Towns Data)**:
   Upload the verified local CSV `sample-data/orange_towns_clean.csv`:
   ```bash
   nlm source add <notebook-id> --file "sample-data/orange_towns_clean.csv"
   ```

Verify all 4 sources are attached:
```bash
nlm source list <notebook-id>
```

### Step 4: Execute 5 Grounded Queries
Run each query individually with `nlm notebook query`:

1. **CBP Scope (Self-employment / Non-employers)**:
   ```bash
   nlm notebook query <notebook-id> "Does County Business Patterns (CBP) or NAICS 812910 count non-employer pet care providers such as solo dog walkers and informal pet sitters, or only employer establishments?"
   ```

2. **FRED Price Index Interpretation**:
   ```bash
   nlm notebook query <notebook-id> "Is FRED series CUSR0000SS61031 measured in dollar amounts or is it a price index? Can it tell us the local price of grooming in Warwick or Monroe?"
   ```

3. **Census Pet Ownership Coverage**:
   ```bash
   nlm notebook query <notebook-id> "Does the Census American Community Survey (ACS) collect data on pet ownership, dog counts, or household pet care spending?"
   ```

4. **Income Comparison & Margin of Error Overlap**:
   ```bash
   nlm notebook query <notebook-id> "Comparing Warwick town and Monroe town in orange_towns_clean.csv, what are their median household incomes and margins of error? Do their confidence intervals overlap?"
   ```

5. **NAICS Code Distinction**:
   ```bash
   nlm notebook query <notebook-id> "What is the difference in scope between NAICS 812910 (Pet Care Services) and NAICS 541940 (Veterinary Services)?"
   ```

### Step 5: Citation Audit & Logging
1. For every query response, review the cited source passages.
2. Verify against the raw source text whether the citation directly supports the claim.
3. Record findings in `evidence/notebooklm-transcript.md`:
   - Notebook Name and ID
   - Sources table with URLs and justification for being primary sources
   - Questions table with command, question, shortened answer, exact quoted passage, confirmation status (`Confirmed` / `Not confirmed`), and target ledger row.
4. Record corresponding entries in `evidence/claim-ledger.csv`.
5. Answer reflection questions in `completed-workbook.md` Section 5.
