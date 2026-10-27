# Failure and Recovery Log (Step 7)

For each failure: write the prediction FIRST, then run, then record. Keep the broken evidence; do not overwrite it.

| # | Failure | My prediction (written before the test) | Evidence preserved (file, output, or screenshot name) | Observed | Diagnosis | Smallest repair | Repeat test and result |
|---|---|---|---|---|---|---|---|
| F1 | Seeded AI brief | Claims I expect to fail: | `evidence/claim-ledger.csv` rows | | | Corrected brief file: | Every corrected claim re-traces to raw data? |
| F2a | `broken-requests` A (county 71) | Rows expected (Vinh, 2026-10-27 14:52): **0** — `71` is not a valid three-digit county code | `data/raw/broken/A-county-71.response.txt` (0 bytes); `api-manifest.md` F2 table | **HTTP 204, 0 rows** — matches the prediction | Logic of the request: the county parameter must be the three-digit FIPS string `071`; `71` matches no county | Changed `county:71` → `county:071` | **92 rows**, HTTP 200 (`A-county-71-fixed.response.txt`) |
| F2b | `broken-requests` B (county 017) | Rows expected (Vinh, 2026-10-27 14:52): the **wrong county's** tracts, not Orange's 92 — 017 is a different county | `data/raw/broken/B-wrong-county-017.response.txt` (1,333 bytes, same as the course fixture) | **HTTP 200, 16 rows — all "Chenango County, New York"** — matches the prediction; a 200 status looked like success | Wrong geography: 017 is Chenango County; Orange County is 071 | Changed `county:017` → `county:071` | **92 rows**, all Orange County (`B-wrong-county-017-fixed.response.txt`) |
| F2c | `broken-requests` C (year 2009) | Rows expected (Vinh, 2026-10-27 14:52): **fewer than 92** — the 2009 survey used older tract boundaries | `data/raw/broken/C-old-vintage-2009.response.txt` (5,076 bytes, same as the course fixture) | **HTTP 200, 67 rows** — matches the prediction; again a 200 that is wrong | Wrong vintage: ACS 2009 uses the 2000-census tracts (67 in Orange County); the project uses ACS 2023 | Changed `/data/2009/` → `/data/2023/` | **92 rows** (`C-old-vintage-2009-fixed.response.txt`) |
| F3 | Leakage table | Held-out R2 predicted: | | | Which column leaks: | Column removed: | Held-out R2 after: |
| F4 | MOE pair | Town I expect to rank first: | `sample-data/moe_pair.csv` | Ranges overlap? | | Claim downgraded to: | |
