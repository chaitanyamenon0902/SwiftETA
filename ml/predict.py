import pandas as pd
import joblib

from ml.feature_engineering import run_feature_engineering
from ml.utils import PIPELINE_PATH

# ----------------------------------------
# LOAD TRAINED PIPELINE
# ----------------------------------------

pipeline = joblib.load(PIPELINE_PATH)

# ----------------------------------------
# PREDICTION FUNCTION
# ----------------------------------------

def predict_eta(input_data: dict):

    # Convert to dataframe
    df = pd.DataFrame([input_data])

    # Run feature engineering
    df = run_feature_engineering(df)

    # Predict
    prediction = pipeline.predict(df)[0]

    return {
        "predicted_eta_minutes": round(float(prediction), 2)
    }


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    sample_input = {

        "restaurant_latitude": 12.9716,
        "restaurant_longitude": 77.5946,

        "customer_latitude": 12.9352,
        "customer_longitude": 77.6245,

        "order_timestamp": "2026-05-16 19:30:00",

        "order_type": "Buffet",
        "vehicle_type": "Bike",

        "rider_age": 28,
        "rider_rating": 4.7,

        "traffic_level": 8,
        "weather_condition": "Rainy"
    }

    result = predict_eta(sample_input)

    print(result)