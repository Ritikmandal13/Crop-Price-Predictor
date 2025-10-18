"""
Machine Learning Model Handler
Loads pre-trained models and handles predictions
"""
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class MLModelHandler:
    def __init__(self):
        """Initialize ML Handler with models"""
        self.models = {}
        self.preprocessors = {}
        self.model_dir = 'model'
        self.available_commodities = ['Jowar', 'Wheat', 'Cotton', 'Sugarcane', 'Bajra']
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Load existing models
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models from pickle files"""
        print("Loading ML models...")
        
        model_files = {
            'Jowar': 'jmodel.pkl',
            'Wheat': 'wmodel.pkl',
            'Cotton': 'cmodel.pkl',
            'Sugarcane': 'smodel.pkl',
            'Bajra': 'bmodel.pkl'
        }
        
        # Load preprocessor from model directory
        preprocessor_path = os.path.join(self.model_dir, 'preprocessor.pkl')
        if os.path.exists(preprocessor_path):
            try:
                with open(preprocessor_path, 'rb') as f:
                    self.base_preprocessor = pickle.load(f)
                print(f"✅ Loaded preprocessor from {preprocessor_path}")
            except Exception as e:
                print(f"⚠️  Could not load preprocessor: {e}")
                self.base_preprocessor = None
        else:
            print(f"⚠️  Preprocessor not found at {preprocessor_path}")
            self.base_preprocessor = None
        
        # Load each commodity model from model directory
        for commodity, filename in model_files.items():
            model_path = os.path.join(self.model_dir, filename)
            
            if os.path.exists(model_path):
                try:
                    with open(model_path, 'rb') as f:
                        self.models[commodity] = pickle.load(f)
                    print(f"✅ Loaded {commodity} model from {model_path}")
                except Exception as e:
                    print(f"⚠️  Could not load {commodity} model: {e}")
            else:
                print(f"⚠️  Model not found: {model_path}")
        
        if not self.models:
            print("⚠️  No models loaded. Creating dummy models for testing...")
            self._create_dummy_models()
    
    def _create_dummy_models(self):
        """Create simple dummy models if real models are not available"""
        for commodity in self.available_commodities:
            # Create a simple Random Forest model
            model = RandomForestRegressor(n_estimators=10, random_state=42)
            
            # Train on dummy data
            X_dummy = np.random.rand(100, 3)  # month, year, rainfall
            y_dummy = np.random.rand(100) * 100 + 100  # prices between 100-200
            
            model.fit(X_dummy, y_dummy)
            self.models[commodity] = model
            print(f"✅ Created dummy model for {commodity}")
    
    def predict(self, commodity, location, month, year, rainfall):
        """
        Make price prediction for given inputs
        
        Args:
            commodity: Crop name (e.g., 'Wheat')
            location: District name
            month: Month (1-12)
            year: Year
            rainfall: Rainfall in mm
        
        Returns:
            Dictionary with prediction result
        """
        try:
            if commodity not in self.models:
                return {
                    'success': False,
                    'error': f'Model not available for {commodity}'
                }
            
            # Prepare input features
            features = np.array([[month, year, rainfall]], dtype=object)
            
            # Preprocess if preprocessor available
            if self.base_preprocessor:
                try:
                    features = self.base_preprocessor.transform(features)
                except:
                    # If preprocessing fails, use raw features
                    features = np.array([[month, year, rainfall]], dtype=float)
            else:
                features = np.array([[month, year, rainfall]], dtype=float)
            
            # Make prediction
            model = self.models[commodity]
            prediction = model.predict(features)[0]
            
            # Calculate price range based on commodity
            # MSP (Minimum Support Price) multipliers from original project
            multipliers = {
                'Jowar': {'min': 1550, 'max': 2970},
                'Wheat': {'min': 1350, 'max': 2125},
                'Cotton': {'min': 3600, 'max': 6080},
                'Sugarcane': {'min': 2250, 'max': 2775},
                'Bajra': {'min': 1175, 'max': 2350}
            }
            
            if commodity in multipliers:
                min_price = (prediction * multipliers[commodity]['min']) / 100
                max_price = (prediction * multipliers[commodity]['max']) / 100
                predicted_price = (min_price + max_price) / 2
            else:
                # Default calculation if commodity not in list
                predicted_price = prediction * 20  # Basic multiplier
                min_price = predicted_price * 0.8
                max_price = predicted_price * 1.2
            
            return {
                'success': True,
                'predicted_price': round(predicted_price, 2),
                'min_price': round(min_price, 2),
                'max_price': round(max_price, 2),
                'commodity': commodity,
                'location': location,
                'month': month,
                'year': year,
                'rainfall': rainfall
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def retrain_model(self, commodity, dataset_path):
        """
        Retrain model with new dataset
        
        Args:
            commodity: Crop name
            dataset_path: Path to CSV dataset
        
        Returns:
            Dictionary with training result
        """
        try:
            # Load dataset
            df = pd.read_csv(dataset_path)
            
            # Validate dataset has required columns
            required_cols = ['Month', 'Year', 'Rainfall', 'WPI']
            if not all(col in df.columns for col in required_cols):
                return {
                    'success': False,
                    'error': f'Dataset must contain columns: {required_cols}'
                }
            
            # Prepare features and target
            X = df[['Month', 'Year', 'Rainfall']].values
            y = df['WPI'].values
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            # Save model
            model_filename = f"{commodity.lower()}_model.pkl"
            model_path = os.path.join(self.model_dir, model_filename)
            
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Update loaded model
            self.models[commodity] = model
            
            return {
                'success': True,
                'accuracy': r2 * 100,
                'rmse': rmse,
                'samples': len(df),
                'model_path': model_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_available_commodities(self):
        """Return list of available commodities"""
        return self.available_commodities
    
    def is_model_available(self, commodity):
        """Check if model is available for commodity"""
        return commodity in self.models

# Create global instance
ml_handler = MLModelHandler()

