# API manifest

Written by `scripts/pull_data.py`. Every URL has the key replaced by `<KEY>`.

## Step 4 pull, 2026-10-29T19:17:47+00:00

| Request | URL | HTTP status | Rows | Retrieved (UTC) | Raw file |
|---|---|---|---|---|---|
| acs5_tracts | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB01003_001E%2CB19013_001E%2CB19013_001M%2CB01002_001E%2CB09001_001E%2CB25003_001E%2CB25003_003E%2CB25064_001E%2CB25064_001M%2CB08303_001E%2CB08303_008E%2CB08303_009E%2CB08303_010E%2CB08303_011E%2CB08303_012E%2CB08303_013E%2CB25034_001E%2CB25034_008E%2CB25034_009E%2CB25034_010E%2CB25034_011E%2CB15003_001E%2CB15003_022E%2CB15003_023E%2CB15003_024E%2CB15003_025E&for=tract%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 92 | 2026-10-29T19:17:44+00:00 | `data/raw/acs5_tracts.json` |
| acs5_towns | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB01003_001E%2CB19013_001E%2CB19013_001M%2CB25064_001E%2CB25064_001M%2CB25003_001E%2CB25003_003E%2CB25034_001E%2CB25034_008E%2CB25034_009E%2CB25034_010E%2CB25034_011E%2CB09001_003E%2CB09001_004E%2CB09001_001E%2CB14001_002E%2CC16002_001E%2CC16002_002E%2CC16002_004E%2CC16002_007E%2CC16002_010E%2CC16002_013E&for=county+subdivision%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 24 | 2026-10-29T19:17:45+00:00 | `data/raw/acs5_towns.json` |
| cbp_812910 | `https://api.census.gov/data/2022/cbp?get=NAME%2CNAICS2017_LABEL%2CESTAB%2CEMP%2CPAYANN&for=county%3A071&in=state%3A36&NAICS2017=812910&key=<KEY>` | 200 | 1 | 2026-10-29T19:17:46+00:00 | `data/raw/cbp_812910.json` |
| cbp_541940 | `https://api.census.gov/data/2022/cbp?get=NAME%2CNAICS2017_LABEL%2CESTAB%2CEMP%2CPAYANN&for=county%3A071&in=state%3A36&NAICS2017=541940&key=<KEY>` | 200 | 1 | 2026-10-29T19:17:46+00:00 | `data/raw/cbp_541940.json` |
| fred_CUSR0000SS61031 | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUSR0000SS61031` | 200 | 297 | 2026-10-29T19:17:47+00:00 | `data/raw/fred_CUSR0000SS61031.csv` |

## Step 7 F2 broken requests and fixes, 2026-10-27T18:55:29+00:00

| Request | URL | HTTP status | Rows | Retrieved (UTC) | Raw file |
|---|---|---|---|---|---|
| A-county-71 | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A71&key=<KEY>` | 204 | 0 | 2026-10-27T18:55:26+00:00 | `data/raw/broken/A-county-71.response.txt` |
| A-county-71-fixed | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 92 | 2026-10-27T18:55:26+00:00 | `data/raw/broken/A-county-71-fixed.response.txt` |
| B-wrong-county-017 | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A017&key=<KEY>` | 200 | 16 | 2026-10-27T18:55:27+00:00 | `data/raw/broken/B-wrong-county-017.response.txt` |
| B-wrong-county-017-fixed | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 92 | 2026-10-27T18:55:27+00:00 | `data/raw/broken/B-wrong-county-017-fixed.response.txt` |
| C-old-vintage-2009 | `https://api.census.gov/data/2009/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 67 | 2026-10-27T18:55:28+00:00 | `data/raw/broken/C-old-vintage-2009.response.txt` |
| C-old-vintage-2009-fixed | `https://api.census.gov/data/2023/acs/acs5?get=NAME%2CB19013_001E&for=tract%3A%2A&in=state%3A36+county%3A071&key=<KEY>` | 200 | 92 | 2026-10-27T18:55:28+00:00 | `data/raw/broken/C-old-vintage-2009-fixed.response.txt` |

