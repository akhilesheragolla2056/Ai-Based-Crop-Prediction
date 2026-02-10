# Utility functions for yield data filtering and model training
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

CROP_YIELD_CSV = "data/raw/crop_yield.csv"
MODEL_PATH = "artifacts/models/yield_regressor.joblib"


def filter_yield_data(crop=None, state=None, season=None, year=None):
    df = pd.read_csv(CROP_YIELD_CSV)
    if crop:
        df = df[df["Crop"].str.lower() == crop.lower()]
    if state:
        df = df[df["State"].str.lower() == state.lower()]
    if season:
        df = df[df["Season"].str.lower().str.strip() == season.lower().strip()]
    if year:
        df = df[df["Crop_Year"] == int(year)]
    return df


def train_yield_model():
    df = pd.read_csv(CROP_YIELD_CSV)
    # Features: Crop, Season, State, Rainfall, Fertilizer, Pesticide
    features = ["Crop", "Season", "State", "Annual_Rainfall", "Fertilizer", "Pesticide"]
    X = df[features]
    y = df["Yield"]
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.2f}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"R^2: {r2_score(y_test, y_pred):.2f}")
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return model


def predict_yield(crop, state, season, rainfall, fertilizer, pesticide):
    import joblib

    model = joblib.load(MODEL_PATH)
    # Prepare input as DataFrame with same columns as training
    input_df = pd.DataFrame(
        [
            {
                "Crop": crop,
                "Season": season,
                "State": state,
                "Annual_Rainfall": rainfall,
                "Fertilizer": fertilizer,
                "Pesticide": pesticide,
            }
        ]
    )
    input_df = pd.get_dummies(input_df)
    # Align columns with model
    model_cols = (
        joblib.load(MODEL_PATH.replace(".joblib", "_cols.joblib"))
        if os.path.exists(MODEL_PATH.replace(".joblib", "_cols.joblib"))
        else None
    )
    if model_cols is not None:
        for col in model_cols:
            if col not in input_df:
                input_df[col] = 0
        input_df = input_df[model_cols]
    return model.predict(input_df)[0]


# Save columns for prediction alignment after training
if __name__ == "__main__":
    model = train_yield_model()
    import joblib

    df = pd.read_csv(CROP_YIELD_CSV)
    features = ["Crop", "Season", "State", "Annual_Rainfall", "Fertilizer", "Pesticide"]
    X = pd.get_dummies(df[features])
    joblib.dump(list(X.columns), MODEL_PATH.replace(".joblib", "_cols.joblib"))
