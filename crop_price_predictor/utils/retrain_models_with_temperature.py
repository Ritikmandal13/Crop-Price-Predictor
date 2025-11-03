"""
Retrain All ML Models with Temperature Feature
Updates models to use 4 features: Month, Year, Rainfall, Temperature
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline

def retrain_model(crop_name, csv_path, model_output_path):
    """
    Train a Random Forest model for a specific crop
    
    Args:
        crop_name: Name of the crop
        csv_path: Path to CSV with training data
        model_output_path: Path to save the trained model
    
    Returns:
        Dictionary with training metrics
    """
    print(f"\n{'='*60}")
    print(f"Training model for: {crop_name}")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} rows from {csv_path}")
    
    # Prepare features and target
    # Features: Month, Year, Rainfall, Temperature
    X = df[['Month', 'Year', 'Rainfall', 'Temperature']].values
    y = df['WPI'].values
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Testing set: {len(X_test)} samples")
    
    # Create and train Random Forest model
    print("\nTraining Random Forest...")
    
    model = RandomForestRegressor(
        n_estimators=100,      # Number of trees
        max_depth=15,          # Maximum depth of trees
        min_samples_split=5,   # Minimum samples to split node
        min_samples_leaf=2,    # Minimum samples in leaf
        random_state=42,
        n_jobs=-1              # Use all CPU cores
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    
    # Testing performance
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\n📊 Training Metrics:")
    print(f"   R² Score:  {train_r2:.4f}")
    print(f"   RMSE:      {train_rmse:.4f}")
    print(f"   MAE:       {train_mae:.4f}")
    
    print(f"\n📊 Testing Metrics:")
    print(f"   R² Score:  {test_r2:.4f}")
    print(f"   RMSE:      {test_rmse:.4f}")
    print(f"   MAE:       {test_mae:.4f}")
    
    # Feature importance
    feature_names = ['Month', 'Year', 'Rainfall', 'Temperature']
    importances = model.feature_importances_
    
    print(f"\n🎯 Feature Importances:")
    for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
        print(f"   {name:12s}: {importance:.4f} ({importance*100:.1f}%)")
    
    # Save model
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    with open(model_output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n✅ Model saved to: {model_output_path}")
    
    return {
        'crop': crop_name,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'feature_importances': dict(zip(feature_names, importances)),
        'n_samples': len(df)
    }

def retrain_all_models():
    """Retrain all crop models using Maharashtra data"""
    
    crops = {
        'Jowar': ('data/states/Maharashtra/Jowar.csv', 'model/jmodel.pkl'),
        'Wheat': ('data/states/Maharashtra/Wheat.csv', 'model/wmodel.pkl'),
        'Cotton': ('data/states/Maharashtra/Cotton.csv', 'model/cmodel.pkl'),
        'Sugarcane': ('data/states/Maharashtra/Sugarcane.csv', 'model/smodel.pkl'),
        'Bajra': ('data/states/Maharashtra/Bajra.csv', 'model/bmodel.pkl')
    }
    
    results = []
    
    print("\n" + "="*70)
    print("🌾 RETRAINING ALL ML MODELS WITH TEMPERATURE FEATURE")
    print("="*70)
    
    for crop, (csv_path, model_path) in crops.items():
        try:
            result = retrain_model(crop, csv_path, model_path)
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error training {crop}: {str(e)}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 TRAINING SUMMARY")
    print("="*70)
    print()
    
    print(f"{'Crop':<12} {'R² Score':<10} {'RMSE':<10} {'MAE':<10} {'Samples':<10}")
    print("-" * 60)
    
    for result in results:
        print(f"{result['crop']:<12} {result['test_r2']:<10.4f} "
              f"{result['test_rmse']:<10.2f} {result['test_mae']:<10.2f} "
              f"{result['n_samples']:<10}")
    
    print()
    
    # Average metrics
    avg_r2 = np.mean([r['test_r2'] for r in results])
    avg_rmse = np.mean([r['test_rmse'] for r in results])
    avg_mae = np.mean([r['test_mae'] for r in results])
    
    print(f"{'Average':<12} {avg_r2:<10.4f} {avg_rmse:<10.2f} {avg_mae:<10.2f}")
    print()
    
    print("="*70)
    print("✅ ALL MODELS RETRAINED SUCCESSFULLY!")
    print("="*70)
    print()
    print("🎯 Models now use 4 features:")
    print("   1. Month")
    print("   2. Year")
    print("   3. Rainfall (mm)")
    print("   4. Temperature (°C)  ⭐ NEW!")
    print()
    print("🚀 Your application is now using weather-based predictions!")
    print()

if __name__ == '__main__':
    retrain_all_models()

