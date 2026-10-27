"""Fit and evaluate tract-income models for Week 6 Step 6."""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from sklearn.tree import DecisionTreeRegressor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "clean" / "orange_tracts_clean.csv"
TARGET = "median_income"
FEATURES = [
    "pop",
    "median_age",
    "pct_under18",
    "pct_renter",
    "pct_commute_30plus",
    "pct_built_pre1970",
    "pct_bachelors_plus",
]
TOWNS = ["Warwick town", "Monroe town"]
RANDOM_STATE = 42
TEST_SIZE = 0.25


def make_models() -> dict[str, DecisionTreeRegressor | RandomForestRegressor]:
    return {
        "Decision tree, no depth limit": DecisionTreeRegressor(
            random_state=RANDOM_STATE
        ),
        "Decision tree, max depth 3": DecisionTreeRegressor(
            max_depth=3, random_state=RANDOM_STATE
        ),
        "Random forest": RandomForestRegressor(
            n_estimators=500, random_state=RANDOM_STATE
        ),
    }


def main() -> None:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Required tract dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH)
    required_columns = {"geoid", "town", TARGET, *FEATURES}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    data = data.dropna(subset=[TARGET]).copy()
    missing_features = data[FEATURES].isna().sum()
    missing_features = missing_features[missing_features > 0]
    if not missing_features.empty:
        raise ValueError(
            "Selected features contain missing values; investigate before fitting:\n"
            f"{missing_features.to_string()}"
        )

    X = data[FEATURES]
    y = data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print(f"Input rows: {len(pd.read_csv(DATA_PATH))}")
    print(f"Rows with non-missing {TARGET}: {len(data)}")
    print(
        f"Train/test rows: {len(X_train)}/{len(X_test)} "
        f"(test fraction {TEST_SIZE:.0%}, random seed {RANDOM_STATE})"
    )
    print(f"Features: {', '.join(FEATURES)}")
    print("\nHeld-out test metrics (held-out predictions were not used for fitting):")

    models = make_models()
    fitted_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        fitted_models[name] = model
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)
        print(
            f"{name}: train R2={r2_score(y_train, train_predictions):.3f}, "
            f"held-out R2={r2_score(y_test, test_predictions):.3f}, "
            f"held-out MAE=${mean_absolute_error(y_test, test_predictions):,.0f}"
        )

    forest = fitted_models["Random forest"]
    importances = pd.Series(forest.feature_importances_, index=FEATURES)
    print("\nRandom forest top 3 feature importances (fit on training split only):")
    for rank, (feature, importance) in enumerate(
        importances.sort_values(ascending=False).head(3).items(), start=1
    ):
        print(f"{rank}. {feature}: {importance:.3f}")

    # Each tract's residual is based on predictions from folds that excluded it.
    out_of_fold_predictions = cross_val_predict(
        make_models()["Random forest"],
        X,
        y,
        cv=KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
    )
    residuals = data[["town", TARGET]].copy()
    residuals["residual"] = y.to_numpy() - out_of_fold_predictions
    print("\nTown out-of-fold residuals (actual minus predicted; 5-fold CV):")
    for town in TOWNS:
        town_rows = residuals[residuals["town"] == town]
        if town_rows.empty:
            raise ValueError(f"No target rows found for required town: {town}")
        print(
            f"{town}: tracts={len(town_rows)}, "
            f"mean actual=${town_rows[TARGET].mean():,.0f}, "
            f"mean residual=${town_rows['residual'].mean():,.0f}"
        )


if __name__ == "__main__":
    main()
