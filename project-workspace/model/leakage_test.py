"""Week 6 Step 7, failure F3: find the column that leaks the answer.

Same setup as model/fit_models.py (25% held-out test set, seed 42, 500-tree
random forest) so the scores are comparable. Run from project-workspace/:

    .venv/bin/python model/leakage_test.py
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "sample-data" / "leakage_starter_table.csv"
TARGET = "median_income"
NOT_FEATURES = ["geoid", "town", TARGET]   # identifiers and the answer itself
RANDOM_STATE = 42
TEST_SIZE = 0.25


def fit_and_score(data, features):
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data[TARGET], test_size=TEST_SIZE, random_state=RANDOM_STATE)
    forest = RandomForestRegressor(n_estimators=500, random_state=RANDOM_STATE).fit(X_train, y_train)
    pred = forest.predict(X_test)
    importances = pd.Series(forest.feature_importances_, index=features).sort_values(ascending=False)
    return r2_score(y_train, forest.predict(X_train)), r2_score(y_test, pred), mean_absolute_error(y_test, pred), importances


def main():
    data = pd.read_csv(DATA_PATH).dropna()
    features = [c for c in data.columns if c not in NOT_FEATURES]
    print(f"Rows used: {len(data)} | train/test: {round(len(data) * (1 - TEST_SIZE))}/{round(len(data) * TEST_SIZE)} "
          f"(seed {RANDOM_STATE}) | features: {', '.join(features)}\n")

    tr, te, mae, imp = fit_and_score(data, features)
    print(f"WITH every column:   train R2={tr:.3f}, held-out R2={te:.3f}, held-out MAE=${mae:,.0f}")
    print("Top 3 importances:", ", ".join(f"{k} {v:.3f}" for k, v in imp.head(3).items()))

    suspect = imp.index[0]
    bands = data.groupby(suspect)[TARGET].agg(["min", "max", "count"]).sort_index()
    overlaps = sum(bands["max"].iloc[i] >= bands["min"].iloc[i + 1] for i in range(len(bands) - 1))
    print(f"\nWhy '{suspect}' leaks: it is the target cut into {len(bands)} bands. Income range per band:")
    for band, row in bands.iterrows():
        print(f"  {suspect}={band}: ${row['min']:,.0f} to ${row['max']:,.0f} ({int(row['count'])} tracts)")
    print(f"Overlapping band ranges: {overlaps} (0 means each band is a fixed slice of the answer)")
    print(f"Spearman rank correlation with {TARGET}: {data[suspect].corr(data[TARGET], method='spearman'):.3f}")
    rule = (data[TARGET] // 10000).astype(int)
    print(f"Rows where {suspect} == {TARGET} // 10,000 exactly: {(rule == data[suspect]).sum()} of {len(data)}")

    kept = [c for c in features if c != suspect]
    tr2, te2, mae2, imp2 = fit_and_score(data, kept)
    print(f"\nWITHOUT '{suspect}': train R2={tr2:.3f}, held-out R2={te2:.3f}, held-out MAE=${mae2:,.0f}")
    print("Top 3 importances:", ", ".join(f"{k} {v:.3f}" for k, v in imp2.head(3).items()))


if __name__ == "__main__":
    main()
