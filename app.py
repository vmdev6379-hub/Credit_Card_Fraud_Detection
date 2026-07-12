"""
Fraud Screening Console
========================
A small Flask web app that wraps the Logistic Regression fraud-detection
model from the project in a browser UI.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

RANDOM_STATE = 2
DATA_PATH = "creditcard.csv"
FEATURES = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Data + model, prepared once at startup
# ---------------------------------------------------------------------------
STATE = {}


def load_dataset(path: str = DATA_PATH) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)

    rng = np.random.default_rng(RANDOM_STATE)
    n_normal, n_fraud = 20000, 100
    n_total = n_normal + n_fraud
    time = np.sort(rng.integers(0, 172792, size=n_total))

    normal_v = rng.normal(0.0, 1.0, size=(n_normal, 28))
    normal_amount = np.abs(rng.normal(60, 80, size=n_normal))
    fraud_v = rng.normal(2.5, 2.0, size=(n_fraud, 28))
    fraud_amount = np.abs(rng.normal(120, 250, size=n_fraud))

    v_cols = np.vstack([normal_v, fraud_v])
    amount = np.concatenate([normal_amount, fraud_amount])
    label = np.concatenate([np.zeros(n_normal), np.ones(n_fraud)])

    df = pd.DataFrame(v_cols, columns=[f"V{i}" for i in range(1, 29)])
    df.insert(0, "Time", time)
    df["Amount"] = amount
    df["Class"] = label.astype(int)
    return df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)


def build_state():
    df = load_dataset()
    is_synthetic = not os.path.exists(DATA_PATH)

    normal = df[df.Class == 0]
    fraud = df[df.Class == 1]

    normal_sample = normal.sample(n=min(len(fraud), len(normal)), random_state=RANDOM_STATE)
    balanced = pd.concat([normal_sample, fraud], axis=0).sample(frac=1, random_state=RANDOM_STATE)

    X = balanced[FEATURES]
    Y = balanced["Class"]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y, random_state=RANDOM_STATE
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_s, Y_train)

    pred = model.predict(X_test_s)
    metrics = {
        "accuracy": round(float(accuracy_score(Y_test, pred)), 4),
        "precision": round(float(precision_score(Y_test, pred)), 4),
        "recall": round(float(recall_score(Y_test, pred)), 4),
        "f1": round(float(f1_score(Y_test, pred)), 4),
    }
    cm = confusion_matrix(Y_test, pred).tolist()

    # a handful of sample transactions for the "load sample" / ticker features
    samples = []
    for cls, label in [(0, "normal"), (1, "fraud")]:
        rows = df[df.Class == cls].sample(n=6, random_state=RANDOM_STATE)
        for _, row in rows.iterrows():
            samples.append({
                "label": label,
                "features": {f: round(float(row[f]), 4) for f in FEATURES},
            })

    STATE.update(dict(
        df=df, model=model, scaler=scaler, metrics=metrics, confusion_matrix=cm,
        samples=samples, is_synthetic=is_synthetic,
        class_counts={"normal": int((df.Class == 0).sum()), "fraud": int((df.Class == 1).sum())},
    ))


build_state()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        metrics=STATE["metrics"],
        class_counts=STATE["class_counts"],
        is_synthetic=STATE["is_synthetic"],
        features=FEATURES,
    )


@app.route("/api/meta")
def api_meta():
    return jsonify({
        "metrics": STATE["metrics"],
        "confusion_matrix": STATE["confusion_matrix"],
        "class_counts": STATE["class_counts"],
        "is_synthetic": STATE["is_synthetic"],
        "samples": STATE["samples"],
        "features": FEATURES,
    })


@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(force=True)
    try:
        row = [float(payload["features"][f]) for f in FEATURES]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Missing or invalid feature values."}), 400

    X = np.array(row).reshape(1, -1)
    X_scaled = STATE["scaler"].transform(X)
    proba = STATE["model"].predict_proba(X_scaled)[0][1]
    label = "fraud" if proba >= 0.5 else "normal"

    return jsonify({"label": label, "fraud_probability": round(float(proba), 4)})


if __name__ == "__main__":
    app.run(debug=True)
