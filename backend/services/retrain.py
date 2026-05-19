from backend.database.db import SessionLocal
from backend.models import Feedback
from ml.train_model import train_model

def check_and_retrain():

    db = SessionLocal()
    count = db.query(Feedback).count()

    if count % 20 == 0:
        train_model()
        print("MODEL RETRAINED")