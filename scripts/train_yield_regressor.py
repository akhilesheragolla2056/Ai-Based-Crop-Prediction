# Sample script: Merge yield dataset and train a regression model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load your crop recommendation data
rec_df = pd.read_csv("data/raw/Crop recommendation dataset.csv")

# Load a yield dataset (replace with your actual file)
yield_df = pd.read_csv(
    "data/raw/crop_yield_with_features.csv"
)  # <-- Download and place a real dataset here

# Merge on common columns (e.g., crop, region, season)
merged = pd.merge(rec_df, yield_df, on=["crop", "region", "season"], how="inner")

# Select features and target
y = merged["yield"]  # Actual yield column name may vary
X = merged.drop(["yield"], axis=1)

# Convert categorical columns to numeric (if needed)
X = pd.get_dummies(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R^2: {r2:.2f}")

# Save model if needed
# import joblib
# joblib.dump(model, 'artifacts/models/yield_regressor.joblib')

# Note: Replace file paths and column names as per your actual datasets.
# Download a real yield dataset and place it at data/raw/crop_yield_with_features.csv for this script to work.
