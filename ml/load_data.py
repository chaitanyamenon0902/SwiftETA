import pandas as pd
from backend.db.database import SessionLocal
from backend.db.models import ETAFeedback

def load_training_data():
    db = SessionLocal()

    rows = db.query(ETAFeedback).all()

    data = []
    for r in rows:
        data.append({
            "driver_lat": r.driver_lat,
            "driver_lng": r.driver_lng,
            "restaurant_lat": r.restaurant_lat,
            "restaurant_lng": r.restaurant_lng,
            "traffic_level": r.traffic_level,
            "weather_condition": r.weather_condition,
            "order_timestamp": r.order_timestamp,
            "actual_eta": r.actual_eta
        })

    return pd.DataFrame(data)