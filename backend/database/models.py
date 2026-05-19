from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from backend.database.db import Base


class ETAPrediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    # location data
    restaurant_latitude = Column(Float)
    restaurant_longitude = Column(Float)
    customer_latitude = Column(Float)
    customer_longitude = Column(Float)

    # order data
    order_type = Column(String)
    vehicle_type = Column(String)
    rider_name = Column(String)

    rider_age = Column(Integer)
    rider_rating = Column(Float)

    traffic_level = Column(Integer, default=5)
    weather_condition = Column(String, default="Clear")

    # ML outputs
    predicted_eta = Column(Float)
    actual_eta = Column(Float, nullable=True)

    feedback_provided = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, nullable=False)

    actual_eta = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)