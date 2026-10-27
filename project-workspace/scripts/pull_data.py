"""Week 6 data pull: Census ACS + CBP and FRED for the pet-care case (Team 3).

Run from project-workspace/, after loading your key in YOUR OWN terminal:

    source .venv/bin/activate
    set -a; . ./.env; set +a
    python scripts/pull_data.py              # Step 4: the five downloads
    python scripts/pull_data.py --broken     # Step 7 F2: the three broken requests, then fixed

What it does, in order:
 1. Reads the key from the CENSUS_API environment variable. It never prints it.
 2. Downloads ACS 2023 tracts, ACS 2023 towns, CBP 2022 (812910, 541940), FRED CUSR0000SS61031.
 3. Saves every response unchanged in data/raw/.
 4. Writes clean tables in data/clean/.
 5. Writes api-manifest.md (URL with the key replaced by <KEY>, HTTP status, rows, date).
 6. Stops with an error if the tract request is not 92 rows or the key appears in any output.
It never deletes anything and writes only inside data/ and api-manifest.md.
"""
import argparse
import csv
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent          # project-workspace/
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
MANIFEST = ROOT / "api-manifest.md"
SAMPLE = ROOT / "sample-data"

STATE, COUNTY = "36", "071"                              # New York, Orange County
ACS_YEAR, CBP_YEAR = 2023, 2022
EXPECTED_TRACTS = 92
NAICS = {"812910": "case industry", "541940": "contrast (vets)"}
FRED_SERIES = "CUSR0000SS61031"
TIMEOUT = 60

