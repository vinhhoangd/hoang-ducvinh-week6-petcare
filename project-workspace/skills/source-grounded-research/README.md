Student work goes here (created in the Start Here steps). Keep this note.

# Source-Grounded Research Skill Guide

This folder contains the reproducible research workflow (`SKILL.md`) for **Case 4: Pet-care Daycare (Warwick town vs. Monroe town)** using the NotebookLM CLI (`nlm`).

Please read this guide before running or adapting the skill.

---

## 1. Prerequisites (Read First Before Use)

1. **CLI Installation**:
   Ensure `nlm` (version 0.15.6 or later) is installed via `uv`:
   ```bash
   uv tool install notebooklm-mcp-cli
   ```
2. **Human Authentication Gate**:
   You must authenticate personally in your own terminal before invoking the skill:
   ```bash
   nlm login
   ```
   Verify authentication status at any time with the read-only check:
   ```bash
   nlm login --check
   ```
3. **Zero Credential Exposure**:
   The skill and its scripts **never** handle, prompt for, or log Google credentials, cookies, or API tokens. Any agent asking for credentials or cookies must be immediately refused.

---

## 2. Safety & Governance Rules

* **No Destructive Operations**: Never run delete commands (`nlm notebook delete` or `nlm source delete`) without explicit permission from the course instructor.
* **Non-Interactive Querying**: Always use `nlm notebook query <notebook-id> "<prompt>"` for reproducible, one-shot answers. Never launch interactive REPL sessions (`nlm chat start`), which trap non-interactive agents.
* **Public Primary Sources Only**: Only official statistical agency documentation and verified frozen local datasets may be ingested. Never upload unvetted blogs or secondary opinion pieces.
* **"No Citation, No Claim" Rule**: An AI answer without an exact verifiable quotation from the underlying primary source must be marked `Not confirmed` and cannot be ledgered as evidence.
* **Ignore AI Follow-up Prompts**: NotebookLM frequently appends unsolicited follow-up suggestions (e.g., *"Would you like to explore..."*). These are conversational prompts, not evidence, and must be ignored.

---

## 3. Ingested Primary Sources

The skill attaches four vetted, public primary sources:

| # | Source Title | Location | Why It Is a Primary Source |
|---|---|---|---|
| **1** | About the American Community Survey | `https://www.census.gov/programs-surveys/acs/about.html` | Official U.S. Census Bureau documentation defining ACS scope, data items collected, and survey purposes. |
| **2** | About County Business Patterns (CBP) | `https://www.census.gov/programs-surveys/cbp/about.html` | Official U.S. Census Bureau technical overview defining employer establishments, Business Register sources, and scope. |
| **3** | CPI: Pet Food and Treats (CUSR0000SS61031) | `https://fred.stlouisfed.org/series/CUSR0000SS61031` | Official Bureau of Labor Statistics price index series published by Federal Reserve Bank of St. Louis. |
| **4** | Clean Town Data | `sample-data/orange_towns_clean.csv` | Frozen project dataset containing verified 2019–2023 ACS 5-year town-level estimates and margins of error for Orange County, NY. |

---

## 4. How to Run the Skill (Step-by-Step)

### Step 1: Create the Standardized Notebook
Follow the naming standard `<Case> - <Town A> vs <Town B>`:
```bash
nlm notebook create "Pet-care - Warwick town vs Monroe town"
```
Copy the returned `notebook_id` and set a project alias:
```bash
nlm alias set petcare <notebook-id>
```

### Step 2: Ingest the Sources
Add the 4 vetted sources and wait for cloud processing:
```bash
nlm source add petcare --url "https://www.census.gov/programs-surveys/acs/about.html" --wait
nlm source add petcare --url "https://www.census.gov/programs-surveys/cbp/about.html" --wait
nlm source add petcare --url "https://fred.stlouisfed.org/series/CUSR0000SS61031" --wait
nlm source add petcare --file "sample-data/orange_towns_clean.csv" --wait
```
Verify all 4 sources are attached with status `ready` (`2`):
```bash
nlm source list petcare
```

### Step 3: Run the 5 Grounded Queries
Execute the five standardized research questions:

1. **CBP Employer Scope**:
   ```bash
   nlm notebook query petcare "Does County Business Patterns (CBP) count non-employer pet care providers such as solo dog walkers and informal pet sitters, or only employer establishments?"
   ```
2. **FRED Price Index Units**:
   ```bash
   nlm notebook query petcare "Is FRED series CUSR0000SS61031 measured in dollar amounts or is it a price index? Can it tell us the local price of grooming or daycare in Warwick or Monroe?"
   ```
3. **Census Pet Ownership Coverage**:
   ```bash
   nlm notebook query petcare "Does the Census American Community Survey (ACS) collect data on pet ownership, dog counts, or household pet care spending?"
   ```
4. **Town Income & MOE Overlap**:
   ```bash
   nlm notebook query petcare "Comparing Warwick town and Monroe town in orange_towns_clean.csv, what are their median household incomes and margins of error? Do their 90% confidence margins of error overlap?"
   ```
5. **NAICS 6-Digit Code Definitions**:
   ```bash
   nlm notebook query petcare "What is the difference in scope between NAICS 812910 (Pet Care Services) and NAICS 541940 (Veterinary Services)?"
   ```

---

## 5. Human Audit & Logging Protocol

After running each query:
1. **Open and Inspect Citations**: Review the citation text returned in the references block against the raw source.
2. **Audit Confirmation Status**:
   - If the cited passage directly supports the claim, mark it **Confirmed**.
   - If the cited passage does not contain the specific fact or definition (e.g. Q5, where the general CBP About page does not define 6-digit NAICS operational boundaries), mark it **Not confirmed**.
3. **Update Deliverable Artifacts**:
   - Log the commands, answers, quoted passages, and statuses in [`evidence/notebooklm-transcript.md`](../../evidence/notebooklm-transcript.md).
   - Enter each factual claim into [`evidence/claim-ledger.csv`](../../evidence/claim-ledger.csv).
   - Complete Section 5 of [`completed-workbook.md`](../../completed-workbook.md).
