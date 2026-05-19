import joblib
import pandas as pd
from ml.feature_engineering import run_feature_engineering

PIPELINE_PATH = "ml/pipeline.pkl"

pipeline = joblib.load(PIPELINE_PATH)


def predict_eta(input_data: dict):

    print("🚀 MODEL PREDICTION TRIGGERED")  # <-- IMPORTANT DEBUG LINE
    # convert request → dataframe
    df = pd.DataFrame([input_data])

    # feature engineering
    df = run_feature_engineering(df)

    # prediction
    prediction = pipeline.predict(df)[0]

    return {
        "predicted_eta_minutes": round(float(prediction), 2)
    }