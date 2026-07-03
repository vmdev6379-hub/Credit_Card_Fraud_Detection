# Fraud Screening Console

A small web app that puts the Credit Card Fraud Detection Logistic
Regression model behind a browser UI. Enter (or load a sample) transaction,
and it returns a fraud probability in real time.

## Run it locally

```bash
cd webapp
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

By default it looks for `creditcard.csv` (the Kaggle "Credit Card Fraud
Detection" dataset) in this folder. If it isn't there, the app automatically
generates a synthetic dataset with the same schema so everything still works
out of the box — download the real dataset from
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud and drop it in this
folder for real results.

## What's inside

```
webapp/
├── app.py              Flask backend: trains the model at startup,
│                        serves the page, and exposes /api/predict
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/main.js
```

- `GET /`            — the web page
- `GET /api/meta`    — model metrics, class balance, and sample transactions (JSON)
- `POST /api/predict`— body `{"features": {"Time":.., "Amount":.., "V1":.., ...}}` → `{"label": "fraud"|"normal", "fraud_probability": 0.87}`

## Putting it online

This is a standard Flask app, so any Python host works:

- **Render / Railway / Fly.io** — connect the repo, they auto-detect Flask.
  Set the start command to `gunicorn app:app` (add `gunicorn` to
  `requirements.txt` first).
- **PythonAnywhere** — upload the folder and point a web app at `app.py`.
- **Docker** — wrap it in a container with the `requirements.txt` and expose
  port 5000, then deploy that image anywhere that runs containers.

For production, don't use `python app.py` directly (that's Flask's dev
server) — run it behind `gunicorn` or `waitress` instead:

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```
