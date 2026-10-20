# Model Card (Step 6)

A model card is a one-page honest description of a model: what it predicts, what it was trained on, how well it did on data it had not seen, and where it should not be trusted. Fill every section. Numbers must come from your own run; paste the command or notebook cell that produced each one into the "Where I got it" column.

## 1. What the model predicts

- Target (the thing predicted): *Tract median household income (`median_income`) unless your instructor says otherwise.*
- Rows: all Orange County NY tracts with a non-missing target. Number of rows used:
- Features used (list the column names):
- Features you deliberately left out, and why (at least one):
- Training/held-out split (what fraction, what random seed):

## 2. Results table

| Model | Train R2 | Held-out R2 | Held-out average error in dollars (MAE) | Where I got it |
|---|---|---|---|---|
| Example only (delete): decision tree, no depth limit | 1.00 | 0.1 | 25,000 | cell 7 |
| Decision tree, no depth limit | | | | |
| Decision tree, depth limited to 3 | | | | |
| Random forest | | | | |

*R2 near 1.0 means the model reproduces the answer; near 0 means it is no better than guessing the average. A huge gap between Train R2 and Held-out R2 means the model memorized.*

## 3. Required study: how does a tree work and why is a forest steadier?

Before you read the results, ask your agent three questions and paste the answers you decided to keep (shortened to your own words):

1. How does a decision tree decide where to split?
2. How is a random forest different from one tree?
3. Why is a forest usually more stable than one tree?

> Your summary in your own words (3 to 5 sentences):

Now check the claim on your data. Fill this in using your table above:

> The tree's gap between train and held-out R2 was ______. The forest's gap was ______. This (does / does not) match the idea that a forest is steadier, because ______.

## 4. Feature importance

*List the top three features for the forest and what each one could mean for the client. Importance is not cause: a feature can rank high because it moves with income, not because it creates it.*

| Rank | Feature | Importance | What it could mean | What it does NOT prove |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## 5. Your town versus the rest of the county

*Use out-of-sample residuals (actual minus predicted, with each tract predicted by a model that did not train on it). A town whose tracts are consistently above the prediction earns more than its features would suggest.*

| Town | Number of tracts | Mean actual income | Mean residual | Reading |
|---|---|---|---|---|
| | | | | |
| | | | | |

Why a town with 3 to 8 tracts is a weak sample, in one sentence:

> 

## 6. Leakage check (Failure F3)

- Prediction BEFORE running `sample-data/leakage_starter_table.csv`: held-out R2 will be ______.
- Observed held-out R2 with the leaking column:
- Which column leaks, and how do you know?
- Held-out R2 after removing it:
- Why a score that high should have made you suspicious:

## 7. Limits (required)

- Sample size:
- Time period of the data:
- Variables not in the model that matter:
- One decision the model should NOT be used for:
