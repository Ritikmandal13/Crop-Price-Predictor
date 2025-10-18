# 🌾 Crop Price Prediction Using Random Forest

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-Powered Agricultural Price Prediction Platform**

A modern web application that helps farmers make informed decisions through machine learning-powered crop price predictions, historical analysis, and AI-driven crop recommendations.

---

## 🎯 What This Does

- 📊 **Predict crop prices** using Random Forest ML algorithms
- 📈 **View historical trends** with interactive charts (2012-2018 data)
- 🔮 **Forecast future prices** for the next 6 months
- 🌱 **Get crop recommendations** based on soil, rainfall, and profitability
- 💰 **See actual rupee prices** (₹/quintal), not just index numbers

**Supports:** Jowar, Wheat, Cotton, Sugarcane, Bajra

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ritikmandal13/Crop-Price-Predictor.git
cd Crop-Price-Predictor/crop_price_predictor
```

### 2️⃣ Install & Setup
```bash
pip install -r requirements.txt
python -c "from auth.database import init_db; init_db()"
```

### 3️⃣ Run the App
```bash
python app.py
```

**Open:** http://127.0.0.1:5000

---

## 🔑 Demo Login

| Role | Username | Password |
|------|----------|----------|
| 👨‍🌾 Farmer | `farmer` | `farmer123` |
| 👨‍💼 Admin | `admin` | `admin123` |

---

## ✨ Features

### 🎯 **Core Features**
- ✅ **User Authentication** - Secure login for Admin & Farmer
- ✅ **Price Prediction** - ML-powered forecasting
- ✅ **Historical Charts** - Interactive Plotly visualizations
- ✅ **Price Forecasting** - Next 6 months predictions
- ✅ **Crop Advisor** - Smart recommendations
- ✅ **Weather Integration** - Rainfall & temperature data

### 📊 **Visualizations**
- Long-term price trends (with rainfall overlay)
- Seasonal price patterns
- Year-wise comparisons
- Future price forecasts
- All interactive & responsive!

### 🤖 **AI/ML Features**
- Random Forest regression models
- 5 crop-specific models
- Trend-based forecasting
- Multi-factor crop scoring
- Admin can retrain models

---

## 📂 Project Structure

```
📁 Crop-Price-Prediction-Using-Random-Forest/
│
├── 📁 crop_price_predictor/          ← MAIN APPLICATION
│   ├── 📄 app.py                     Main Flask app (435 lines)
│   ├── 📄 requirements.txt           Dependencies
│   ├── 📄 README.md                  Complete documentation
│   ├── 📄 SETUP_GUIDE.md            Detailed setup instructions
│   ├── 📄 FEATURES_COMPLETE.md      All features list
│   │
│   ├── 📁 auth/                      Authentication system
│   │   └── database.py               SQLite setup
│   │
│   ├── 📁 utils/                     Utility modules
│   │   ├── ml_handler.py             ML model manager
│   │   ├── crop_recommendation.py    Crop advisory
│   │   ├── price_visualization.py    Chart generation
│   │   └── helpers.py                Helper functions
│   │
│   ├── 📁 model/                     Machine Learning
│   │   ├── jmodel.pkl                Jowar model
│   │   ├── wmodel.pkl                Wheat model
│   │   ├── cmodel.pkl                Cotton model
│   │   ├── smodel.pkl                Sugarcane model
│   │   ├── bmodel.pkl                Bajra model
│   │   └── preprocessor.pkl          Data preprocessor
│   │
│   ├── 📁 data/                      Data storage
│   │   ├── *.csv                     Historical datasets (5 crops)
│   │   ├── crop_predictor.db         SQLite database
│   │   └── uploads/                  User uploads
│   │
│   ├── 📁 templates/                 HTML templates (14 files)
│   └── 📁 static/                    CSS & JavaScript
│
└── 📄 plan.md                        SRS Document
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](crop_price_predictor/SETUP_GUIDE.md) | **Step-by-step setup instructions** |
| [README.md](crop_price_predictor/README.md) | Complete project documentation |
| [FEATURES_COMPLETE.md](crop_price_predictor/FEATURES_COMPLETE.md) | All features & requirements |
| [plan.md](plan.md) | Original SRS document |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask, Python 3.9+, SQLite |
| **ML/AI** | scikit-learn (Random Forest), NumPy, Pandas |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Security** | Werkzeug (password hashing), Flask sessions |
| **Deployment** | Gunicorn, Hugging Face Spaces ready |

