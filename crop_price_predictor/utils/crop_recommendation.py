"""
Crop Recommendation System
Suggests best crops based on soil type, rainfall, market demand, and profitability
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class CropRecommendationSystem:
    def __init__(self):
        """Initialize the crop recommendation system"""
        self.model = None
        self.crop_database = self._initialize_crop_database()
    
    def _initialize_crop_database(self):
        """Initialize crop database with characteristics"""
        return {
            'Jowar': {
                'soil_types': ['Black', 'Red', 'Sandy Loam'],
                'min_rainfall': 400,
                'max_rainfall': 1000,
                'min_temp': 25,
                'max_temp': 35,
                'growing_season': 'Kharif',
                'avg_profit_per_acre': 25000,
                'market_demand': 'Medium',
                'water_requirement': 'Low'
            },
            'Wheat': {
                'soil_types': ['Loamy', 'Clay', 'Sandy Loam'],
                'min_rainfall': 300,
                'max_rainfall': 600,
                'min_temp': 10,
                'max_temp': 25,
                'growing_season': 'Rabi',
                'avg_profit_per_acre': 30000,
                'market_demand': 'High',
                'water_requirement': 'Medium'
            },
            'Cotton': {
                'soil_types': ['Black', 'Sandy Loam', 'Alluvial'],
                'min_rainfall': 500,
                'max_rainfall': 1200,
                'min_temp': 21,
                'max_temp': 30,
                'growing_season': 'Kharif',
                'avg_profit_per_acre': 40000,
                'market_demand': 'High',
                'water_requirement': 'High'
            },
            'Sugarcane': {
                'soil_types': ['Loamy', 'Black', 'Red'],
                'min_rainfall': 750,
                'max_rainfall': 1500,
                'min_temp': 20,
                'max_temp': 35,
                'growing_season': 'Year-round',
                'avg_profit_per_acre': 50000,
                'market_demand': 'High',
                'water_requirement': 'Very High'
            },
            'Bajra': {
                'soil_types': ['Sandy', 'Sandy Loam', 'Red'],
                'min_rainfall': 250,
                'max_rainfall': 600,
                'min_temp': 25,
                'max_temp': 35,
                'growing_season': 'Kharif',
                'avg_profit_per_acre': 20000,
                'market_demand': 'Medium',
                'water_requirement': 'Low'
            },
            'Rice': {
                'soil_types': ['Clay', 'Loamy', 'Alluvial'],
                'min_rainfall': 1000,
                'max_rainfall': 2000,
                'min_temp': 20,
                'max_temp': 35,
                'growing_season': 'Kharif',
                'avg_profit_per_acre': 35000,
                'market_demand': 'Very High',
                'water_requirement': 'Very High'
            },
            'Maize': {
                'soil_types': ['Loamy', 'Sandy Loam', 'Black'],
                'min_rainfall': 500,
                'max_rainfall': 1000,
                'min_temp': 18,
                'max_temp': 30,
                'growing_season': 'Kharif/Rabi',
                'avg_profit_per_acre': 28000,
                'market_demand': 'High',
                'water_requirement': 'Medium'
            }
        }
    
    def recommend_crops(self, soil_type, rainfall, temperature, season='Kharif'):
        """
        Recommend crops based on input parameters
        
        Args:
            soil_type: Type of soil (e.g., 'Black', 'Loamy', 'Sandy')
            rainfall: Expected annual rainfall in mm
            temperature: Average temperature in Celsius
            season: Growing season (Kharif/Rabi)
        
        Returns:
            List of recommended crops with scores
        """
        recommendations = []
        
        for crop, info in self.crop_database.items():
            score = 0
            reasons = []
            
            # Check soil compatibility (40 points)
            if soil_type in info['soil_types']:
                score += 40
                reasons.append(f"✓ Suitable for {soil_type} soil")
            else:
                reasons.append(f"✗ Not ideal for {soil_type} soil")
            
            # Check rainfall suitability (25 points)
            if info['min_rainfall'] <= rainfall <= info['max_rainfall']:
                score += 25
                reasons.append(f"✓ Good rainfall match ({rainfall}mm)")
            elif rainfall < info['min_rainfall']:
                score += 10
                reasons.append(f"⚠ Rainfall below optimal ({rainfall}mm < {info['min_rainfall']}mm)")
            else:
                score += 15
                reasons.append(f"⚠ Rainfall above optimal ({rainfall}mm > {info['max_rainfall']}mm)")
            
            # Check temperature suitability (20 points)
            if info['min_temp'] <= temperature <= info['max_temp']:
                score += 20
                reasons.append(f"✓ Ideal temperature ({temperature}°C)")
            else:
                score += 5
                reasons.append(f"⚠ Temperature not optimal")
            
            # Market demand score (15 points)
            demand_scores = {'Very High': 15, 'High': 12, 'Medium': 8, 'Low': 5}
            score += demand_scores.get(info['market_demand'], 5)
            reasons.append(f"Market demand: {info['market_demand']}")
            
            recommendations.append({
                'crop': crop,
                'score': score,
                'profitability': info['avg_profit_per_acre'],
                'water_requirement': info['water_requirement'],
                'season': info['growing_season'],
                'market_demand': info['market_demand'],
                'reasons': reasons,
                'suitability': self._get_suitability_label(score)
            })
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def _get_suitability_label(self, score):
        """Convert score to suitability label"""
        if score >= 85:
            return 'Excellent'
        elif score >= 70:
            return 'Very Good'
        elif score >= 55:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        else:
            return 'Not Recommended'
    
    def get_crop_info(self, crop_name):
        """Get detailed information about a specific crop"""
        return self.crop_database.get(crop_name, None)
    
    def compare_crops(self, crop1, crop2):
        """Compare two crops side by side"""
        info1 = self.crop_database.get(crop1)
        info2 = self.crop_database.get(crop2)
        
        if not info1 or not info2:
            return None
        
        comparison = {
            'crop1': crop1,
            'crop2': crop2,
            'profitability_diff': info1['avg_profit_per_acre'] - info2['avg_profit_per_acre'],
            'better_profit': crop1 if info1['avg_profit_per_acre'] > info2['avg_profit_per_acre'] else crop2,
            'water_comparison': {
                crop1: info1['water_requirement'],
                crop2: info2['water_requirement']
            },
            'market_comparison': {
                crop1: info1['market_demand'],
                crop2: info2['market_demand']
            }
        }
        
        return comparison

# Global instance
crop_recommender = CropRecommendationSystem()

