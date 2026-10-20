# Broken request fixtures (expected: 92 tracts for Orange County 36/071, ACS 2023)

- **A-county-71**: `https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:36%20county:71&key=<KEY>` -> HTTP 204, 0 rows
- **B-wrong-county-017**: `https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:36%20county:017&key=<KEY>` -> HTTP 200, 16 rows
- **C-old-vintage-2009**: `https://api.census.gov/data/2009/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:36%20county:071&key=<KEY>` -> HTTP 200, 67 rows
