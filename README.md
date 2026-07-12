# 💳 Fraud Screening Console

A lightweight Flask-based web application that uses a **Logistic Regression** model to detect fraudulent credit card transactions in real time.

Users can manually enter transaction details or load sample transactions through an intuitive web interface. The application instantly predicts whether a transaction is **Fraudulent** or **Legitimate** and displays the corresponding fraud probability.

---

# ✨ Features

* Real-time fraud prediction
* Logistic Regression machine learning model
* Clean and responsive web interface
* REST API for predictions
* Automatic model training at application startup
* Automatic synthetic dataset generation if the original dataset is unavailable
* Works with the Kaggle Credit Card Fraud Detection dataset

---

# 📂 Project Structure

```text
webapp/
│
├── app.py                 # Flask backend and ML model
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Frontend HTML
│
├── static/
│   ├── css/
│   │   └── style.css      # Application styling
│   │
│   └── js/
│       └── main.js        # Frontend JavaScript
│
└── creditcard.csv         # Kaggle dataset (optional)
```

---

# 📊 Dataset

The application is designed to use the **Credit Card Fraud Detection** dataset available on Kaggle.

**Download the dataset:**

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Place the downloaded **`creditcard.csv`** file inside the `webapp` directory.

If the dataset is not found, the application automatically creates a synthetic dataset with the same feature schema, allowing the project to run without additional setup. For accurate predictions and evaluation, it is recommended to use the original Kaggle dataset.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/fraud-screening-console.git

cd fraud-screening-console/webapp
```

---

## 2. Create a virtual environment (Recommended)

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the application

```bash
python app.py
```

---

## 5. Open the application

Visit the following URL in your browser:

```text
http://127.0.0.1:5000
```

---

# 🔌 API Endpoints

## Home Page

```http
GET /
```

Returns the main web interface.

---

## Model Information

```http
GET /api/meta
```

Returns model information, including:

* Model accuracy
* Class distribution
* Sample transactions
* Dataset statistics

---

## Fraud Prediction

```http
POST /api/predict
```

### Request Body

```json
{
  "features": {
    "Time": 1000,
    "Amount": 52.30,
    "V1": 0.23,
    "V2": -0.41,
    "...": "..."
  }
}
```

### Response

```json
{
  "label": "fraud",
  "fraud_probability": 0.87
}
```

---

# 🧠 Machine Learning Model

The application uses a **Logistic Regression** classifier trained on the Credit Card Fraud Detection dataset.

### Workflow

1. Load the dataset.
2. Preprocess transaction features.
3. Train the Logistic Regression model.
4. Evaluate model performance.
5. Serve predictions through the Flask API.

---

# 🌐 Deployment

This application is a standard Flask project and can be deployed on any Python hosting platform.

## Render

* Connect your GitHub repository.
* Render automatically detects the Flask application.
* Add **Gunicorn** to `requirements.txt`.
* Set the start command:

```bash
gunicorn app:app
```

---

## Railway

* Connect the GitHub repository.
* Railway automatically installs dependencies.
* Start command:

```bash
gunicorn app:app
```

---

## Fly.io

Deploy using a Dockerfile or the Fly CLI.

---

## PythonAnywhere

* Upload the project files.
* Create a new Flask web application.
* Point the application to `app.py`.

---

## Docker

Create a Docker image using the project directory and `requirements.txt`, then expose the required port.

---

# 🚀 Production Server

Do **not** use Flask's built-in development server in production.

Instead, install **Gunicorn** (Linux/macOS) or **Waitress** (Windows).

### Gunicorn

```bash
pip install gunicorn

gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

### Waitress (Windows)

```bash
pip install waitress

waitress-serve --host=0.0.0.0 --port=8000 app:app
```

---

# 📦 Requirements

* Python 3.9+
* Flask
* NumPy
* Pandas
* Scikit-learn
* Gunicorn (Production)
* Waitress (Windows Production)

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📸 Application Overview

The application provides:

* A modern web interface
* Manual transaction entry
* Sample transaction loading
* Real-time fraud prediction
* Fraud probability visualization
* REST API support

---

# 📄 License

This project is intended for educational and research purposes.

The Credit Card Fraud Detection dataset belongs to its original creators and is available through Kaggle.

---

# 👨‍💻 Author

Developed as a Machine Learning and Flask web application demonstrating real-time credit card fraud detection using Logistic Regression.

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
