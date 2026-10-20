# Model-Risk Note (ADI501, Step 11)

Write for a manager who will not read the code. Each risk needs a number you measured and a guardrail rule.

| Risk | How it could mislead the manager | My measured evidence | Numeric guardrail |
|---|---|---|---|
| Small n | A town result built on very few tracts | Tracts per town: | Do not report a town result with fewer than ___ tracts |
| Leakage | A feature that contains the answer inflates the score | F3 R2 with and without the leak: | Reject any held-out R2 above ___ without a leakage review |
| Correlated features | Importance split or inflated among features that move together | Correlation between your top two features: | Report importance only as a group when correlation exceeds ___ |
| Overfitting | A tree that memorizes | Train versus held-out gap: | Reject a model when the gap exceeds ___ |

Decision this note changes (one sentence):
