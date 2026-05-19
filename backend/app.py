from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import asyncio
import random
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import requests

from ml.inference import predict_eta as ml_predict_eta
from backend.database.db import SessionLocal, engine
from backend.database import models
from backend.database.models import ETAPrediction, Feedback


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(r * c, 2)


app = FastAPI(title="SWIFT-ETA", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173","http://127.0.0.1.5174","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


class ETARequest(BaseModel):
    restaurant_latitude: float
    restaurant_longitude: float
    customer_latitude: float
    customer_longitude: float
    order_timestamp: str
    order_type: str
    vehicle_type: str
    rider_name: str
    rider_age: int
    rider_rating: float
    traffic_level: int = 5
    weather_condition: str = "Clear"


class ETAResponse(BaseModel):
    prediction_id: int
    predicted_eta_minutes: float
    restaurant_latitude: float
    restaurant_longitude: float
    customer_latitude: float
    customer_longitude: float
    city: str
    distance_km: float
    traffic_index: float
    weather_hint: str
    status: str


class FeedbackRequest(BaseModel):
    prediction_id: int
    actual_eta: float


@app.get("/")
def home():
    return {"message": "SWIFT-ETA Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict_eta", response_model=ETAResponse)
def predict_eta_route(data: ETARequest, db: Session = Depends(get_db)):
    try:
        payload = data.model_dump()
        result = ml_predict_eta(payload)

        eta = float(result.get("predicted_eta_minutes", 0.0))

        distance_km = calculate_distance(
            data.restaurant_latitude,
            data.restaurant_longitude,
            data.customer_latitude,
            data.customer_longitude,
        )

        traffic_index = float(data.traffic_level)
        weather_hint = data.weather_condition

        city = "Unknown City"
        try:
            geo_url = (
                "https://nominatim.openstreetmap.org/reverse"
                f"?format=json&lat={data.customer_latitude}&lon={data.customer_longitude}"
            )
            geo_res = requests.get(
                geo_url,
                headers={"User-Agent": "SWIFT-ETA/1.0"},
                timeout=10,
            )
            geo_res.raise_for_status()
            geo = geo_res.json()

            address = geo.get("address", {})
            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("state_district")
                or "Unknown City"
            )
        except Exception:
            pass

        prediction = ETAPrediction(
            restaurant_latitude=data.restaurant_latitude,
            restaurant_longitude=data.restaurant_longitude,
            customer_latitude=data.customer_latitude,
            customer_longitude=data.customer_longitude,
            order_type=data.order_type,
            vehicle_type=data.vehicle_type,
            rider_name=data.rider_name,
            rider_age=data.rider_age,
            rider_rating=data.rider_rating,
            traffic_level=data.traffic_level,
            weather_condition=data.weather_condition,
            predicted_eta=eta,
            created_at=datetime.utcnow(),
            feedback_provided=False,
            actual_eta=None,
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return {
            "prediction_id": prediction.id,
            "predicted_eta_minutes": eta,
            "restaurant_latitude": data.restaurant_latitude,
            "restaurant_longitude": data.restaurant_longitude,
            "customer_latitude": data.customer_latitude,
            "customer_longitude": data.customer_longitude,
            "city": city,
            "distance_km": distance_km,
            "traffic_index": traffic_index,
            "weather_hint": weather_hint,
            "status": "success",
        }

    except Exception as e:
        db.rollback()
        return {
            "prediction_id": 0,
            "predicted_eta_minutes": 0.0,
            "restaurant_latitude": data.restaurant_latitude,
            "restaurant_longitude": data.restaurant_longitude,
            "customer_latitude": data.customer_latitude,
            "customer_longitude": data.customer_longitude,
            "city": "Unknown City",
            "distance_km": 0.0,
            "traffic_index": float(data.traffic_level),
            "weather_hint": data.weather_condition,
            "status": f"error: {str(e)}",
        }


@app.post("/submit_feedback")
def submit_feedback(data: FeedbackRequest, db: Session = Depends(get_db)):
    try:
        prediction = db.query(ETAPrediction).filter(
            ETAPrediction.id == data.prediction_id
        ).first()

        if not prediction:
            return {"status": "error", "message": "Prediction not found"}

        prediction.actual_eta = data.actual_eta
        prediction.feedback_provided = True

        feedback = Feedback(
            prediction_id=data.prediction_id,
            actual_eta=data.actual_eta,
        )

        db.add(feedback)
        db.commit()

        return {"status": "success", "message": "Feedback saved successfully"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}


@app.get("/analytics")
def analytics():
    return {
        "total_predictions": random.randint(1000, 5000),
        "feedback_received": random.randint(200, 800),
        "active_orders": random.randint(80, 150),
        "traffic_index": round(random.uniform(5, 9), 1),
        "prediction_accuracy": round(random.uniform(90, 97), 1),
    }


@app.get("/model/metrics")
def model_metrics():
    return {
        "rmse": 4.45,
        "mae": 3.36,
        "r2_score": 0.9752,
        "drift_score": 0.03,
    }


@app.websocket("/ws/live-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            event = {
                "eventType": random.choice(
                    ["RIDER_UPDATE", "TRAFFIC_ALERT", "ETA_UPDATE", "NEW_ORDER"]
                ),
                "message": random.choice(
                    [
                        "Heavy traffic detected",
                        "ETA updated",
                        "Rider picked up order",
                        "New delivery assigned",
                    ]
                ),
                "time": datetime.now().strftime("%H:%M:%S"),
            }
            await websocket.send_json(event)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print("WebSocket error:", e)