# Same variables as the frozen sample (sample-data/api_manifest.json), so results can be compared.
TRACT_VARS = ["NAME", "B01003_001E", "B19013_001E", "B19013_001M", "B01002_001E", "B09001_001E",
              "B25003_001E", "B25003_003E", "B25064_001E", "B25064_001M", "B08303_001E",
              "B08303_008E", "B08303_009E", "B08303_010E", "B08303_011E", "B08303_012E", "B08303_013E",
              "B25034_001E", "B25034_008E", "B25034_009E", "B25034_010E", "B25034_011E",
              "B15003_001E", "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]
# Sample town variables plus B09001_004E ("3 and 4 years"): the sample's "under5" is really
# B09001_003E alone, which Census labels "Under 3 years".
TOWN_VARS = ["NAME", "B01003_001E", "B19013_001E", "B19013_001M", "B25064_001E", "B25064_001M",
             "B25003_001E", "B25003_003E", "B25034_001E", "B25034_008E", "B25034_009E", "B25034_010E",
             "B25034_011E", "B09001_003E", "B09001_004E", "B09001_001E", "B14001_002E",
             "C16002_001E", "C16002_002E", "C16002_004E", "C16002_007E", "C16002_010E", "C16002_013E"]

# Step 7 F2: the three requests from sample-data/broken-requests/README.md, and their fixes.
BROKEN = [
    ("A-county-71", {"year": 2023, "county": "71"}, "county must be the three-digit string 071"),
    ("B-wrong-county-017", {"year": 2023, "county": "017"}, "017 is a different county; Orange is 071"),
    ("C-old-vintage-2009", {"year": 2009, "county": "071"}, "2009 is an old vintage; the project uses ACS 2023"),
]


def get_key():
    key = os.environ.get("CENSUS_API", "").strip()
    if not key:
        sys.exit("CENSUS_API is empty. In project-workspace/, run:  set -a; . ./.env; set +a  "
                 "then run this script again. (Never paste the key into a file or a chat.)")
    return key


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def redact(text, key):
    return text.replace(key, "<KEY>") if key else text


def fetch(name, base, params, key, out_path, kind):
    """One request. Saves the body unchanged and returns a manifest row (key redacted)."""
    if key:
        params = {**params, "key": key}
    url = requests.Request("GET", base, params=params).prepare().url
    row = {"name": name, "url": redact(url, key), "retrieved": now(), "raw_file": str(out_path.relative_to(ROOT))}
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        row.update(status=f"error: {redact(type(e).__name__ + ' ' + str(e), key)}", rows=0)
        return row, None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(r.content)
    rows, parsed = 0, None
    if r.status_code == 200 and r.content.strip():
        if kind == "json":
            try:
                parsed = r.json()
                rows = len(parsed) - 1
            except ValueError:
                rows = 0
        else:
            parsed = r.text
            rows = max(len(r.text.strip().splitlines()) - 1, 0)
    row.update(status=r.status_code, rows=rows)
    return row, parsed


def num(v):
    """Census strings to float; Census 'no data' codes (large negatives) become None."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x < -100000 else x


def pct(part, whole):
    return None if part is None or not whole else round(100 * part / whole, 2)


def total(rec, cols):
    vals = [num(rec[c]) for c in cols]
    return None if any(v is None for v in vals) else sum(vals)


def town_of_tract():
    """Tract-to-town mapping from the frozen sample (the ACS tract response has no town field)."""
    with open(SAMPLE / "orange_tracts_clean.csv", newline="") as f:
        return {r["geoid"]: r["town"] for r in csv.DictReader(f)}


def clean_tracts(table):
    head, rows = table[0], table[1:]
    towns = town_of_tract()
    out = []
    for raw in rows:
        r = dict(zip(head, raw))
        geoid = r["state"] + r["county"] + r["tract"]
        pop = num(r["B01003_001E"])
        out.append({
            "geoid": geoid, "town": towns.get(geoid, ""), "pop": pop,
            "median_income": num(r["B19013_001E"]), "median_income_moe": num(r["B19013_001M"]),
            "median_age": num(r["B01002_001E"]), "pct_under18": pct(num(r["B09001_001E"]), pop),
            "pct_renter": pct(num(r["B25003_003E"]), num(r["B25003_001E"])),
            "median_rent": num(r["B25064_001E"]), "median_rent_moe": num(r["B25064_001M"]),
            "pct_commute_30plus": pct(total(r, [f"B08303_0{i:02d}E" for i in range(8, 14)]), num(r["B08303_001E"])),
            "pct_built_pre1970": pct(total(r, [f"B25034_0{i:02d}E" for i in range(8, 12)]), num(r["B25034_001E"])),
            "pct_bachelors_plus": pct(total(r, [f"B15003_0{i:02d}E" for i in range(22, 26)]), num(r["B15003_001E"])),
        })
    return out


def clean_towns(table):
    head, rows = table[0], table[1:]
    out = []
    for raw in rows:
        r = dict(zip(head, raw))
        hh = num(r["C16002_001E"])
        out.append({
            "town": r["NAME"].split(",")[0], "pop": num(r["B01003_001E"]),
            "median_income": num(r["B19013_001E"]), "median_income_moe": num(r["B19013_001M"]),
            "median_rent": num(r["B25064_001E"]), "median_rent_moe": num(r["B25064_001M"]),
            "pct_renter": pct(num(r["B25003_003E"]), num(r["B25003_001E"])),
            "pct_built_pre1970": pct(total(r, [f"B25034_0{i:02d}E" for i in range(8, 12)]), num(r["B25034_001E"])),
            "under3": num(r["B09001_003E"]), "under5": total(r, ["B09001_003E", "B09001_004E"]),
            "under18": num(r["B09001_001E"]), "school_enrolled": num(r["B14001_002E"]),
            "pct_hh_non_english_only": pct(None if hh is None or num(r["C16002_002E"]) is None else hh - num(r["C16002_002E"]), hh),
            "pct_hh_limited_english": pct(total(r, ["C16002_004E", "C16002_007E", "C16002_010E", "C16002_013E"]), hh),
        })
    return out


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_manifest(rows, title, append=False):
    lines = [] if append else ["# API manifest", "",
                               "Written by `scripts/pull_data.py`. Every URL has the key replaced by `<KEY>`.", ""]
    lines += [f"## {title}", "", "| Request | URL | HTTP status | Rows | Retrieved (UTC) | Raw file |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['name']} | `{r['url']}` | {r['status']} | {r['rows']} | {r['retrieved']} | `{r['raw_file']}` |")
    text = "\n".join(lines) + "\n\n"
    with open(MANIFEST, "a" if append else "w") as f:
        f.write(text)


def key_leaks(key):
    """Every file this script wrote that contains the key (should be none)."""
    paths = [MANIFEST] + [p for p in (ROOT / "data").rglob("*") if p.is_file()]
    return [str(p.relative_to(ROOT)) for p in paths if p.exists() and key in p.read_text(errors="ignore")]


def acs_url(year):
    return f"https://api.census.gov/data/{year}/acs/acs5"


def run_main(key):
    rows = []
    geo = {"in": f"state:{STATE} county:{COUNTY}"}
    m, tracts = fetch("acs5_tracts", acs_url(ACS_YEAR), {"get": ",".join(TRACT_VARS), "for": "tract:*", **geo},
                      key, RAW / "acs5_tracts.json", "json")
    rows.append(m)
    m, towns = fetch("acs5_towns", acs_url(ACS_YEAR), {"get": ",".join(TOWN_VARS), "for": "county subdivision:*", **geo},
                     key, RAW / "acs5_towns.json", "json")
    rows.append(m)
    cbp = []
    for code, note in NAICS.items():
        m, body = fetch(f"cbp_{code}", f"https://api.census.gov/data/{CBP_YEAR}/cbp",
                        {"get": "NAME,NAICS2017_LABEL,ESTAB,EMP,PAYANN", "for": f"county:{COUNTY}",
                         "in": f"state:{STATE}", "NAICS2017": code}, key, RAW / f"cbp_{code}.json", "json")
        rows.append(m)
        if body:
            r = dict(zip(body[0], body[1]))
            cbp.append({"naics": code, "label": r["NAICS2017_LABEL"], "role": note, "geography": r["NAME"],
                        "establishments": num(r["ESTAB"]), "employees": num(r["EMP"]),
                        "annual_payroll_thousand_dollars": num(r["PAYANN"])})
    m, fred = fetch(f"fred_{FRED_SERIES}", "https://fred.stlouisfed.org/graph/fredgraph.csv", {"id": FRED_SERIES},
                    None, RAW / f"fred_{FRED_SERIES}.csv", "csv")
    rows.append(m)

    if tracts:
        write_csv(CLEAN / "orange_tracts_clean.csv", clean_tracts(tracts))
    if towns:
        write_csv(CLEAN / "orange_towns_clean.csv", clean_towns(towns))
    if cbp:
        write_csv(CLEAN / "cbp_orange_county.csv", cbp)
    if fred:
        data = list(csv.reader(io.StringIO(fred)))
        write_csv(CLEAN / f"fred_{FRED_SERIES}.csv",
                  [{"date": d, "index_value": num(v)} for d, v in data[1:]])
    write_manifest(rows, f"Step 4 pull, {now()}")

    print("Request                status  rows")
    for r in rows:
        print(f"{r['name']:<22} {str(r['status']):<7} {r['rows']}")
    sample_counts = {"acs5_tracts": EXPECTED_TRACTS, "acs5_towns": 24}
    for r in rows:
        if r["name"] in sample_counts:
            same = "matches" if r["rows"] == sample_counts[r["name"]] else "DIFFERS FROM"
            print(f"{r['name']}: {r['rows']} rows, {same} the frozen sample ({sample_counts[r['name']]})")
    return rows


def run_broken(key):
    rows = []
    for name, p, fix in BROKEN:
        geo = {"get": "NAME,B19013_001E", "for": "tract:*", "in": f"state:{STATE} county:{p['county']}"}
        m, _ = fetch(name, acs_url(p["year"]), geo, key, RAW / "broken" / f"{name}.response.txt", "json")
        m["fix"] = fix
        rows.append(m)
        fixed = {"get": "NAME,B19013_001E", "for": "tract:*", "in": f"state:{STATE} county:{COUNTY}"}
        m2, _ = fetch(name + "-fixed", acs_url(ACS_YEAR), fixed, key, RAW / "broken" / f"{name}-fixed.response.txt", "json")
        rows.append(m2)
    write_manifest(rows, f"Step 7 F2 broken requests and fixes, {now()}", append=True)
    print("Request                          status  rows")
    for r in rows:
        print(f"{r['name']:<32} {str(r['status']):<7} {r['rows']}")
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--broken", action="store_true", help="Step 7 F2: run the three broken requests, then the fixed ones")
    args = ap.parse_args()
    key = get_key()
    rows = run_broken(key) if args.broken else run_main(key)

    leaks = key_leaks(key)
    if leaks:
        sys.exit(f"STOP: the key appears in {leaks}. Remove it before committing or sharing anything.")
    print("Key check: the key does not appear in data/ or api-manifest.md.")
    if not args.broken:
        tract = next(r for r in rows if r["name"] == "acs5_tracts")
        if tract["rows"] != EXPECTED_TRACTS:
            sys.exit(f"STOP: tract request returned {tract['rows']} rows, expected {EXPECTED_TRACTS}.")
        bad = [r["name"] for r in rows if r["status"] != 200]
        if bad:
            sys.exit(f"STOP: these requests did not return HTTP 200: {bad}")
        print(f"OK: all requests returned 200 and the tract request has {EXPECTED_TRACTS} rows.")


if __name__ == "__main__":
    main()
