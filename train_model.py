import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("sepsis.csv")

features = ["HR", "SBP", "Temp", "Resp"]

# Convert 6 time steps into one row
def create_sequences(df, steps=6):
    X, y = [], []
    for i in range(len(df) - steps):
        seq = df[features].iloc[i:i+steps].values.flatten()
        X.append(seq)
        y.append(df["Sepsis"].iloc[i+steps])
    return np.array(X), np.array(y)

X, y = create_sequences(df)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save model
joblib.dump(model, "sepsis_model.pkl")

print("Model trained successfully!")