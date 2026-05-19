import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

from feature_engineering import run_feature_engineering
from ml.utils import (
    TARGET_COL,
    CAT_COLS,
    ALL_NUMERIC_FEATURES,
    MODEL_PATH,
    SCALER_PATH,
    PIPELINE_PATH,
    rmse,
)

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

DATA_PATH = "../food_delivery_eta_dataset.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# ----------------------------------------
# FEATURE ENGINEERING
# ----------------------------------------

print("Running feature engineering...")
df = run_feature_engineering(df)

# ----------------------------------------
# DROP MISSING TARGETS
# ----------------------------------------

df = df.dropna(subset=[TARGET_COL])

# ----------------------------------------
# FEATURES + TARGET
# ----------------------------------------

FEATURES = ALL_NUMERIC_FEATURES + CAT_COLS

X = df[FEATURES]
y = df[TARGET_COL]

# ----------------------------------------
# TRAIN TEST SPLIT
# ----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------------------
# PREPROCESSING
# ----------------------------------------

numeric_transformer = Pipeline(
    steps=[
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, ALL_NUMERIC_FEATURES),
        ("cat", categorical_transformer, CAT_COLS),
    ]
)

# ----------------------------------------
# MODEL
# ----------------------------------------

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    objective="reg:squarederror"
)

# ----------------------------------------
# FULL PIPELINE
# ----------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# ----------------------------------------
# TRAIN
# ----------------------------------------

print("Training model...")
pipeline.fit(X_train, y_train)

# ----------------------------------------
# PREDICT
# ----------------------------------------

preds = pipeline.predict(X_test)

# ----------------------------------------
# METRICS
# ----------------------------------------

mae = mean_absolute_error(y_test, preds)
rmse_score = rmse(y_test, preds)
r2 = r2_score(y_test, preds)

print("\nMODEL PERFORMANCE")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse_score:.2f}")
print(f"R2   : {r2:.4f}")

# ----------------------------------------
# SAVE PIPELINE
# ----------------------------------------

joblib.dump(pipeline, PIPELINE_PATH)

# Save model separately
joblib.dump(model, MODEL_PATH)

# Save scaler separately
scaler = pipeline.named_steps["preprocessor"] \
                 .named_transformers_["num"] \
                 .named_steps["scaler"]

joblib.dump(scaler, SCALER_PATH)

print("\nModel saved successfully!")