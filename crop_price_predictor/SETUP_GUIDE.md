# 🚀 Complete Setup Guide - Crop Price Predictor

This guide will help you set up the Crop Price Predictor application on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** ([Download here](https://www.python.org/downloads/))
- **Git** (optional, for cloning) ([Download here](https://git-scm.com/downloads))
- **pip** (comes with Python)

---

## 🔧 Installation Steps

### **Step 1: Clone or Download the Repository**

#### Option A: Using Git (Recommended)
```bash
git clone https://github.com/YOUR_USERNAME/Crop-Price-Prediction-Using-Random-Forest.git
cd Crop-Price-Prediction-Using-Random-Forest
```

#### Option B: Download ZIP
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file
4. Navigate to the extracted folder

---

### **Step 2: Navigate to the Application Directory**

```bash
cd crop_price_predictor
```

---

### **Step 3: Create Virtual Environment (Recommended)**

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### **Step 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- scikit-learn (machine learning)
- Plotly (interactive charts)
- And all other required packages

**Wait for installation to complete** (may take 2-5 minutes).

---

### **Step 5: Initialize the Database**

Run the following command to create the SQLite database:

```bash
python -c "from auth.database import init_db; init_db()"
```

You should see: **"✅ Database initialized successfully!"**

This creates:
- Users table
- Predictions table
- Default admin account
- Default farmer account (for testing)

---

### **Step 6: Start the Application**

```bash
python app.py
```

You should see:
```
Loading ML models...
✅ Loaded Jowar model from model\jmodel.pkl
✅ Loaded Wheat model from model\wmodel.pkl
✅ Loaded Cotton model from model\cmodel.pkl
✅ Loaded Sugarcane model from model\smodel.pkl
✅ Loaded Bajra model from model\bmodel.pkl
✅ Database initialized successfully!
 * Running on http://127.0.0.1:5000
```

---

### **Step 7: Access the Application**

Open your web browser and go to:

```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

---

## 🔑 Demo Login Credentials

### Farmer Account:
- **Username:** `farmer`
- **Password:** `farmer123`

### Admin Account:
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **Security Note:** Change these credentials for production use!

---

## ✅ Quick Setup (One Command)

### Windows:
```bash
setup_and_run.bat
```

### macOS/Linux:
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

This script will:
1. Check Python installation
2. Install all dependencies
3. Initialize database
4. Start the application

---

## 🎯 Testing the Application

### **1. Test as Farmer:**
1. Go to login page
2. Select **"Farmer"** role
3. Login with `farmer` / `farmer123`
4. Try making a price prediction:
   - Select crop: **Wheat**
   - Choose month: **October**
   - Enter year: **2025**
   - (Optional) Rainfall: **150**
   - Click **"Predict Price"**
5. View your prediction history
6. Try **"Crop Recommendation"** feature
7. View **"Price History"** charts

### **2. Test as Admin:**
1. Logout (if logged in as farmer)
2. Login with **"Admin"** role
3. Username: `admin` / Password: `admin123`
4. Explore:
   - Dashboard statistics
   - Recent predictions
   - Upload dataset (optional)
   - View all logs

---

## 📊 Project Structure

```
crop_price_predictor/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── setup_and_run.bat        # Windows quick start
├── setup_and_run.sh         # Linux/Mac quick start
│
├── auth/                    # Authentication module
│   ├── database.py          # SQLite database setup
│   └── __init__.py
│
├── utils/                   # Utility modules
│   ├── ml_handler.py        # ML model management
│   ├── crop_recommendation.py  # Crop advisory system
│   ├── price_visualization.py  # Chart generation
│   ├── helpers.py           # Helper functions
│   └── __init__.py
│
├── model/                   # Machine Learning models
│   ├── jmodel.pkl          # Jowar model
│   ├── wmodel.pkl          # Wheat model
│   ├── cmodel.pkl          # Cotton model
│   ├── smodel.pkl          # Sugarcane model
│   ├── bmodel.pkl          # Bajra model
│   └── preprocessor.pkl    # Data preprocessor
│
├── data/                    # Data storage
│   ├── *.csv               # Historical price datasets
│   ├── crop_predictor.db   # SQLite database (created on first run)
│   └── uploads/            # Uploaded datasets
│
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── farmer_dashboard.html
│   ├── admin_dashboard.html
│   └── ... (11 more templates)
│
└── static/                  # Static assets
    ├── css/style.css       # Custom styles
    └── js/main.js          # JavaScript
```

---

## 🛠️ Troubleshooting

### **Problem 1: "Module not found" errors**

**Solution:**
```bash
# Make sure you're in the right directory
cd crop_price_predictor

# Reinstall dependencies
pip install -r requirements.txt
```

---

### **Problem 2: "Address already in use" (Port 5000)**

**Solution:**
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Or change port in app.py:
# port = int(os.environ.get('PORT', 5001))  # Use 5001 instead
```

---

### **Problem 3: scikit-learn installation fails on Windows**

**Solution:**
If you see "Microsoft Visual C++ 14.0 required" error:

1. Use pre-built wheels:
   ```bash
   pip install --upgrade pip
   pip install scikit-learn --only-binary :all:
   ```

2. Or install with conda:
   ```bash
   conda install scikit-learn
   ```

---

### **Problem 4: Database errors**

**Solution:**
```bash
# Delete old database
rm data/crop_predictor.db  # macOS/Linux
del data\crop_predictor.db  # Windows

# Reinitialize
python -c "from auth.database import init_db; init_db()"
```

---

### **Problem 5: Models not loading**

**Solution:**
Check if model files exist:
```bash
# Windows:
dir model\*.pkl

# macOS/Linux:
ls -la model/*.pkl
```

You should see 6 files:
- jmodel.pkl, wmodel.pkl, cmodel.pkl, smodel.pkl, bmodel.pkl, preprocessor.pkl

If missing, re-copy from the original source or retrain.

---

## 🌐 Accessing from Other Devices

To access from other devices on the same network:

1. Find your local IP address:
   ```bash
   # Windows:
   ipconfig
   
   # macOS/Linux:
   ifconfig
   ```

2. Look for IPv4 Address (e.g., 192.168.1.100)

3. On other devices, open:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

---

## 🔐 Security Considerations

### **Before Deploying to Production:**

1. **Change Secret Key:**
   ```python
   # In app.py, change:
   app.config['SECRET_KEY'] = 'your-unique-secret-key-here'
   ```

2. **Change Default Passwords:**
   - Edit `auth/database.py`
   - Change admin and farmer default passwords

3. **Disable Debug Mode:**
   ```python
   # In app.py, change:
   app.run(host='0.0.0.0', port=port, debug=False)
   ```

4. **Use Environment Variables:**
   - Create `.env` file
   - Store sensitive data there
   - Never commit `.env` to GitHub

---

## 📦 Database Schema

### **Users Table:**
```sql
id, username, password_hash, role, full_name, location, created_at
```

### **Predictions Table:**
```sql
id, user_id, commodity, location, rainfall, month, year, predicted_price, prediction_date
```

---

## 🔄 Updating the Application

To get the latest updates:

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies (if changed)
pip install -r requirements.txt

# Restart application
python app.py
```

---

## 📱 Features Available

### **For Farmers:**
- ✅ Price prediction for 5 crops
- ✅ Historical price charts (interactive)
- ✅ 6-month price forecast
- ✅ Crop recommendation system
- ✅ Prediction history

### **For Admins:**
- ✅ Analytics dashboard
- ✅ User management
- ✅ Dataset upload
- ✅ Model retraining
- ✅ Prediction logs

---

## 💡 Tips for Best Experience

1. **Use latest Chrome/Firefox** for best chart rendering
2. **Clear browser cache** if you see old designs
3. **Enable JavaScript** for interactive features
4. **Use desktop/tablet** for admin features (better UX)

---

## 📞 Need Help?

If you encounter issues:

1. Check this troubleshooting guide
2. Review error messages in terminal
3. Check `data/crop_predictor.db` exists
4. Verify all model files are present
5. Ensure port 5000 is not in use

---

## 🎉 You're All Set!

The application should now be running successfully. Enjoy predicting crop prices! 🌾

---

**Last Updated:** October 2025  
**Version:** 1.0.0

