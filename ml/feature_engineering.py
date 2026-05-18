"""
feature_engineering.py
-----------------------
All feature creation logic lives here.
Designed to work on the raw Swiggy CSV and add/verify every feature
needed by the model. Compatible with both the synthetic dataset produced
by our generator and a real CSV that may be missing some columns.
"""

import numpy as np
import pandas as pd
from ml.utils import get_logger, haversine_vectorised, timer

log = get_logger("feature_engineering")


# ─────────────────────────────────────────────
# ORDER TYPE → PREP TIME LOOKUP
# ─────────────────────────────────────────────
PREP_TIME_LOOKUP = {
    "Drink":   (3,  8),
    "Snack":   (5,  15),
    "Dessert": (5,  15),
    "Meal":    (12, 28),
    "Buffet":  (20, 45),
}

COMPLEXITY_LOOKUP = {
    "Drink":   (1, 4),
    "Snack":   (2, 5),
    "Dessert": (2, 6),
    "Meal":    (4, 8),
    "Buffet":  (7, 10),
}

VEHICLE_SPEED_LOOKUP = {
    "Bike":     (6.5, 9.0),
    "Scooter":  (5.5, 8.5),
    "Bicycle":  (2.5, 5.5),
}


def _synthesise_column(df: pd.DataFrame, col: str) -> pd.Series:
    """
    If a column is missing from the raw CSV, synthesise it from
    correlated existing columns so the pipeline still works.
    Returns a Series aligned to df.index.
    """
    n = len(df)
    rng = np.random.default_rng(42)

    if col == "distance_km":
        return pd.Series(
            haversine_vectorised(
                df["restaurant_latitude"].values,
                df["restaurant_longitude"].values,
                df["customer_latitude"].values,
                df["customer_longitude"].values,
            ).round(2),
            index=df.index,
        )

    if col == "hour_of_day":
        return pd.to_datetime(df["order_timestamp"]).dt.hour

    if col == "day_of_week":
        return pd.to_datetime(df["order_timestamp"]).dt.dayofweek

    if col == "is_weekend":
        return (pd.to_datetime(df["order_timestamp"]).dt.dayofweek >= 5).astype(int)

    if col == "is_peak_hour":
        h = pd.to_datetime(df["order_timestamp"]).dt.hour
        return (((h >= 12) & (h <= 14)) | ((h >= 19) & (h <= 22))).astype(int)

    if col == "time_bucket":
        h = pd.to_datetime(df["order_timestamp"]).dt.hour
        return pd.cut(
            h,
            bins=[-1, 4, 11, 16, 21, 24],
            labels=["Late Night", "Morning", "Afternoon", "Evening", "Late Night"],
            ordered=False,
        ).astype(str)

    if col == "items_count":
        base = {"Drink": 1, "Snack": 2, "Dessert": 2, "Meal": 4, "Buffet": 8}
        return df["order_type"].map(base).fillna(3).astype(int) + rng.integers(0, 3, n)

    if col == "estimated_prep_time":
        vals = np.zeros(n)
        for ot, (lo, hi) in PREP_TIME_LOOKUP.items():
            mask = df["order_type"] == ot
            vals[mask] = rng.uniform(lo, hi, mask.sum())
        return pd.Series(vals.round(1), index=df.index)

    if col == "order_complexity_score":
        vals = np.zeros(n)
        for ot, (lo, hi) in COMPLEXITY_LOOKUP.items():
            mask = df["order_type"] == ot
            vals[mask] = rng.uniform(lo, hi, mask.sum())
        return pd.Series(np.clip(vals, 1, 10).round(2), index=df.index)

    if col == "rider_experience_score":
        return pd.Series(
            np.clip((df["rider_age"] - 18) / 27 * 7 + rng.uniform(1, 3, n), 1, 10).round(2),
            index=df.index,
        )

    if col == "vehicle_speed_score":
        vals = np.zeros(n)
        for vt, (lo, hi) in VEHICLE_SPEED_LOOKUP.items():
            mask = df["vehicle_type"] == vt
            vals[mask] = rng.uniform(lo, hi, mask.sum())
        return pd.Series(vals.round(2), index=df.index)

    if col == "rider_active_orders":
        return pd.Series(
            rng.choice([0, 1, 2, 3, 4], n, p=[0.15, 0.30, 0.28, 0.18, 0.09]),
            index=df.index,
        )

    if col == "rider_idle_time":
        active = df.get("rider_active_orders", pd.Series(np.ones(n), index=df.index))
        return pd.Series(
            np.clip(rng.exponential(8, n) - active.values * 3, 0, 60).round(1),
            index=df.index,
        )

    if col == "traffic_level":
        peak = df.get("is_peak_hour", pd.Series(np.zeros(n), index=df.index)).values
        base = np.where(peak, rng.uniform(6.5, 10.0, n), rng.uniform(3.0, 7.5, n))
        return pd.Series(np.clip(base, 1, 10).round(2), index=df.index)

    if col == "road_congestion_score":
        tl  = df.get("traffic_level", pd.Series(np.full(n, 5.0), index=df.index)).values
        zd  = df.get("zone_density_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(tl * 0.8 + zd * 0.15 + rng.uniform(-1, 1, n), 1, 10).round(2), index=df.index)

    if col == "signal_density":
        zd = df.get("zone_density_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(zd * 0.6 + rng.uniform(1, 4, n), 1, 10).round(2), index=df.index)

    if col == "average_road_speed":
        tl = df.get("traffic_level", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(40 - tl * 3.2 - rng.uniform(0, 5, n), 6, 45).round(1), index=df.index)

    if col == "zone_density_score":
        tl = df.get("traffic_level", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(tl * 0.7 + rng.uniform(0.5, 3.5, n), 1, 10).round(2), index=df.index)

    if col == "route_complexity_score":
        zd = df.get("zone_density_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        sd = df.get("signal_density", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(zd * 0.5 + sd * 0.3 + rng.uniform(0.5, 2.5, n), 1, 10).round(2), index=df.index)

    if col == "weather_condition":
        return pd.Series(
            rng.choice(["Sunny", "Cloudy", "Rainy", "Stormy"], n, p=[0.45, 0.28, 0.20, 0.07]),
            index=df.index,
        )

    if col == "weather_severity_score":
        wmap = {"Sunny": 1.0, "Cloudy": 2.0, "Rainy": 6.0, "Stormy": 9.0}
        return df["weather_condition"].map(wmap).fillna(3.0).round(2)

    if col == "rain_flag":
        return df["weather_condition"].isin(["Rainy", "Stormy"]).astype(int)

    if col == "active_orders_nearby":
        zd = df.get("zone_density_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series(np.clip(rng.poisson(zd * 1.5), 0, 30).astype(int), index=df.index)

    if col == "rider_supply_demand_ratio":
        peak = df.get("is_peak_hour", pd.Series(np.zeros(n), index=df.index)).values
        return pd.Series(np.clip(1.5 - peak * 0.5 + rng.uniform(-0.3, 0.3, n), 0.2, 2.5).round(2), index=df.index)

    if col == "restaurant_queue_length":
        pt = df.get("estimated_prep_time", pd.Series(np.full(n, 15.0), index=df.index)).values
        peak = df.get("is_peak_hour", pd.Series(np.zeros(n), index=df.index)).values
        return pd.Series(
            np.clip(np.round(pt / 10 + peak * rng.uniform(1, 4, n) + rng.poisson(1.5, n)), 0, 20).astype(int),
            index=df.index,
        )

    if col == "batch_delivery_flag":
        ao = df.get("rider_active_orders", pd.Series(np.zeros(n), index=df.index)).values
        return pd.Series(((ao >= 2) & (rng.random(n) < 0.35)).astype(int), index=df.index)

    if col == "zone_demand_score":
        zd   = df.get("zone_density_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        peak = df.get("is_peak_hour", pd.Series(np.zeros(n), index=df.index)).values
        wk   = df.get("is_weekend", pd.Series(np.zeros(n), index=df.index)).values
        return pd.Series(np.clip(zd*0.6 + peak*2.0 + wk*1.0 + rng.uniform(0, 2, n), 1, 10).round(2), index=df.index)

    if col == "delivery_hotspot_flag":
        zds = df.get("zone_demand_score", pd.Series(np.full(n, 5.0), index=df.index)).values
        return pd.Series((zds >= 7.0).astype(int), index=df.index)

    raise ValueError(f"No synthesis rule for column: {col}")


# ─────────────────────────────────────────────
# INTERACTION FEATURES
# ─────────────────────────────────────────────

def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cross-product / ratio features that capture real-world
    non-linear relationships between variables.
    """
    df = df.copy()

    # Rain × peak hour: compounding delay
    df["rain_x_peak"]          = df["rain_flag"] * df["is_peak_hour"]

    # Distance × congestion: longer road through busy area = worse
    df["dist_x_congestion"]    = df["distance_km"] * df["road_congestion_score"]

    # Weather severity × traffic: multiplicative misery index
    df["weather_x_traffic"]    = df["weather_severity_score"] * df["traffic_level"]

    # Prep time relative to order complexity
    df["prep_per_complexity"]  = (df["estimated_prep_time"] /
                                  df["order_complexity_score"].clip(lower=1))

    # Rider performance index (high rating + experience = better)
    df["rider_performance"]    = (df["rider_rating"] * 0.6 +
                                  df["rider_experience_score"] * 0.4)

    # Demand pressure: queue vs supply ratio
    df["demand_pressure"]      = (df["restaurant_queue_length"] /
                                  df["rider_supply_demand_ratio"].clip(lower=0.1))

    # Effective travel speed estimate
    df["effective_speed"]      = (df["average_road_speed"] *
                                  (df["vehicle_speed_score"] / 10))

    # Estimated travel minutes (engineered, not used as target)
    df["est_travel_min"]       = (df["distance_km"] /
                                  df["effective_speed"].clip(lower=0.5)) * 60

    # Workload index: active orders + batch penalty
    df["rider_workload"]       = (df["rider_active_orders"] * 2 +
                                  df["batch_delivery_flag"] * 1.5)

    # Hour sine/cosine for cyclical encoding
    df["hour_sin"]             = np.sin(2 * np.pi * df["hour_of_day"] / 24)
    df["hour_cos"]             = np.cos(2 * np.pi * df["hour_of_day"] / 24)

    # Day sine/cosine
    df["day_sin"]              = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_cos"]              = np.cos(2 * np.pi * df["day_of_week"] / 7)

    log.info(f"Added 12 interaction / cyclical features. Shape: {df.shape}")
    return df


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

REQUIRED_COLS = (
    ["distance_km", "hour_of_day", "day_of_week", "is_weekend", "is_peak_hour",
     "time_bucket", "order_complexity_score", "estimated_prep_time", "items_count",
     "rider_experience_score", "vehicle_speed_score", "rider_active_orders",
     "rider_idle_time", "traffic_level", "road_congestion_score", "signal_density",
     "average_road_speed", "zone_density_score", "route_complexity_score",
     "weather_condition", "weather_severity_score", "rain_flag",
     "active_orders_nearby", "rider_supply_demand_ratio", "restaurant_queue_length",
     "batch_delivery_flag", "zone_demand_score", "delivery_hotspot_flag"]
)


@timer
def run_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master feature engineering function.
    - Verifies all required columns exist
    - Synthesises any missing ones
    - Adds interaction features
    Returns an enriched DataFrame.
    """
    log.info("Starting feature engineering …")
    df = df.copy()

    # Ensure weather_condition exists before rain_flag / weather_severity_score
    priority_order = [
        "hour_of_day", "day_of_week", "is_weekend", "is_peak_hour", "time_bucket",
        "distance_km", "estimated_prep_time", "order_complexity_score", "items_count",
        "rider_experience_score", "vehicle_speed_score", "rider_active_orders",
        "rider_idle_time", "traffic_level", "zone_density_score",
        "road_congestion_score", "signal_density", "average_road_speed",
        "route_complexity_score", "weather_condition", "weather_severity_score",
        "rain_flag", "active_orders_nearby", "rider_supply_demand_ratio",
        "restaurant_queue_length", "batch_delivery_flag", "zone_demand_score",
        "delivery_hotspot_flag",
    ]

    for col in priority_order:
        if col not in df.columns:
            log.warning(f"Column '{col}' missing — synthesising from correlated features.")
            df[col] = _synthesise_column(df, col)

    df = add_interaction_features(df)
    log.info(f"Feature engineering complete. Final shape: {df.shape}")
    return df