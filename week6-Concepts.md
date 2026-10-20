# Week 6 Concepts — Source-Grounded Market Intelligence

Read this before Step 0 if any term is new. Each entry says what the term is, why it matters this week, how it shows up in your work, and gives an AI prompt for going further. Back to the main instructions: `START-HERE.html`.

## API

**What it is:** A web address that answers a request with data instead of a web page. Your script sends a request ("tract incomes for Orange County, NY") and gets rows back.

**Why it matters:** An API call can be repeated tomorrow and give the same answer. A number someone typed from a website cannot be checked the same way.

**How it appears in your work:** Step 4. Your script saves every raw response, so any number in your brief can be traced to a saved file.

**Ask your agent:** "Explain what a REST API request and response are using the Census API as the example, and show what a query string is."

## API key (a credential)

**What it is:** A code the data provider gives you so it knows who is asking. It works like a password.

**Why it matters:** Anyone with your key can use your account. Keys pasted into prompts, logs, repos, or screenshots leak.

**How it appears in your work:** The key lives only in an environment variable (loaded from a `.env` file that is never submitted). The manifest shows `<KEY>` where the key would be.

**Ask your agent:** "What is an environment variable, and why is it safer than putting a secret inside a script?"

## ACS and margin of error (MOE)

**What it is:** The American Community Survey asks a sample of households and publishes *estimates*. Each estimate has a margin of error: the true value is probably within estimate ± MOE.

**Why it matters:** If Town A's income is $117,680 ± $8,605 and Town B's is $116,019 ± $13,663, the ranges overlap, so you cannot say A is higher. Ranking noise is a classic mistake.

**How it appears in your work:** Failure F4 and Step 8. Compare ranges, not point numbers.

**Ask your agent:** "How do I decide whether two survey estimates with margins of error are really different?"

## CBP and "establishments"

**What it is:** County Business Patterns counts *employer establishments* (places with paid employees) by industry and county.

**Why it matters:** It does not count self-employed owners, and it is county-wide. "129 establishments in the county" does not mean "129 competitors within five miles."

**How it appears in your work:** The seeded brief makes this mistake on purpose.

**Ask your agent:** "What is the difference between an employer establishment and a nonemployer business in Census data?"

## FRED and index values

**What it is:** The Federal Reserve's data site. Many series are *indexes* (a price level set to 100 in a base period), not dollars. They are usually national.

**Why it matters:** An index rising from 384.9 to 397.9 is a 3.4 percent change, not "12.96 percent" (the point difference). A national price index is not your town's menu prices.

**How it appears in your work:** Step 8: compute percent change yourself from index levels.

**Ask your agent:** "How do I compute a percent change from two index values, and why is that different from the point change?"

## Census tract and pooling

**What it is:** A tract is a small area of roughly a few thousand people. Towns are built from tracts; Orange County has 92.

**Why it matters:** A single town has only 3 to 8 tracts, too few to train a model. We train on all 92 together (*pooling*), then see where each town sits relative to the county.

**How it appears in your work:** Step 6, town-versus-county table.

**Ask your agent:** "Why can a model trained on many small areas together be more reliable than one trained on a few?"

## Proxy

**What it is:** A measurable stand-in for what you really want to know. Median income is a proxy for spending power, not demand for coffee.

**Why it matters:** Labeling a proxy as a proxy is the difference between honest and misleading.

**How it appears in your work:** The `evidence_type` column of your claim ledger.

**Ask your agent:** "Give three examples of proxies used in business decisions and say what each can't tell you."

## Claim ledger

**What it is:** A table with one row per claim: the value, unit, geography, period, source field, calculation, citation, evidence type, and status.

**Why it matters:** It forces you to trace every number. A refuted row proves your verification worked.

**How it appears in your work:** `evidence/claim-ledger.csv`, used in Steps 5, 7, 8 and 10.

**Ask your agent:** "How do analysts keep an audit trail for the numbers in a report?"

## NotebookLM and source grounding

**What it is:** A tool that answers questions using only the sources you add and shows citations to passages in them.

**Why it matters:** A cited answer can still be wrong if the passage doesn't say what the answer claims, or if your sources are poor. You are responsible for opening the citation.

**How it appears in your work:** Step 5, with the `nlm` command-line tool.

**Ask your agent:** "What is the difference between a chatbot answering from its training and a tool answering only from supplied documents?"

## Skill (`SKILL.md`)

**What it is:** A short instruction file your agent reads so it follows the same procedure every time.

**Why it matters:** A skill makes a workflow repeatable and lets another person run it, which is the transfer trial.

**How it appears in your work:** Step 5 builds your research skill; the transfer trial tests it.

**Ask your agent:** "What should a good agent instruction file contain, and what should it forbid?"

## Decision tree, random forest, held-out data

**What it is:** A decision tree predicts a number by asking a chain of yes/no questions about the data ("is the renter share above 40 percent?"). A random forest builds many trees on varied samples and averages them. *Held-out data* is data the model never trained on, used for an honest score.

**Why it matters:** An unpruned tree can memorize the training data (score 1.0) and fail on new data. A forest is usually steadier because averaging cancels individual trees' flukes.

**How it appears in your work:** Step 6 and the model card.

**Ask your agent:** "Explain overfitting using a decision tree, and why averaging many trees helps."

## R² and feature importance

**What it is:** R² measures how much better the model is than guessing the average: 1.0 is perfect, 0 is no better, and it can be negative. Feature importance shows which inputs the model leaned on.

**Why it matters:** Importance describes the model, not the world. A feature can rank high because it moves with income without causing it.

**How it appears in your work:** The results and importance tables in your model card.

**Ask your agent:** "Explain R-squared in plain words and why feature importance does not prove causation."

## Leakage

**What it is:** A feature that secretly contains the answer (for example an income band computed from income).

**Why it matters:** Scores near perfect should make you suspicious, not proud.

**How it appears in your work:** Failure F3.

**Ask your agent:** "Give an example of data leakage in a business prediction model and how to detect it."

## Primary research

**What it is:** Collecting new evidence yourself (a short survey, counts at a location, a test offer) when public data cannot answer the question.

**Why it matters:** "Public data cannot answer this" is a valid, valuable finding. Inventing a number is not.

**How it appears in your work:** The decision brief and, for ADI501, the pilot recommendation (especially the pet-care case).

**Ask your agent:** "Design a cheap two-week test a small business could run to estimate demand."
