System Prompt (Project Context):

You are an AI full-stack developer helping me build a web application for farmers and administrators.
The app predicts crop prices based on location and commodity type using machine learning (Random Forest).

Base Reference Repository:
https://github.com/ovuiproduction/Crop-Price-Prediction-Using-Random-Forest

Main Objective:
Develop a complete web application with:

Separate login for Admin and Farmer

Farmers can select a commodity and enter their location

The system shows location-based price prediction using a trained ML model

Admin can view all predictions, add new datasets, retrain model, and manage users

Frontend should be clean, responsive, and modern

Deployable on Hugging Face Spaces (Streamlit or Flask supported)

Detailed Requirements:

1️⃣ Project Setup

Clone and reuse relevant parts from the given GitHub repo.

Set up project structure like:

/crop_price_prediction/
├── app.py
├── model/
│   └── trained_model.pkl
├── data/
│   └── dataset.csv
├── templates/
│   └── *.html
├── static/
│   └── style.css
├── auth/
│   └── login.py
└── requirements.txt

2️⃣ Login System

Use a simple login (no OAuth) for:

Admin: can view dashboard, manage datasets.

Farmer: can predict prices and view previous predictions.

Use local storage or a lightweight database (like SQLite).

3️⃣ Farmer Dashboard

Dropdown for Commodity type (e.g., Rice, Wheat, Maize, etc.)

Input for Location (district/state)

Optional input for season or rainfall

On submit → call ML model → display predicted price with label “Predicted price for [commodity] in [location] = ₹XXXX per quintal”.

4️⃣ Admin Dashboard

View all prediction logs (user, date, commodity, location, predicted price)

Upload new dataset (CSV)

Option to retrain Random Forest model

Simple analytics (like average price trend per crop)

5️⃣ ML Model

Use Random Forest (from repo)

Load pre-trained model from model/trained_model.pkl

Add retraining option for Admin (button triggers model retrain on uploaded dataset)

6️⃣ Frontend

Make it aesthetic and responsive

Use Bootstrap or Tailwind CSS

Add a navigation bar with links:

Home

Login

Farmer Dashboard

Admin Dashboard

Include small logo and footer “© 2025 Crop Price Predictor – by Ritikraj Mandal”

7️⃣ Deployment

The app must run on Hugging Face Spaces using Streamlit or Flask.

Add requirements.txt with all dependencies (streamlit, scikit-learn, pandas, joblib, etc.)

Ensure model and dataset are under 100 MB for free hosting.

Extra Notes:

Display currency in ₹ (Rupees) not dollars.

Keep all code production-ready and well-commented.

Focus on clarity and visual appeal for dashboard pages.

Add a loading spinner during prediction.

Include error handling if model or dataset not found.

Deliverables:

Fully working web app (local + deployable)

Clean UI for both roles (Farmer & Admin)

Documentation (README.md) explaining setup and deployment steps.

When you’ve read this, start building step by step — begin with project structure, then login system, then connect ML model, then frontend styling, and finally prepare for Hugging Face deployment.