---

## 📸 Features Overview

### 🎯 **Price Prediction**
Input: Commodity, Month, Year, Rainfall → Output: Price in ₹/quintal

### 📈 **Historical Analysis**
Interactive charts showing:
- 7-year price trends
- Seasonal patterns
- Year-wise comparisons
- Rainfall correlations

### 🔮 **Price Forecasting**
6-month future predictions with confidence levels

### 🌱 **Crop Recommendation**
AI scores crops based on:
- Soil type (7 types)
- Rainfall levels
- Temperature
- Market demand
- Profitability potential

---

## 🔧 Requirements

```
Python >= 3.9
Flask >= 3.0.0
scikit-learn >= 1.4.0
pandas >= 2.1.0
plotly >= 5.18.0
```

See [requirements.txt](crop_price_predictor/requirements.txt) for complete list.

---

## 🌐 Deployment Options

This application can be deployed on:

- ✅ **Hugging Face Spaces** (Recommended - Free tier available)
- ✅ **Heroku** (Easy deployment)
- ✅ **Railway** (Simple & fast)
- ✅ **Render** (Free tier available)
- ✅ **AWS/Azure/GCP** (Production scale)

All configuration files included (Procfile, runtime.txt).

---

## 🐛 Troubleshooting

**Common issues and solutions:**

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port in app.py or kill existing process |
| Module not found | Ensure you're in `crop_price_predictor/` directory |
| Database error | Delete `crop_predictor.db` and reinitialize |
| Models not loading | Check `model/` folder has 6 .pkl files |

**Full troubleshooting guide:** [SETUP_GUIDE.md](crop_price_predictor/SETUP_GUIDE.md#troubleshooting)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- **Research Paper:** [International Publications](https://internationalpubls.com/index.php/cana/article/view/762)
- **Original Research:** Onkar Waghmode, Shripad Wattamwar, Atharva Wagh, Aditya Zite
- **ML Framework:** scikit-learn team
- **UI Framework:** Bootstrap team
- **Charts:** Plotly team

---

## 📊 Project Stats

- **Lines of Code:** ~3,000+
- **Python Modules:** 8
- **HTML Templates:** 14
- **ML Models:** 6
- **Datasets:** 5 crops
- **Historical Data:** 2012-2018 (81 months per crop)

---

## 🔮 Future Enhancements

- [ ] Add more crops (Rice, Maize, Pulses)
- [ ] Real-time weather API integration
- [ ] Multi-state support (Punjab, UP, etc.)
- [ ] Mobile app (React Native)
- [ ] SMS/WhatsApp alerts
- [ ] Multi-language support (Hindi, Marathi)
- [ ] PDF export for predictions
- [ ] Advanced ML models (LSTM, ARIMA)

---

<div align="center">

## 🌾 Made for Indian Farmers 🇮🇳

**Empowering Agriculture Through Technology**

⭐ **Star this repository if you find it useful!** ⭐

[Report Bug](https://github.com/Ritikmandal13/Crop-Price-Predictor/issues) · 
[Request Feature](https://github.com/Ritikmandal13/Crop-Price-Predictor/issues)

</div>

---

**Quick Links:**
- 📖 [Full Documentation](crop_price_predictor/README.md)
- 🚀 [Setup Guide](crop_price_predictor/SETUP_GUIDE.md)
- ✨ [Features List](crop_price_predictor/FEATURES_COMPLETE.md)
- 📋 [SRS Document](plan.md)

