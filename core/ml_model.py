import numpy as np
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

# train model from real DB data
def train_model(data):
    X = []
    y = []

    for d in data:
        avg_mood = d['avg_mood']
        negative_count = d['negative_count']
        risk = d['risk']

        X.append([avg_mood, negative_count])

        if risk == "Low":
            y.append(0)
        elif risk == "Moderate":
            y.append(1)
        else:
            y.append(2)

    if len(X) > 0:
        model.fit(X, y)


def predict_risk(avg_mood, negative_count):
    if not hasattr(model, "coef_"):
        return "Moderate"  # fallback

    pred = model.predict([[avg_mood, negative_count]])[0]

    return ["Low", "Moderate", "High"][pred]


def get_recommendation(risk):
    if risk == "High":
        return [
            "Take a break and relax",
            "Talk to someone you trust",
            "Consider professional help"
        ]
    elif risk == "Moderate":
        return [
            "Try meditation",
            "Go for a walk",
            "Reduce screen time"
        ]
    else:
        return [
            "Keep doing what you're doing",
            "Stay active",
            "Maintain healthy habits"
        ]