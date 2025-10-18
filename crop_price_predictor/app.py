"""
Crop Price Predictor - Main Flask Application
Author: Ritikraj Mandal
Description: Web application for predicting crop prices using Random Forest ML models
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime
import pandas as pd
import json

# Import custom modules
from auth.database import init_db, get_db
from utils.ml_handler import MLModelHandler
from utils.helpers import allowed_file, get_current_year
from utils.crop_recommendation import crop_recommender
from utils.price_visualization import price_visualizer

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_db()

# Initialize ML Model Handler
ml_handler = MLModelHandler()

# ==================== DECORATORS ====================

def login_required(f):
    """Decorator to protect routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to protect admin-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('farmer_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for both Admin and Farmer"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # 'admin' or 'farmer'
        
        db = get_db()
        cursor = db.cursor()
        
        # Query user from database
        cursor.execute(
            'SELECT id, username, password_hash, role FROM users WHERE username = ? AND role = ?',
            (username, role)
        )
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            # Login successful
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect based on role
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('farmer_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for new farmers"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        location = request.form.get('location')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username already exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))
        
        # Insert new farmer
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, full_name, location) VALUES (?, ?, ?, ?, ?)',
            (username, password_hash, 'farmer', full_name, location)
        )
        db.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    username = session.get('username')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('index'))

# ==================== FARMER ROUTES ====================

