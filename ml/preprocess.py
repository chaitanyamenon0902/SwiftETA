"""
preprocess.py
-------------
Data loading, validation, cleaning, encoding and train/test split.
The Preprocessor class is stateful — fit on train, transform on test/live.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from ml.utils import (
    get_logger, timer, RANDOM_STATE, TEST_SIZE, TARGET_COL,
    ID_COLS, CAT_COLS, ALL_NUMERIC_FEATURES,
    SCALER_PATH, ENCODER_PATH,
)

log = get_logger("preprocess")


# ─────────────────────────────────────────────
# DATA LOADING & VALIDATION
# ─────────────────────────────────────────────

@timer
def load_and_validate(filepath: str) -> pd.DataFrame:
    """
    Load CSV, run sanity checks, return raw DataFrame.
    Raises on critical failures.
    """
    log.info(f"Loading dataset from: {filepath}")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")

    df = pd.read_csv(filepath, low_memory=False)
    log.info(f"Loaded {len(df):,} rows × {df.shape[1]} columns")

    # Must have target
    if TARGET_COL not in df.columns:
        raise ValueError(f"Target column '{TARGET_COL}' not found in dataset.")

    # Basic stats on target
    tgt = df[TARGET_COL]
    log.info(
        f"Target '{TARGET_COL}': min={tgt.min():.1f} | max={tgt.max():.1f} | "
        f"mean={tgt.mean():.1f} | std={tgt.std():.1f}"
    )

    missing_pct = df.isnull().mean() * 100
    cols_with_missing = missing_pct[missing_pct > 0]
    if not cols_with_missing.empty:
        log.warning(f"Columns with missing values:\n{cols_with_missing.to_string()}")

    return df


# ─────────────────────────────────────────────
# CLEANING
# ─────────────────────────────────────────────

@timer
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Remove obvious outliers in the target (< 5 or > 120 min)
    - Fill residual NaN values
    - Fix dtype issues
    """
    log.info("Cleaning dataset …")
    n_before = len(df)

    # Drop target outliers
    df = df[(df[TARGET_COL] >= 5) & (df[TARGET_COL] <= 120)].copy()
    log.info(f"Removed {n_before - len(df):,} target outliers → {len(df):,} rows remain")

    # Fill numeric NaN with median
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Fill categorical NaN with mode
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # Clip known score columns to valid range
    score_cols = [c for c in df.columns if "score" in c or "level" in c or "flag" in c]
    for col in score_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].clip(lower=0)

    log.info("Cleaning complete.")
    return df


# ─────────────────────────────────────────────
# PREPROCESSOR CLASS
# ─────────────────────────────────────────────

class Preprocessor:
    """
    Stateful preprocessing pipeline.

    Usage:
        prep = Preprocessor()
        X_train, X_test, y_train, y_test = prep.fit_transform(df)

        # Later, for a new single row:
        X_live = prep.transform_input(raw_dict)
    """

    def __init__(self):
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.scaler = StandardScaler()
        self.feature_columns: list[str] = []
        self._fitted = False

    # ─── fit_transform ───────────────────────

    @timer
    def fit_transform(self, df: pd.DataFrame):
        """
        Fit encoders + scaler on the full dataset,
        then return stratified train/test splits.
        """
        log.info("Fitting preprocessing pipeline …")
        df = df.copy()

        # ── Drop ID columns (no signal)
        df = df.drop(columns=[c for c in ID_COLS if c in df.columns], errors="ignore")

        # ── Separate target
        y = df.pop(TARGET_COL).values

        # ── Encode categoricals
        for col in CAT_COLS:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
                log.info(f"  Encoded '{col}': {list(le.classes_)}")

        # ── Keep only known feature columns (avoids leakage)
        all_expected = ALL_NUMERIC_FEATURES + CAT_COLS
        # also keep engineered cols that may be present
        extra_engineered = [
            "rain_x_peak", "dist_x_congestion", "weather_x_traffic",
            "prep_per_complexity", "rider_performance", "demand_pressure",
            "effective_speed", "est_travel_min", "rider_workload",
            "hour_sin", "hour_cos", "day_sin", "day_cos",
        ]
        keep_cols = [c for c in (all_expected + extra_engineered) if c in df.columns]
        df = df[keep_cols]
        self.feature_columns = keep_cols

        log.info(f"Feature matrix: {df.shape[1]} columns × {df.shape[0]:,} rows")

        # ── Scale
        X = self.scaler.fit_transform(df.values)

        # ── Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        log.info(f"Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")

        self._fitted = True
        return X_train, X_test, y_train, y_test

    # ─── transform_input ─────────────────────

    def transform_input(self, raw: dict) -> np.ndarray:
        """
        Transform a single raw input dictionary for live inference.
        Returns a (1, n_features) NumPy array.
        """
        if not self._fitted:
            raise RuntimeError("Preprocessor has not been fitted. Call fit_transform first.")

        row = {}
        for col in self.feature_columns:
            if col in raw:
                row[col] = raw[col]
            else:
                # Fill with 0 — missing features at inference time
                row[col] = 0

        # Apply label encoders
        for col, le in self.label_encoders.items():
            if col in row:
                val = str(row[col])
                if val in le.classes_:
                    row[col] = int(le.transform([val])[0])
                else:
                    row[col] = 0  # unknown category → 0

        arr = np.array([[row[c] for c in self.feature_columns]], dtype=float)
        return self.scaler.transform(arr)

    # ─── persistence ─────────────────────────

    def save(self):
        joblib.dump(
            {
                "label_encoders":  self.label_encoders,
                "scaler":          self.scaler,
                "feature_columns": self.feature_columns,
            },
            ENCODER_PATH,
        )
        log.info(f"Preprocessor saved → {ENCODER_PATH}")

    @classmethod
    def load(cls) -> "Preprocessor":
        data = joblib.load(ENCODER_PATH)
        obj = cls()
        obj.label_encoders  = data["label_encoders"]
        obj.scaler          = data["scaler"]
        obj.feature_columns = data["feature_columns"]
        obj._fitted = True
        log.info(f"Preprocessor loaded from {ENCODER_PATH}")
        return obj