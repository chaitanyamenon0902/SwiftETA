from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.databse.db import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    rider_name = Column(String)
    eta = Column(Float)
    weather = Column(Integer)
    traffic = Column(Integer)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer)
    actual_eta = Column(Float)