@app.route('/farmer/dashboard')
@login_required
def farmer_dashboard():
    """Farmer dashboard - predict crop prices"""
    if session.get('role') != 'farmer':
        return redirect(url_for('admin_dashboard'))
    
    # Get available commodities and locations
    commodities = ml_handler.get_available_commodities()
    
    # Get farmer's prediction history
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''SELECT commodity, location, predicted_price, prediction_date 
           FROM predictions 
           WHERE user_id = ? 
           ORDER BY prediction_date DESC 
           LIMIT 10''',
        (session['user_id'],)
    )
    history = cursor.fetchall()
    
    return render_template('farmer_dashboard.html', 
                         commodities=commodities, 
                         history=history)

@app.route('/farmer/predict', methods=['POST'])
@login_required
def predict_price():
    """Handle price prediction request"""
    if session.get('role') != 'farmer':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get form data
        commodity = request.form.get('commodity')
        location = 'Maharashtra'  # Default to state-level since predictions are state-wide
        
        # Handle optional rainfall field - default to 100 if empty
        rainfall_input = request.form.get('rainfall', '100').strip()
        rainfall = float(rainfall_input) if rainfall_input else 100.0
        
        month = int(request.form.get('month', datetime.now().month))
        year = int(request.form.get('year', datetime.now().year))
        
        # Make prediction
        prediction = ml_handler.predict(commodity, location, month, year, rainfall)
        
        if prediction['success']:
            # Save prediction to database
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO predictions 
                   (user_id, commodity, location, rainfall, month, year, predicted_price) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (session['user_id'], commodity, location, rainfall, month, year, 
                 prediction['predicted_price'])
            )
            db.commit()
            
            flash(f"Prediction successful! Price: ₹{prediction['predicted_price']:.2f} per quintal", 'success')
            return redirect(url_for('prediction_result', 
                                  commodity=commodity, 
                                  location=location, 
                                  price=prediction['predicted_price']))
        else:
            flash(f"Prediction failed: {prediction['error']}", 'danger')
            return redirect(url_for('farmer_dashboard'))
            
    except Exception as e:
        flash(f'Error making prediction: {str(e)}', 'danger')
        return redirect(url_for('farmer_dashboard'))

@app.route('/farmer/result')
@login_required
def prediction_result():
    """Display prediction result"""
    commodity = request.args.get('commodity')
    location = request.args.get('location')
    price = float(request.args.get('price'))
    
    return render_template('prediction_result.html', 
                         commodity=commodity, 
                         location=location, 
                         price=price)

# ==================== CROP RECOMMENDATION ROUTES ====================

@app.route('/farmer/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    """Crop recommendation page"""
    if session.get('role') != 'farmer':
        return redirect(url_for('admin_dashboard'))
    
    recommendations = None
    
    if request.method == 'POST':
        soil_type = request.form.get('soil_type')
        rainfall = float(request.form.get('rainfall', 500))
        temperature = float(request.form.get('temperature', 25))
        season = request.form.get('season', 'Kharif')
        
        recommendations = crop_recommender.recommend_crops(
            soil_type, rainfall, temperature, season
        )
    
    return render_template('crop_recommendation.html', 
                         recommendations=recommendations)

# ==================== PRICE HISTORY & VISUALIZATION ROUTES ====================

@app.route('/farmer/price-history/<commodity>')
@login_required
def price_history(commodity):
    """Display historical price trends for a commodity"""
    try:
        # Generate charts
        trend_chart = price_visualizer.create_historical_trend_chart(commodity)
        seasonal_chart = price_visualizer.create_seasonal_pattern_chart(commodity)
        comparison_chart = price_visualizer.create_year_comparison_chart(commodity)
        
        return render_template('price_history.html',
                             commodity=commodity,
                             trend_chart=trend_chart,
                             seasonal_chart=seasonal_chart,
                             comparison_chart=comparison_chart)
    except Exception as e:
        flash(f'Error loading price history: {str(e)}', 'danger')
        return redirect(url_for('farmer_dashboard'))

@app.route('/farmer/price-forecast/<commodity>')
@login_required
def price_forecast(commodity):
    """Display price forecast for next 6 months"""
    try:
        # Generate forecast chart
        forecast_chart = price_visualizer.create_future_forecast_chart(commodity, months_ahead=6)
        predictions = price_visualizer.predict_future_prices(commodity, months_ahead=6)
        
        return render_template('price_forecast.html',
                             commodity=commodity,
                             forecast_chart=forecast_chart,
                             predictions=predictions)
    except Exception as e:
        flash(f'Error generating forecast: {str(e)}', 'danger')
        return redirect(url_for('farmer_dashboard'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics"""
    db = get_db()
    cursor = db.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM predictions')
    total_predictions = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "farmer"')
    total_farmers = cursor.fetchone()[0]
    
    # Get recent predictions
    cursor.execute(
        '''SELECT p.commodity, p.location, p.predicted_price, p.prediction_date, u.username
           FROM predictions p
           JOIN users u ON p.user_id = u.id
           ORDER BY p.prediction_date DESC
           LIMIT 20'''
    )
    recent_predictions = cursor.fetchall()
    
    # Get commodity-wise statistics
    cursor.execute(
        '''SELECT commodity, COUNT(*) as count, AVG(predicted_price) as avg_price
           FROM predictions
           GROUP BY commodity
           ORDER BY count DESC'''
    )
    commodity_stats = cursor.fetchall()
    
    return render_template('admin_dashboard.html',
                         total_predictions=total_predictions,
                         total_farmers=total_farmers,
                         recent_predictions=recent_predictions,
                         commodity_stats=commodity_stats)

@app.route('/admin/upload-dataset', methods=['GET', 'POST'])
@admin_required
def upload_dataset():
    """Upload new dataset"""
    if request.method == 'POST':
        if 'dataset' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(request.url)
        
        file = request.files['dataset']
        commodity = request.form.get('commodity')
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{commodity}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            flash(f'Dataset uploaded successfully: {filename}', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file type. Please upload CSV files only.', 'danger')
    
    return render_template('upload_dataset.html', 
                         commodities=ml_handler.get_available_commodities())

@app.route('/admin/retrain-model', methods=['POST'])
@admin_required
def retrain_model():
    """Retrain ML model with new data"""
    try:
        commodity = request.form.get('commodity')
        dataset_path = request.form.get('dataset_path')
        
        result = ml_handler.retrain_model(commodity, dataset_path)
        
        if result['success']:
            flash(f"Model retrained successfully for {commodity}! Accuracy: {result['accuracy']:.2f}%", 'success')
        else:
            flash(f"Model retraining failed: {result['error']}", 'danger')
            
    except Exception as e:
        flash(f'Error retraining model: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view-logs')
@admin_required
def view_logs():
    """View all prediction logs"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute(
        '''SELECT p.id, u.username, p.commodity, p.location, p.predicted_price, 
                  p.rainfall, p.month, p.year, p.prediction_date
           FROM predictions p
           JOIN users u ON p.user_id = u.id
           ORDER BY p.prediction_date DESC'''
    )
    logs = cursor.fetchall()
    
    return render_template('admin_logs.html', logs=logs)

# ==================== API ROUTES ====================

@app.route('/api/commodities')
def get_commodities():
    """API endpoint to get available commodities"""
    return jsonify(ml_handler.get_available_commodities())

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

