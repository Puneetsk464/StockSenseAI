import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


# -----------------------------
# Generate Synthetic Dataset
# -----------------------------

def generate_dataset(n_samples=5000):

    np.random.seed(42)

    age = np.random.randint(18, 70, n_samples)
    income = np.random.randint(200000, 3000000, n_samples)
    corpus = np.random.randint(50000, 5000000, n_samples)
    horizon = np.random.randint(3, 120, n_samples)
    appetite = np.random.randint(1, 6, n_samples)

    # create synthetic risk score
    risk_score = (
        (1 - age / 70) * 0.25 +
        (income / 3000000) * 0.20 +
        (corpus / 5000000) * 0.15 +
        (horizon / 120) * 0.20 +
        (appetite / 5) * 0.20
    )

    risk_score = np.clip(risk_score, 0, 1)

    df = pd.DataFrame({
        "age": age,
        "income": income,
        "corpus": corpus,
        "horizon": horizon,
        "risk_appetite": appetite,
        "risk_score": risk_score
    })

    return df


# -----------------------------
# Train Model
# -----------------------------

def train_model():

    df = generate_dataset()

    X = df.drop("risk_score", axis=1)
    y = df["risk_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)

    joblib.dump(model, "models/risk_model.pkl")

    print("Risk model trained and saved.")


if __name__ == "__main__":
    train_model()