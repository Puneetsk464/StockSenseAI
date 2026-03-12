import joblib
import pandas as pd
import logging

logger = logging.getLogger(__name__)

model = joblib.load("models/risk_model.pkl")


def predict_risk(age, income, corpus, horizon_months, risk_appetite):

    X = pd.DataFrame([{
        "age": age,
        "income": income,
        "corpus": corpus,
        "horizon": horizon_months,
        "risk_appetite": risk_appetite
    }])

    model_risk_score = model.predict(X)[0]

    # Blend model prediction with direct risk_appetite scaling
    # Model gives 50% weight, risk_appetite scaling gives 50% weight
    model_weight = 0.5
    appetite_weight = 0.5

    # Normalize risk_appetite (1-5 scale → 0-1 scale)
    normalized_appetite = (risk_appetite - 1) / 4.0  # Maps 1→0, 5→1
    normalized_appetite = max(0, min(1, normalized_appetite))  # Clamp to 0-1

    # Blend the two signals for better differentiation
    blended_risk_score = (model_weight * model_risk_score) + \
        (appetite_weight * normalized_appetite)

    logger.debug(
        f"Risk calculation: model={model_risk_score:.4f}, appetite_normalized={normalized_appetite:.4f}, blended={blended_risk_score:.4f}")

    return float(blended_risk_score)


def risk_category(score):

    if score < 0.3:
        return "Conservative"
    elif score < 0.6:
        return "Moderate"
    elif score < 0.8:
        return "Growth"
    else:
        return "Aggressive"
