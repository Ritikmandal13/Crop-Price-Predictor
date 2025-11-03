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
from utils.state_config import state_config

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
    
    # Get available commodities and states
    commodities = ml_handler.get_available_commodities()
    states = state_config.get_all_states()
    
    # Get farmer's prediction history
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''SELECT commodity, state, predicted_price, prediction_date 
           FROM predictions 
           WHERE user_id = ? 
           ORDER BY prediction_date DESC 
           LIMIT 10''',
        (session['user_id'],)
    )
    history = cursor.fetchall()
    
    return render_template('farmer_dashboard.html', 
                         commodities=commodities,
                         states=states,
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
        state = request.form.get('state', 'Maharashtra')  # Get selected state
        
        # Handle optional rainfall field - default to 100 if empty
        rainfall_input = request.form.get('rainfall', '100').strip()
        rainfall = float(rainfall_input) if rainfall_input else 100.0
        
        # Handle optional temperature field - default to 25 if empty
        temperature_input = request.form.get('temperature', '25').strip()
        temperature = float(temperature_input) if temperature_input else 25.0
        
        month = int(request.form.get('month', datetime.now().month))
        year = int(request.form.get('year', datetime.now().year))
        
        # Make prediction with state parameter and temperature
        prediction = ml_handler.predict(commodity, state, month, year, rainfall, temperature)
        
        if prediction['success']:
            # Save prediction to database
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO predictions 
                   (user_id, commodity, state, rainfall, temperature, month, year, predicted_price) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (session['user_id'], commodity, state, rainfall, temperature, month, year, 
                 prediction['predicted_price'])
            )
            db.commit()
            
            flash(f"Prediction successful for {state}! Price: ₹{prediction['predicted_price']:.2f} per quintal", 'success')
            return redirect(url_for('prediction_result', 
                                  commodity=commodity, 
                                  state=state, 
                                  price=prediction['predicted_price'],
                                  rainfall=rainfall,
                                  temperature=temperature,
                                  month=month,
                                  year=year))
        else:
            flash(f"Prediction failed: {prediction['error']}", 'danger')
            return redirect(url_for('farmer_dashboard'))
            
    except Exception as e:
        flash(f'Error making prediction: {str(e)}', 'danger')
        return redirect(url_for('farmer_dashboard'))

@app.route('/farmer/result')
@login_required
def prediction_result():
    """Display prediction result with detailed analysis"""
    commodity = request.args.get('commodity')
    state = request.args.get('state', 'Maharashtra')
    price = float(request.args.get('price'))
    rainfall = request.args.get('rainfall', '100')
    temperature = request.args.get('temperature', '25')
    month = request.args.get('month', '1')
    year = request.args.get('year', '2025')
    
    # Get additional data for detailed analysis
    from utils.price_visualization import PriceVisualization
    from utils.state_config import state_config
    from datetime import datetime
    
    price_visualizer = PriceVisualization()
    
    # Get historical data for comparison
    try:
        historical_data = price_visualizer.load_historical_data(commodity, state)
        if historical_data is not None and not historical_data.empty:
            # Calculate statistics
            avg_price = historical_data['WPI'].mean()
            min_price = historical_data['WPI'].min()
            max_price = historical_data['WPI'].max()
            
            # Convert to actual prices
            avg_actual_price = price_visualizer._wpi_to_price(avg_price, commodity)
            min_actual_price = price_visualizer._wpi_to_price(min_price, commodity)
            max_actual_price = price_visualizer._wpi_to_price(max_price, commodity)
            
            # Price comparison
            price_vs_avg = ((price - avg_actual_price) / avg_actual_price) * 100
            
            # Market sentiment
            if price_vs_avg > 10:
                market_sentiment = "Bullish"
                sentiment_color = "success"
                sentiment_icon = "fas fa-arrow-up"
            elif price_vs_avg < -10:
                market_sentiment = "Bearish"
                sentiment_color = "danger"
                sentiment_icon = "fas fa-arrow-down"
            else:
                market_sentiment = "Stable"
                sentiment_color = "info"
                sentiment_icon = "fas fa-minus"
        else:
            avg_actual_price = min_actual_price = max_actual_price = 0
            price_vs_avg = 0
            market_sentiment = "Unknown"
            sentiment_color = "secondary"
            sentiment_icon = "fas fa-question"
    except:
        avg_actual_price = min_actual_price = max_actual_price = 0
        price_vs_avg = 0
        market_sentiment = "Unknown"
        sentiment_color = "secondary"
        sentiment_icon = "fas fa-question"
    
    # Get month name
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_name = month_names[int(month)]
    
    # Get current time
    from datetime import datetime
    current_time = datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')
    
    # Get crop information
    crop_info = {
        'Jowar': {'season': 'Kharif', 'duration': '4-5 months', 'yield': '15-20 quintals/hectare'},
        'Wheat': {'season': 'Rabi', 'duration': '4-5 months', 'yield': '40-50 quintals/hectare'},
        'Cotton': {'season': 'Kharif', 'duration': '6-7 months', 'yield': '15-20 quintals/hectare'},
        'Sugarcane': {'season': 'Year-round', 'duration': '12-18 months', 'yield': '80-100 tons/hectare'},
        'Bajra': {'season': 'Kharif', 'duration': '3-4 months', 'yield': '20-25 quintals/hectare'}
    }
    
    crop_details = crop_info.get(commodity, {'season': 'Unknown', 'duration': 'Unknown', 'yield': 'Unknown'})
    
    return render_template('prediction_result.html', 
                         commodity=commodity, 
                         state=state, 
                         price=price,
                         rainfall=rainfall,
                         temperature=temperature,
                         month=month,
                         month_name=month_name,
                         year=year,
                         avg_price=avg_actual_price,
                         min_price=min_actual_price,
                         max_price=max_actual_price,
                         price_vs_avg=price_vs_avg,
                         market_sentiment=market_sentiment,
                         sentiment_color=sentiment_color,
                         sentiment_icon=sentiment_icon,
                         crop_details=crop_details,
                         current_time=current_time)

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
@app.route('/farmer/price-history/<commodity>/<state>')
@login_required
def price_history(commodity, state=None):
    """Display historical price trends for a commodity in a specific state"""
    try:
        # If no state specified, redirect to state selection
        if not state:
            states = state_config.get_all_states()
            # Now show all states, not just those with crop data
            available_states = list(states)  # Every state
            return render_template('select_state_for_history.html',
                                 commodity=commodity,
                                 states=available_states)
        
        # Generate charts for specific state
        trend_chart = price_visualizer.create_historical_trend_chart(commodity, state)
        seasonal_chart = price_visualizer.create_seasonal_pattern_chart(commodity, state)
        comparison_chart = price_visualizer.create_year_comparison_chart(commodity, state)
        
        return render_template('price_history.html',
                             commodity=commodity,
                             state=state,
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
        '''SELECT p.commodity, p.state, p.predicted_price, p.prediction_date, u.username
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
        '''SELECT p.id, u.username, p.commodity, p.state, p.predicted_price, 
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

