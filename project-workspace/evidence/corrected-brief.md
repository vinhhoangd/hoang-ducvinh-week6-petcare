# Corrected Research Brief: Pet-care Business (Warwick town vs Monroe town)

*Corrected and human-verified by Yuhe Luo (Research Owner, Team 3). Replaces the unverified seeded brief `seeded-ai-briefs/case4-pet-care-ai-brief.md`. All claims re-traced to raw data files and audited in `evidence/claim-ledger.csv`.*

---

## 1. Decision Frame and Purpose
The client is deciding whether to open a dog daycare with grooming in **Warwick town** or **Monroe town** (Orange County, NY), and whether to proceed immediately or pilot first. This brief evaluates what public data (ACS 5-year 2019–2023, CBP 2022, FRED) can and cannot substantiate.

---

## 2. Corrected Findings and Audit of Seeded Claims

* **C1 (Corrected — Pet Ownership Count: `unknown` / Refuted):**  
  *Original claim:* "ACS shows Warwick town has roughly 4,491 pet-owning households."  
  *Audit & Correction:* **Refuted.** The U.S. Census American Community Survey collects demographic, housing, and income data, but does **not** survey pet ownership, pet counts, or household pet expenditures. The figure 4,491 was an AI hallucination. Under our decision rule, pet-owning household counts are labeled **unknown** and cannot be obtained from public census files (`evidence/claim-ledger.csv`, row C1 / L3).

* **C2 (Corrected — Industry Competitor Count: Refuted):**  
  *Original claim:* "Orange County has 40 veterinary establishments, so mobile groomers face 40 direct competitors."  
  *Audit & Correction:* **Refuted.** According to County Business Patterns 2022 (`sample-data/raw/cbp_541940.json`), the 40 establishments in Orange County are **veterinary services** (NAICS 541940), which provide clinical medical treatments rather than primary pet daycare or mobile grooming. Commercial pet care establishments (except veterinary, NAICS 812910) number **24** establishments across Orange County (`sample-data/raw/cbp_812910.json`). Furthermore, CBP reports county-level aggregates and excludes solo/non-employer groomers, so local town-level competition remains unmeasured (`evidence/claim-ledger.csv`, rows C2, L1, L5).

* **C3 (Corrected — Spending Trends: `unknown` / Unsupported):**  
  *Original claim:* "U.S. pet spending is rising, so Monroe town residents are spending more on pet care."  
  *Audit & Correction:* **Unsupported.** Attributing nationwide macro pet-industry expenditure expansion directly to Monroe town households commits an ecological fallacy. No public municipal dataset tracks local pet care discretionary spending (`evidence/claim-ledger.csv`, row C3).

* **C4 (Corrected — Housing Tenure: Proxy):**  
  *Original claim:* "19.38% of Warwick town households are renters (apartment residents), so they are more likely to buy grooming."  
  *Audit & Correction:* **Proxy.** ACS 2019–2023 (`sample-data/orange_towns_clean.csv`) confirms that renter-occupied housing units account for **19.38%** (2,276 of 11,743 occupied units, `data/raw/acs5_towns.json` B25003_003E / B25003_001E) in Warwick town and **19.01%** in Monroe town. However, concluding that renters are "more likely to buy grooming" is an unverified behavioral assumption; renters frequently face property pet restrictions and may spend less on luxury pet care (`evidence/claim-ledger.csv`, row C4).

* **C5 (Corrected — Inflation Benchmark: Proxy):**  
  *Original claim:* "The pet food and treats CPI moved from 191.485 to 194.485 (1.57%) over twelve months."  
  *Audit & Correction:* **Proxy.** In the FRED series `CUSR0000SS61031` (`sample-data/raw/fred_CUSR0000SS61031.csv`), the index rose from 191.485 (Aug 2025) to 194.485 (Aug 2026), representing a 1.57% increase. However, this is a **national commodity index for retail pet food and treats**, not a measure of local service labor rates, grooming fees, or commercial kennel rents in Orange County (`evidence/claim-ledger.csv`, rows C5, L2).

* **C6 (Corrected — Median Household Income: Supported Numbers, Overlapping MOE):**  
  *Original claim:* "Monroe town median household income is $116,019 ± $13,663 and Warwick town is $117,680 ± $8,605."  
  *Audit & Correction:* **Supported numbers, but statistical rank is indistinguishable.** The 90% confidence intervals are **$109,075 to $126,285** for Warwick town and **$102,356 to $129,682** for Monroe town (`sample-data/moe_pair.csv`). Because the margin-of-error ranges overlap by $17,210, the Census survey cannot statistically rank one town above the other on household wealth (`evidence/claim-ledger.csv`, rows C6, L4).

---

## 3. Comparison Summary: Warwick town vs. Monroe town

| Measure | Warwick town | Monroe town | Data Interpretation & Caveat |
|---|---|---|---|
| **Total Population (`pop`)** | 31,909 | 21,299 | Warwick has a larger base pool (+10,610 residents), but total population does not count dog owners. |
| **Median Household Income** | $117,680 ± $8,605 | $116,019 ± $13,663 | Statistically indistinguishable; MOE confidence intervals overlap substantially. |
| **Renter Share (`pct_renter`)** | 19.38% | 19.01% | Nearly identical housing tenure; proxy for apartment density. |
| **Youth Population (`under18`)** | 6,273 | 5,787 | Rough proxy for families with pets; does not count pets. |
| **Employer Pet Care (CBP 812910)** | 24 countywide | 24 countywide | Covers Orange County overall; cannot differentiate town-level competitors. |
| **Pet Ownership & Spending** | **Unknown** | **Unknown** | Zero public sources measure local pet counts or expenditures. |

---

## 4. Evidence-Grounded Recommendation

* **Recommendation:** **Pilot first; do not open immediately in either town based on public data alone.**  
* **Why the Seeded Brief Failed:** The original AI brief declared: *"Open in Monroe town. The data clearly supports this choice."* This recommendation was completely ungrounded. It relied on hallucinated pet numbers (C1), confused veterinarians with grooming competitors (C2), generalized national inflation to local services (C3, C5), and ignored that median incomes overlap within survey margins of error (C6).
* **Primary-Research Pilot Plan (4-Week Validation):**  
  Because public data leaves local pet ownership, pet density, and demand elasticity **unknown**, the client should run a low-cost, 4-week field validation pilot before signing a commercial lease:
  1. **Town Clerk Pet License Records:** Obtain municipal dog registration filings from both Warwick and Monroe town halls to measure baseline licensed pet density.
  2. **Field Intercepts & Dog Park Audits:** Conduct weekend in-person surveys at local parks (e.g., Warwick Dog Park, Monroe ponds/trails) counting active dogs and surveying owners on current daycare/grooming pain points.
  3. **Competitor Secret-Shopping:** Audit all local commercial boarding facilities and mobile groomers serving Warwick and Monroe for waitlist lengths, service pricing, and capacity constraints.
