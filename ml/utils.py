"""
utils.py
--------
Shared utilities: logging setup, constants, helpers.
"""

import logging
import os
import sys
import time
import numpy as np
from functools import wraps

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE   = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

RANDOM_STATE  = 42
TEST_SIZE     = 0.20
TARGET_COL    = "time_taken_min"

ID_COLS  = ["order_id", "customer_id", "restaurant_id", "rider_id", "order_timestamp"]
CAT_COLS = ["order_type", "vehicle_type", "weather_condition", "time_bucket"]

GEO_COLS     = ["distance_km", "zone_density_score", "route_complexity_score",
                "restaurant_latitude", "restaurant_longitude",
                "customer_latitude", "customer_longitude"]
TIME_COLS    = ["hour_of_day", "day_of_week", "is_weekend", "is_peak_hour"]
ORDER_COLS   = ["order_complexity_score", "estimated_prep_time", "items_count"]
RIDER_COLS   = ["rider_age", "rider_rating", "rider_experience_score",
                "rider_active_orders", "rider_idle_time", "vehicle_speed_score"]
TRAFFIC_COLS = ["traffic_level", "road_congestion_score", "signal_density",
                "average_road_speed"]
WEATHER_COLS = ["weather_severity_score", "rain_flag"]
OPS_COLS     = ["active_orders_nearby", "rider_supply_demand_ratio",
                "restaurant_queue_length", "batch_delivery_flag",
                "zone_demand_score", "delivery_hotspot_flag"]

ALL_NUMERIC_FEATURES = (
    GEO_COLS + TIME_COLS + ORDER_COLS +
    RIDER_COLS + TRAFFIC_COLS + WEATHER_COLS + OPS_COLS
)

# Paths
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH    = os.path.join(BASE_DIR, "eta_model.pkl")
SCALER_PATH   = os.path.join(BASE_DIR, "scaler.pkl")
ENCODER_PATH  = os.path.join(BASE_DIR, "encoders.pkl")
PIPELINE_PATH = os.path.join(BASE_DIR, "pipeline.pkl")
REPORTS_DIR   = os.path.join(BASE_DIR, "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = get_logger("timer")
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        log.info(f"{fn.__name__} completed in {time.perf_counter()-t0:.2f}s")
        return result
    return wrapper


def haversine_vectorised(lat1, lon1, lat2, lon2):
    """Vectorised Haversine distance (km)."""
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi    = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return R * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2)))