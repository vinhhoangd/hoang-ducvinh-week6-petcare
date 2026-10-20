# Failure and Recovery Log (Step 7)

For each failure: write the prediction FIRST, then run, then record. Keep the broken evidence; do not overwrite it.

| # | Failure | My prediction (written before the test) | Evidence preserved (file, output, or screenshot name) | Observed | Diagnosis | Smallest repair | Repeat test and result |
|---|---|---|---|---|---|---|---|
| F1 | Seeded AI brief | Claims I expect to fail: | `evidence/claim-ledger.csv` rows | | | Corrected brief file: | Every corrected claim re-traces to raw data? |
| F2a | `broken-requests` A (county 71) | Rows expected: | | | | | Rows after fix (must be 92): |
| F2b | `broken-requests` B (county 017) | Rows expected: | | | | | |
| F2c | `broken-requests` C (year 2009) | Rows expected: | | | | | |
| F3 | Leakage table | Held-out R2 predicted: | | | Which column leaks: | Column removed: | Held-out R2 after: |
| F4 | MOE pair | Town I expect to rank first: | `sample-data/moe_pair.csv` | Ranges overlap? | | Claim downgraded to: | |

## Example row (delete this section before submitting)

F2a, example wording: "Predicted 92 rows; got HTTP 204 and zero rows. Diagnosis: county code `71` must be the three-digit string `071`. Repair: changed the parameter and reran; 92 rows, matches the manifest."
