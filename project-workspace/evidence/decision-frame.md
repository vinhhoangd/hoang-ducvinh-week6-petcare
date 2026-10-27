# Decision Frame (Step 1 and Step 2)

Fill this in **before** you ask any AI agent to do analysis. Write in your own words. Keep every answer short and specific. Replace every line that begins with `>` with your answer, and delete the guidance text in italics when you are done.

## Team and case

- Team members: Team 3 — Vinh Hoang, Yuhe Luo, Shiming Wan
- Case claimed (1 cafe, 2 childcare, 3 contractor, 4 pet-care, 5 tutoring): 4, pet-care
- Date and time the case was claimed on Canvas: Oct 20, 2026, 2:48 PM (Yuhe Luo's reply in "Week 6 team discussion")
- Two towns you compare (copy from the case table in START-HERE): Warwick town vs Monroe town (CBP 812910, with 541940 as a contrast; FRED CUSR0000SS61031)

## The one decision the client must make

*One sentence. It must end in one of four actions: proceed, pilot, investigate further, or do not proceed.*

> The client must decide whether to open a Pet Care Center in Warwick town or Monroe town, or to pilot a weekend pop-up in each town before signing a lease.

## Success criteria (write these BEFORE using AI)

*A claim in your brief counts as supported only if it passes every test below. Edit the list if you can justify a stricter rule, but you may not remove a test.*

1. Every number in the brief appears in the claim ledger with a source field and a calculation.
2. Every cited source was opened by a human on the team, and the quoted passage says what the claim says.
3. Geography is correct: state, county, and town or tract named in the claim match the data row used.
4. Two ACS estimates are called different only if their margin-of-error ranges do not overlap.
5. A proxy is labeled as a proxy. If the public data cannot answer the question, the brief says "unknown" and proposes primary research.

> Your added rule (optional, with a one-sentence reason):

## Measures you will use

*Pick 4 to 6 ACS measures from `sample-data/orange_tracts_clean.csv` or `orange_towns_clean.csv`, one CBP industry file from `sample-data/raw/`, and one FRED series from `sample-data/raw/`. For each, say what business question it helps answer and what it cannot tell the client.*

| Measure (column or file) | Business question it helps with | What it cannot tell the client |
|---|---|---|
| `pop` (from `orange_towns_clean.csv`) | What is the total potential customer base size in each town? | Does not tell us how many households actually own pets, average household size, or demand for professional pet care. |
| `median_income` & `median_income_moe` (from `orange_towns_clean.csv`) | Do residents have sufficient discretionary income to afford premium pet care and grooming? | Because the MOE intervals overlap ($116,019 ± $13,663 vs $117,680 ± $8,605), the data cannot prove one town is wealthier. Income also does not measure willingness to spend on pets. |
| `pct_renter` (from `orange_towns_clean.csv`) | What proportion of residents rent vs own their homes? | Does not tell us building pet policies (e.g. pet bans/deposits), pet ownership rates among renters vs owners, or preference for mobile grooming vs salon services. |
| `under18` (from `orange_towns_clean.csv`) | Are there family households present (which frequently keep companion animals)? | Children are only a rough proxy; this cannot count actual dogs or cats, nor indicate household pet expenditure. |
| `sample-data/raw/cbp_812910.json` (NAICS 812910) | How many commercial pet care (grooming/boarding) establishments currently operate in Orange County? | County-level aggregate only (does not break down competitors in Warwick vs Monroe), and does not measure market saturation or unmet customer demand. |
| `sample-data/raw/fred_CUSR0000SS61031.csv` (CPI: Pet Food and Treats) | What is the broader macroeconomic cost trend / inflation rate facing pet owners? | It is a national index for retail pet food/treats; it does not measure local Orange County service labor costs, grooming pricing, or local demand elasticity. |

## Prediction before you look (write this now, check it in Step 7)

> I expect the town with the higher total population (`pop`, Warwick town at 31,909 vs Monroe town at 21,299) to look better for this decision because a larger overall resident base provides a larger pool of potential pet-owning households to support ongoing grooming and boarding demand.
> I am 65 percent confident, and the number that would change my mind is if Monroe's median household income were proven statistically significantly higher without margin-of-error overlap, or if primary research reveals a significantly higher pet density in Monroe.

## Claim-ledger rules (read, then follow in `claim-ledger.csv`)

- One row per claim. A claim is any sentence in your brief that contains a number or a comparison.
- `evidence_type`: `measured` (an API value you can point to), `proxy` (stands in for the thing the client really cares about), `assumption` (you chose it), or `unknown` (no public data can answer).
- `status`: `supported`, `proxy`, `unsupported`, or `refuted`.
- Do not delete refuted rows. A refuted row is evidence that your verification worked.
