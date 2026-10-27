# Variable dictionary

Every column in `data/clean/`, written by `scripts/pull_data.py` from the raw files in `data/raw/`. Census labels were taken from the official variable list (`https://api.census.gov/data/2023/acs/acs5/variables.json`, CBP: `.../2022/cbp/variables.json`).

"Estimate with MOE" means the ACS value is a survey estimate that comes with a 90% margin of error. Only the columns marked as having their own `_moe` column carry it in our tables; every other ACS value is still an estimate, but its MOE was not downloaded. Percentages are computed by the script from two ACS counts, so they also carry uncertainty that is not shown.

## `data/clean/orange_tracts_clean.csv` (ACS 5-year 2023, 92 tracts, Orange County NY)

| Column | Plain name | Unit | Census source | Estimate with MOE? |
|---|---|---|---|---|
| `geoid` | Tract ID (state + county + tract) | code | `state`, `county`, `tract` | No (identifier) |
| `town` | Town the tract belongs to | name | Mapping copied from the frozen `sample-data/orange_tracts_clean.csv` (the ACS tract response has no town field) | No (label) |
| `pop` | Total population | people (count) | B01003_001E "Total" | Estimate; MOE not downloaded |
| `median_income` | Median household income | dollars (2023 inflation-adjusted) | B19013_001E | **Yes**, see next row |
| `median_income_moe` | Margin of error of median household income | dollars (±) | B19013_001M | This is the MOE |
| `median_age` | Median age | years | B01002_001E | Estimate; MOE not downloaded |
| `pct_under18` | Share of residents under 18 | percent | B09001_001E ÷ B01003_001E × 100 | Derived from estimates |
| `pct_renter` | Share of occupied homes that are rented | percent | B25003_003E ÷ B25003_001E × 100 | Derived from estimates |
| `median_rent` | Median gross rent | dollars per month | B25064_001E | **Yes**, see next row |
| `median_rent_moe` | Margin of error of median rent | dollars (±) | B25064_001M | This is the MOE |
| `pct_commute_30plus` | Share of workers commuting 30 minutes or more | percent | (B08303_008E…013E) ÷ B08303_001E × 100 | Derived from estimates |
| `pct_built_pre1970` | Share of homes built before 1970 | percent | (B25034_008E…011E) ÷ B25034_001E × 100 | Derived from estimates |
| `pct_bachelors_plus` | Share of adults 25+ with a bachelor's degree or higher | percent | (B15003_022E…025E) ÷ B15003_001E × 100 | Derived from estimates |

## `data/clean/orange_towns_clean.csv` (ACS 5-year 2023, 24 towns/cities = county subdivisions)

| Column | Plain name | Unit | Census source | Estimate with MOE? |
|---|---|---|---|---|
| `town` | Town or city name | name | `NAME` before the first comma | No (label) |
| `pop` | Total population | people (count) | B01003_001E | Estimate; MOE not downloaded |
| `median_income` | Median household income | dollars | B19013_001E | **Yes** |
| `median_income_moe` | Its margin of error | dollars (±) | B19013_001M | This is the MOE |
| `median_rent` | Median gross rent | dollars per month | B25064_001E | **Yes** |
| `median_rent_moe` | Its margin of error | dollars (±) | B25064_001M | This is the MOE |
| `pct_renter` | Share of occupied homes that are rented | percent | B25003_003E ÷ B25003_001E × 100 | Derived from estimates |
| `pct_built_pre1970` | Share of homes built before 1970 | percent | (B25034_008E…011E) ÷ B25034_001E × 100 | Derived from estimates |
| `under3` | Children under 3 living in households | people (count) | B09001_003E "In households: Under 3 years" | Estimate; MOE not downloaded |
| `under5` | Children under 5 living in households | people (count) | B09001_003E + B09001_004E ("3 and 4 years") | Derived from estimates |
| `under18` | Population under 18 | people (count) | B09001_001E | Estimate; MOE not downloaded |
| `school_enrolled` | People 3+ enrolled in school | people (count) | B14001_002E | Estimate; MOE not downloaded |
| `pct_hh_non_english_only` | Share of households that speak a language other than only English | percent | (C16002_001E − C16002_002E) ÷ C16002_001E × 100 | Derived from estimates |
| `pct_hh_limited_english` | Share of households with limited English | percent | (C16002_004E + 007E + 010E + 013E) ÷ C16002_001E × 100 | Derived from estimates |

**Correction to the frozen sample:** `sample-data/orange_towns_clean.csv` has a column named `under5`, but its values are B09001_003E, which Census labels "Under 3 years". Our table keeps that value as `under3` and adds a true `under5`. Every other column matches the sample value for value (checked for all 24 towns and 92 tracts on 2026-10-27).

## `data/clean/cbp_orange_county.csv` (County Business Patterns 2022, Orange County NY)

| Column | Plain name | Unit | Census source | Estimate with MOE? |
|---|---|---|---|---|
| `naics` | Industry code | code | `NAICS2017` | No |
| `label` | Industry name | text | `NAICS2017_LABEL` | No |
| `role` | Why we pulled it | text | Added by us: 812910 = case industry, 541940 = contrast (vets) | No |
| `geography` | Area the count covers | name | `NAME` — the whole county, not a town | No |
| `establishments` | Number of business locations **with paid employees** | count | `ESTAB` "Number of establishments" | No (a count, not a survey estimate; businesses with no employees are not included) |
| `employees` | Number of paid employees | people (count) | `EMP` (mid-March pay period) | No |
| `annual_payroll_thousand_dollars` | Annual payroll | **thousands of dollars** | `PAYANN` "Annual payroll ($1,000)" | No |

## `data/clean/fred_CUSR0000SS61031.csv` (FRED; U.S. Bureau of Labor Statistics, U.S. city average, monthly)

| Column | Plain name | Unit | Source | Estimate with MOE? |
|---|---|---|---|---|
| `date` | Month | YYYY-MM-01 | `observation_date` | No |
| `index_value` | Consumer Price Index for All Urban Consumers: Pet Food and Treats in U.S. City Average | **index points (Dec 1997 = 100), seasonally adjusted — not dollars and not percent** (FRED series page, checked 2026-10-27) | `CUSR0000SS61031` | No MOE published; it is a national index of pet *food* prices, not a local price and not pet *services* |
