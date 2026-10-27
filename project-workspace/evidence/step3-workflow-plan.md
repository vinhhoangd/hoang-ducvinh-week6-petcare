# Step 3 Plan: Human–AI Workflow Specification (Case 4: Pet-Care)

> **Execution Mode:** Planning Only (No code generated or executed)  
> **Target Case:** Case 4 — Pet-Care Business (Warwick Town vs. Monroe Town, Orange County, NY)  
> **Team Members:** Vinh Hoang (Data Owner), Yuhe Luo (Research Owner), Shiming (Model Owner)  

---

## 1. Governance & Security Guardrails

This plan conforms to the following mandatory safety and evaluation standards:

1. **Zero Credential Exposure:**
   - The Census API key must be retrieved solely at runtime via `os.environ.get("CENSUS_API")`.
   - Never paste, prompt for, hardcode, or echo API keys or authentication tokens into chat, code, command arguments, or repo files.
   - Any API request logged into `api-manifest.md` or logs must substitute the real key with `<KEY>`.
   - An intentional credential refusal test will be executed and recorded in `ai-use-log.md`.

2. **Command & File Transparency:**
   - Every file creation, modification, or external query must have a declared target, explicit purpose, identified failure risks, and a verified recovery/rollback procedure.
   - No destructive commands (unjustified deletion, overwriting existing datasets without consent, or global installs).

3. **Generalization & Methodological Rigor:**
   - Predictive modeling must enforce an explicit 80/20 train/held-out test split using a fixed random seed prior to any model training.
   - Models must be benchmarked on both Training and Held-Out Test sets using $R^2$ and Mean Absolute Error (MAE in dollars).
   - Public data limitation: Acknowledge upfront that public data cannot directly measure pet ownership counts; claims asserting pet counts are treated as `unknown` unless verified by primary field research.

---

## 2. Work Breakdown

### Part A: Data Ingestion Pipeline (`scripts/pull_data.py`)

* **Primary Owner:** Vinh Hoang  
* **File Target:** `scripts/pull_data.py`  
* **Output Destinations:** `data/raw/`, `data/clean/`, `api-manifest.md`, `data/variable-dictionary.md`

#### Detailed Procedure:
1. **Runtime Credential Validation:**
   - Check `os.getenv("CENSUS_API")`. If not found or empty, stop immediately with: `"Error: CENSUS_API environment variable not set. Please set it before running."`
2. **ACS 5-Year (2023) Census Tracts:**
   - Endpoint: `https://api.census.gov/data/2023/acs/acs5`
   - Geography: State `36` (NY), County `071` (Orange County), `tract:*`
   - Variables: Median household income (`B19013_001E`), Margin of Error (`B19013_001M`), Total population (`B01003_001E`), Housing tenure (renter/owner: `B25003_003E`, `B25003_002E`), Commute duration (`B08303_001E`, `B08303_013E`), and respective MOEs.
   - Verification standard: Must return exactly **92 census tract rows** matching `sample-data/orange_tracts_clean.csv`.
3. **ACS 5-Year (2023) County Subdivisions (Towns):**
   - Query Warwick town (`cousub:78243`) and Monroe town (`cousub:47933`) for identical measures to allow direct statistical comparison and MOE overlap checks.
4. **County Business Patterns (CBP 2022):**
   - Query NAICS `812910` (Pet care except veterinary) and `541940` (Veterinary services) for Orange County (`county:071`).
5. **FRED Macroeconomic Index:**
   - Retrieve `CUSR0000SS61031` (Consumer Price Index: Pets, pet products and services) directly from St. Louis Fed.
6. **Persistence & Manifest Audit:**
   - Save untouched API responses in `data/raw/`.
   - Save standardized tabular outputs in `data/clean/`.
   - Write `api-manifest.md` recording endpoint URL (key sanitized as `<KEY>`), HTTP status code (must be 200), row count, and retrieval timestamp.
   - Build `data/variable-dictionary.md` defining code, human-readable name, unit, and whether MOE is reported.

---

### Part B: Source-Grounded Research Skill (`skills/source-grounded-research/SKILL.md`)

* **Primary Owner:** Yuhe Luo  
* **File Target:** `skills/source-grounded-research/SKILL.md`  
* **Output Destinations:** `evidence/notebooklm-transcript.md`, `evidence/claim-ledger.csv`

#### Detailed Procedure:
1. **Tooling & Setup:**
   - Verify `nlm` CLI is installed and user logged in manually in terminal (`nlm --version`).
   - Create notebook: `Pet-care - Warwick town vs Monroe town`.
2. **Primary Source Ingestion (Zero Unvetted Sources):**
   - **Source 1:** Official Census Bureau ACS 5-Year technical documentation.
   - **Source 2:** US Census CBP methodology / "About" page (defining employer vs. non-employer establishments).
   - **Source 3:** Federal Reserve Bank of St. Louis FRED series documentation for `CUSR0000SS61031` (explaining price indices).
   - **Source 4:** Local frozen data `sample-data/orange_towns_clean.csv`.
