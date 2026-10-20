# Demonstration Checklist (Step 10)


Tick each item **before** your slot. Do not walk in with an unchecked box.

## Both courses

- [ ] Fresh terminal: key loaded from `.env` (without printing it)
- [ ] `scripts/pull_data.py` runs from a fresh terminal; manifest shows 92 tract rows
- [ ] Can predict, then show, what happens when county `71` is used
- [ ] One NotebookLM answer ready, with the cited passage open and confirmed
- [ ] Claim ledger open: at least one `refuted` row and one `proxy` row, each traced to a raw file
- [ ] Model card open: train and held-out for tree and forest; can explain the gap in plain words
- [ ] Leakage table: can explain which column leaks and the score before and after
- [ ] `moe_pair.csv`: can say why Warwick and Monroe cannot be ranked
- [ ] Can state two things public data cannot tell your client, plus one cheap primary-research test
- [ ] Decision brief open (3 pages or fewer, 5 to 8 numbered claims, each tied to a ledger row)
- [ ] Search of the ZIP for your key found zero hits; `.env` is not in the archive
- [ ] Every teammate knows which part they will speak and operate

## ADI501 only

- [ ] Adoption recommendation and the owner, cost, and refresh step behind it
- [ ] Pilot continue, revise, stop thresholds, and the one number that flips the decision
- [ ] One numeric guardrail from the model-risk note
- [ ] Governance table: who signs off before the brief reaches the client

## If something fails during the demo

Say what you predicted, show what happened, say which of data, logic, or interface it is, and show your smallest fix. A calm diagnosis scores better than a hidden failure.
