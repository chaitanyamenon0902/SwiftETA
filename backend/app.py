from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from ml.predict import predict_eta

import asyncio
import random

from datetime import datetime


app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# ROOT ROUTE
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "SWIFT-ETA Backend Running"
    }

# -----------------------------------
# HEALTH ROUTE
# -----------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# -----------------------------------
# ANALYTICS ROUTE
# -----------------------------------

@app.get("/analytics")
def analytics():

    return {
        "avg_eta": 28.4,
        "active_orders": 142,
        "delayed_orders": 12,
        "traffic_index": 7.3,
        "prediction_accuracy": 94.2
    }

# -----------------------------------
# MODEL METRICS
# -----------------------------------

@app.get("/model/metrics")
def model_metrics():

    return {
        "rmse": 4.45,
        "mae": 3.36,
        "r2_score": 0.9752,
        "drift_score": 0.03
    }

# -----------------------------------
# REQUEST MODEL
# -----------------------------------

class ETARequest(BaseModel):

    restaurant_latitude: float
    restaurant_longitude: float

    customer_latitude: float
    customer_longitude: float

    order_timestamp: str

    order_type: str
    vehicle_type: str

    rider_age: int
    rider_rating: float

    traffic_level: int
    weather_condition: str

# -----------------------------------
# ETA PREDICTION
# -----------------------------------

@app.post("/predict_eta")
def predict(data: ETARequest):

    result = predict_eta(data.dict())

    return result

# -----------------------------------
# WEBSOCKET
# -----------------------------------

@app.websocket("/ws/live-updates")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("WebSocket client connected")

    try:
        while True:

            mock_event = {
                "eventType": random.choice([
                    "RIDER_UPDATE",
                    "TRAFFIC_ALERT",
                    "ETA_UPDATE",
                    "NEW_ORDER"
                ]),

                "message": random.choice([
                    "Heavy traffic detected",
                    "ETA increased to 31 mins",
                    "Rider picked up order",
                    "New delivery assigned"
                ]),

                "time": datetime.now().strftime("%H:%M:%S")
            }

            await websocket.send_json(mock_event)

            await asyncio.sleep(3)

    except Exception as e:

        print("WebSocket disconnected:", e)