3. **Structured Question Execution (`nlm notebook query`):**
   - Q1: *Does NAICS 812910 count non-employer pet care providers (e.g., solo dog walkers, app-based pet sitters), and how are establishments defined?*
   - Q2: *Is FRED series CUSR0000SS61031 measured in nominal dollars, or is it a price index relative to a base period?*
   - Q3: *Can Census ACS tract or town data report the actual number or percentage of pet-owning households?*
   - Q4: *Between Warwick town and Monroe town, which has a higher median household income, and do their 90% confidence margins of error overlap?*
   - Q5: *What are the specific services included under NAICS 812910 versus NAICS 541940?*
4. **Human Verification & Ledgering:**
   - Review each response against cited source passages; record verbatim citations and mark as `confirmed` or `not confirmed` in `evidence/notebooklm-transcript.md`.
   - Transfer verified statements into `evidence/claim-ledger.csv`. Pet-count claims are coded as `unknown` / `unsupported`.

---

### Part C: Tree and Random Forest Regressors (`model/fit_models.py`)

* **Primary Owner:** Shiming  
* **File Target:** `model/fit_models.py`  
* **Output Destination:** `evidence/model-card.md`, `completed-workbook.md` Section 6

#### Detailed Procedure:
1. **Data Preprocessing & Target Definition:**
   - Target variable ($y$): Median household income (`median_household_income`) across the 92 tracts.
   - Features ($X$): Population, housing tenure shares, commute time distributions. Direct proxies of income (e.g. poverty rate, aggregate income) are excluded to prevent target leakage.
2. **Train/Held-Out Test Partitioning:**
   - Split 92 tracts into an 80% training set (approx. 73 tracts) and 20% held-out test set (approx. 19 tracts) using `train_test_split(..., test_size=0.20, random_state=42)`.
   - Preprocessing transformers fit strictly on the training set.
3. **Model Specifications:**
   - **Model 1: Unpruned Decision Tree** (`DecisionTreeRegressor(random_state=42)`): Serves as baseline illustrating unconstrained memorization (Train $R^2 \approx 1.0$, Test $R^2 \approx 0.0$ or negative).
   - **Model 2: Depth-3 Decision Tree** (`DecisionTreeRegressor(max_depth=3, random_state=42)`): Demonstrates rule-based pruning to mitigate overfitting.
   - **Model 3: Random Forest Regressor** (`RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)`): Ensemble variance reduction.
4. **Performance Metrics:**
   - Calculate and display:
     - Training $R^2$ and Held-Out Test $R^2$.
     - Held-Out Test Mean Absolute Error (MAE in dollars: $\text{MAE} = \frac{1}{n} \sum |y - \hat{y}|$).
5. **Interpretability & Residual Diagnostics:**
   - Extract Random Forest top-3 feature importances; document that feature importance indicates associative split utility, not causal business drivers.
   - Compute out-of-sample prediction residuals for tracts located in Warwick and Monroe. Document why 3–8 tracts per town provide insufficient sample size for town-specific standalone models.
   - Record findings in `evidence/model-card.md`.

---

## 3. Decision Checkpoint Table for `ai-use-log.md`

| Command or Action | Target File / Environment | Stated Purpose | Risk Assessment | Rollback / Recovery | Recommendation |
|---|---|---|---|---|---|
| Create `scripts/pull_data.py` | `scripts/pull_data.py` | Implement automated API data retrieval for ACS, CBP, and FRED | Low: isolated script creation | Delete or revert script | **Accept** |
| Execute `pull_data.py` | `data/raw/`, `data/clean/`, `api-manifest.md` | Ingest and clean 92 census tracts and town datasets | Low: writes local data tables; reads env var | Delete generated files and re-run | **Accept** |
| Create `skills/source-grounded-research/SKILL.md` | `skills/source-grounded-research/SKILL.md` | Standardize NotebookLM query and citation workflow | Low: text markdown documentation | Delete or edit file | **Accept** |
| Run `nlm notebook query` commands | NotebookLM CLI session | Retrieve primary-source grounded answers for 5 key questions | Low: read-only API calls against uploaded sources | Discard query results / rerun query | **Accept** |
| Create `model/fit_models.py` | `model/fit_models.py` | Train and evaluate unpruned tree, depth-3 tree, and random forest | Low: isolated script creation | Delete or revert script | **Accept** |
| Execute `fit_models.py` | Terminal / `model-card.md` | Generate train/test $R^2$, MAE, feature importances, and town residuals | Low: computational run on clean dataset | Re-run script with adjusted parameters | **Accept** |

---

## 4. Verification Check against Step 3 Checklist & Workbook

- [x] **Credential handling in prompt:** Verified. Key loaded solely from `CENSUS_API` environment variable.
- [x] **No unjustified delete/overwrite/install:** Verified. All targets, purposes, risks, and recovery paths explicitly documented.
- [x] **Held-out test set specified:** Verified. 80/20 train/test split with seed 42 defined for all model benchmarks.
- [x] **Workbook Section 3 mapping:** Complete coverage for items 3.1 (plan description), 3.2 (revisions/checks), and 3.3 (held-out validation).
