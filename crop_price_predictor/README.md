# 🌾 Crop Price Predictor

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-Powered Crop Price Prediction System for Farmers**

A modern web application that uses Random Forest machine learning algorithms to predict crop prices based on location, weather patterns, and historical data. Designed to help farmers make informed decisions about crop cultivation and sales timing.

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo Credentials](#-demo-credentials)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### 👨‍🌾 For Farmers
- **Price Prediction**: Get accurate crop price forecasts based on:
  - Commodity type (Jowar, Wheat, Cotton, Sugarcane, Bajra)
  - Location (District)
  - Month and Year
  - Rainfall data
- **Prediction History**: View your past predictions
- **User-Friendly Dashboard**: Clean, intuitive interface
- **Price Range**: Get min, max, and average predicted prices

### 👨‍💼 For Administrators
- **Analytics Dashboard**: View comprehensive statistics
- **User Management**: Track farmer registrations and activity
- **Dataset Upload**: Add new training data via CSV
- **Model Retraining**: Retrain ML models with updated datasets
- **Prediction Logs**: Monitor all predictions system-wide
- **Commodity Analytics**: View crop-wise trends and statistics

### 🎨 Design Highlights
- Modern, responsive UI with Bootstrap 5
- Mobile-friendly design
- Loading animations and spinners
- Real-time form validation
- Print-friendly result pages
- Accessible navigation

---

## 🔑 Demo Credentials

### Farmer Account
- **Username**: `farmer`
- **Password**: `farmer123`

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

> ⚠️ **Important**: Change these credentials in production!

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **SQLite** - Lightweight database for users and predictions
- **Python 3.9+** - Programming language

### Machine Learning
- **scikit-learn** - Random Forest regression models
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation
- **Joblib** - Model serialization

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling
- **Bootstrap 5** - Responsive framework
- **JavaScript (ES6+)** - Interactive features
- **Font Awesome** - Icons
- **Google Fonts (Poppins)** - Typography

### Security
- **Werkzeug** - Password hashing
- **Flask Sessions** - Secure session management

---

## 📥 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download
```bash
git clone https://github.com/Ritikmandal13/Crop-Price-Predictor.git
cd Crop-Price-Predictor/crop_price_predictor
```

Or:
1. Download ZIP from GitHub
2. Extract the folder
3. Navigate to `crop_price_predictor` directory

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python -c "from auth.database import init_db; init_db()"
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start at: **http://127.0.0.1:5000**

---

## 🚀 Usage

### For Farmers

1. **Register an Account**
   - Go to `/register`
   - Fill in your details
   - Choose a username and password

2. **Login**
   - Go to `/login`
   - Select "Farmer" role
   - Enter credentials

3. **Make Prediction**
   - Select commodity from dropdown
   - Enter your district location
   - Choose month and year
   - (Optional) Enter average rainfall
   - Click "Predict Price"

4. **View Results**
   - See predicted price in ₹/quintal
   - View prediction history

### For Administrators

1. **Login as Admin**
   - Go to `/login`
   - Select "Admin" role
   - Use admin credentials

2. **View Dashboard**
   - See total predictions and farmers
   - View recent predictions
   - Check commodity-wise statistics

3. **Upload New Dataset**
   - Go to "Upload Dataset"
   - Select commodity
   - Upload CSV file with required format
   - Click "Upload"

4. **Retrain Model**
   - After uploading dataset
   - Fill in commodity and dataset path
   - Click "Start Retraining"
   - Wait for confirmation

5. **View Logs**
   - Go to "View Logs"
   - See all predictions with details
   - Export data if needed

---

## 📁 Project Structure

```
crop_price_predictor/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment
├── Procfile                    # Deployment configuration
├── .gitignore                  # Git ignore rules
│
├── auth/                       # Authentication module
│   ├── __init__.py
│   └── database.py             # Database initialization & helpers
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── helpers.py              # Helper functions
│   └── ml_handler.py           # ML model management
│
├── model/                      # Pre-trained ML models
│   ├── jmodel.pkl              # Jowar model
│   ├── wmodel.pkl              # Wheat model
│   ├── cmodel.pkl              # Cotton model
│   ├── smodel.pkl              # Sugarcane model
│   ├── bmodel.pkl              # Bajra model
│   └── preprocessor.pkl        # Data preprocessor
│
├── data/                       # Data storage
│   ├── crop_predictor.db       # SQLite database
│   └── uploads/                # Uploaded datasets
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── index.html              # Home page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── farmer_dashboard.html   # Farmer dashboard
│   ├── prediction_result.html  # Prediction result
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── upload_dataset.html     # Dataset upload
│   ├── admin_logs.html         # Prediction logs
│   ├── 404.html                # 404 error page
│   └── 500.html                # 500 error page
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css           # Custom styles
    ├── js/
    │   └── main.js             # JavaScript functions
    └── images/                 # Images (if any)
```

---

## 🌐 Deployment

### Hugging Face Spaces (Recommended)

1. **Create Account**
   - Sign up at [huggingface.co](https://huggingface.co)
   - Create a new Space

2. **Upload Files**
   - Upload all project files
   - Ensure `requirements.txt` and `runtime.txt` are included
   - Make sure model files are under 100MB

3. **Configure Space**
   - Select "Flask" as the SDK
   - Set Python version to 3.9
   - Add environment variables if needed

4. **Deploy**
   - Hugging Face will automatically install dependencies
   - Your app will be live at: `https://huggingface.co/spaces/username/crop-predictor`

### Heroku Deployment

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create crop-price-predictor

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Open app
heroku open
```

### Local Production Server

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or using Flask's production server
export FLASK_ENV=production
flask run --host=0.0.0.0
```

---

## 📊 Dataset Format

For uploading new datasets, use this CSV format:

```csv
Month,Year,Rainfall,WPI
1,2020,50.5,120.5
2,2020,30.2,121.3
3,2020,45.7,119.8
```

### Column Descriptions:
- **Month**: Numeric (1-12)
- **Year**: Four-digit year (e.g., 2023)
- **Rainfall**: Average rainfall in millimeters
- **WPI**: Wholesale Price Index

---

## 🔌 API Documentation

### Get Available Commodities
```
GET /api/commodities
```

**Response:**
```json
["Jowar", "Wheat", "Cotton", "Sugarcane", "Bajra"]
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 👨‍💻 Developer

This project is open-source and available for agricultural research and development.

---

## 🙏 Acknowledgments

- Based on research paper: [Crop Price Prediction Using Random Forest](https://internationalpubls.com/index.php/cana/article/view/762)
- Original contributors: Onkar Waghmode, Shripad Wattamwar, Atharva Wagh, Aditya Zite
- Bootstrap team for the amazing framework
- scikit-learn community for ML tools

---

## 📞 Support

For support, email your.email@example.com or create an issue in the repository.

---

## 🔮 Future Enhancements

- [ ] Add more crops (Rice, Maize, etc.)
- [ ] Integrate real-time weather API
- [ ] Multi-language support (Hindi, Marathi)
- [ ] Mobile app (React Native)
- [ ] SMS/WhatsApp notifications
- [ ] Market trend visualization
- [ ] Export reports as PDF
- [ ] Crop recommendation system
- [ ] Blockchain for price transparency

---

<div align="center">

**Made with ❤️ for Indian Farmers**

⭐ Star this repo if you find it helpful!

</div>

