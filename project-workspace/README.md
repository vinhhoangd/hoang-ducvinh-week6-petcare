# Pet-care daycare: Warwick town vs Monroe town (Team 3, case 4)

For the client: what public data says about opening a dog daycare with grooming in Warwick town or Monroe town (Orange County, New York), and how to rebuild the analysis.

## What the data can tell you
- *(Filled in after Steps 7–8: three bullets, each tied to a numbered claim in `decision-brief.md`.)*

## What it cannot tell you
- **How many households own a dog or cat, or what they spend on pet care.** No public dataset used here counts pets; every population, income or family number is only a stand-in.
- **Who your competitors are near a specific location.** The business count (24 pet-care businesses with employees in 2022) covers all of Orange County, not Warwick or Monroe, and leaves out one-person businesses with no employees.
- **Which town's households earn more.** The two median incomes are within each other's margin of error ($117,680 ± $8,605 vs $116,019 ± $13,663), so the survey cannot rank them.
- **Local prices for grooming or daycare.** The price series is a national index for pet *food*, measured in index points, not dollars.

## How to re-run this analysis
You need a free Census API key of your own (https://api.census.gov/data/key_signup.html). Put it only in a file named `.env` in this folder, as one line `CENSUS_API=your-key`, typed yourself. Never put the key in any other file, chat, screenshot or ZIP.

One-time setup (in this folder, with [uv](https://docs.astral.sh/uv/) installed):
```bash
uv venv --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt
```

Each time, in your own terminal:
```bash
source .venv/bin/activate && set -a; . ./.env; set +a && python scripts/pull_data.py
```
It downloads five public datasets into `data/raw/`, writes clean tables in `data/clean/` and a receipt in `api-manifest.md`, and finishes with "OK: … 92 rows" when everything worked.

Rebuilding the NotebookLM notebook:
Sign in to NotebookLM in your own terminal via `nlm login`, then run the reproducible commands in `skills/source-grounded-research/SKILL.md`:
```bash
nlm notebook create "Pet-care - Warwick town vs Monroe town"
nlm alias set petcare <notebook-id>
nlm source add petcare --url "https://www.census.gov/programs-surveys/acs/about.html" --wait
nlm source add petcare --url "https://www.census.gov/programs-surveys/cbp/about.html" --wait
nlm source add petcare --url "https://fred.stlouisfed.org/series/CUSR0000SS61031" --wait
nlm source add petcare --file "sample-data/orange_towns_clean.csv" --wait
```
Query with `nlm notebook query petcare "<question>"`.

## One known limitation
- The Census numbers are survey estimates averaged over 2019–2023, and each town is made of only a few neighbourhoods (8 tracts in Warwick, 5 in Monroe), so small differences between the towns can be noise.

## One concrete next step for the owner
- *(Filled in after the team's recommendation in `decision-brief.md`.)*
