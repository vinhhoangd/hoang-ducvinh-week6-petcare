# Model Card (Step 6)

A model card is a one-page honest description of a model: what it predicts, what it was trained on, how well it did on data it had not seen, and where it should not be trusted. Fill every section. Numbers must come from your own run; paste the command or notebook cell that produced each one into the "Where I got it" column.

## 1. What the model predicts

- Target (the thing predicted): *Tract median household income (`median_income`) unless your instructor says otherwise.*
- Rows: 92 Orange County NY tracts in the input; 91 used after dropping the one tract with missing `median_income`.
- Features used (list the column names): `pop`, `median_age`, `pct_under18`, `pct_renter`, `pct_commute_30plus`, `pct_built_pre1970`, `pct_bachelors_plus`.
- Features deliberately left out: `geoid` is an identifier and `town` is a label, not a numeric predictor; `median_income_moe` describes uncertainty in the target and could leak target-related information; `median_rent` and `median_rent_moe` contain missing values, so they were excluded rather than imputed. The seven selected features have no missing values among the 91 rows used.
- Training/held-out split: 75%/25%, 68 training tracts and 23 held-out tracts, `random_state=42`.

## 2. Results table

| Model | Train R2 | Held-out R2 | Held-out average error in dollars (MAE) | Where I got it |
|---|---|---|---|---|
| Decision tree, no depth limit | 1.000 | 0.260 | $18,041 | `cd project-workspace && .venv/bin/python model/fit_models.py` |
| Decision tree, depth limited to 3 | 0.866 | 0.172 | $20,463 | `cd project-workspace && .venv/bin/python model/fit_models.py` |
| Random forest (500 trees) | 0.954 | 0.552 | $16,581 | `cd project-workspace && .venv/bin/python model/fit_models.py` |

*R2 near 1.0 means the model reproduces the answer; near 0 means it is no better than guessing the average. A huge gap between Train R2 and Held-out R2 means the model memorized.*

## 3. Required study: how does a tree work and why is a forest steadier?

1. How does a decision tree decide where to split? A regression tree tests feature-and-threshold splits and chooses one that reduces squared prediction error within the resulting groups; it repeats this process, and each leaf predicts its training targets' average.
2. How is a random forest different from one tree? It fits many trees using randomized bootstrap samples and feature choices, then averages their predictions.
3. Why is a forest usually more stable than one tree? Averaging trees that make different errors reduces variance, so the prediction is less dependent on one tree's particular splits.

A decision tree splits the tracts into smaller groups by choosing a feature and cutoff that reduce prediction errors. Each final group predicts income using the average income of the tracts in that group. A random forest builds many trees using different samples and feature choices, then averages their predictions. Because the trees may make different mistakes, averaging can make the forest less sensitive to one tree’s splits. In this run, the forest had a smaller train-to-test R² gap and a higher held-out R² than the unpruned tree, although the test set was small.


Now check the claim on your data. Fill this in using your table above:

> Using train R2 minus held-out R2, the unpruned tree's gap was 0.740 and the forest's gap was 0.402. This matches the idea that the forest is steadier on this split: its gap was smaller and its held-out R2 (0.552) was higher than the unpruned tree's (0.260). This is one small held-out sample, not proof the forest will always perform better.

## 4. Feature importance

*List the top three features for the forest and what each one could mean for the client. Importance is not cause: a feature can rank high because it moves with income, not because it creates it.*

| Rank | Feature | Importance | What it could mean | What it does NOT prove |
|---|---|---|---|---|
| 1 | `pct_renter` | 0.445 | Tracts with different renter shares may also differ in household income and housing context. | Renting causes income differences, or renters own more or fewer pets. |
| 2 | `pct_bachelors_plus` | 0.239 | Educational attainment may be associated with the income patterns captured by this model. | Education causes income or predicts an individual's income or pet-care spending. |
| 3 | `pct_commute_30plus` | 0.122 | Long commutes may co-vary with tract income or work patterns. | Commuters need dog daycare, own pets, or will buy this service. |

## 5. Your town versus the rest of the county

*Use out-of-sample residuals (actual minus predicted, with each tract predicted by a model that did not train on it). A town whose tracts are consistently above the prediction earns more than its features would suggest.*

| Town | Number of tracts | Mean actual income | Mean residual | Reading |
|---|---|---|---|---|
| Warwick town | 8 | $118,956 | +$738 | Its tract mean is close to the out-of-fold predictions on average; this is not evidence of local pet-care demand. |
| Monroe town | 5 | $104,575 | -$9,179 | Its tracts averaged below their out-of-fold predictions; the small count makes this estimate uncertain. |

Why a town with 3 to 8 tracts is a weak sample, in one sentence:

> A few tracts provide little information about variation within a town, so one unusual tract can move the town average and residual substantially.

Residual method: each tract was predicted by a 500-tree random forest in shuffled five-fold cross-validation (`random_state=42`); its own target was excluded from the fold used to fit its predictor. Residual is actual minus out-of-fold predicted income.

## 6. Leakage check (Failure F3)

- Prediction BEFORE running `sample-data/leakage_starter_table.csv`: held-out R2 will be ______.
- Observed held-out R2 with the leaking column:
- Which column leaks, and how do you know?
- Held-out R2 after removing it:
- Why a score that high should have made you suspicious:

## 7. Limits (required)

- Sample size: 91 tracts with a reported target (92 input rows; one target missing), with only 23 in the held-out test set. Warwick has 8 modeled tracts and Monroe has 5.
- Time period of the data: 2023 ACS 5-year estimates; these summarize a multi-year survey period and are not a real-time measure.
- Variables not in the model that matter: pet ownership, local willingness to pay, customer demand, pet-friendly rental rules, competitor capacity/pricing, and business operating costs.
- One decision the model should NOT be used for: it should not decide by itself whether to invest in or open a pet-care business in either town.
