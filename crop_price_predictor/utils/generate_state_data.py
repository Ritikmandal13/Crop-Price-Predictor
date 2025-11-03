"""
Generate State-Specific Synthetic Data
Creates realistic variations of crop price data for different Indian states
"""
import pandas as pd
import numpy as np
import os

class StateDataGenerator:
    """Generate state-specific crop price datasets"""
    
    def __init__(self):
        """Initialize with state-specific parameters"""
        
        # State-specific rainfall adjustments (multipliers)
        self.rainfall_adjustments = {
            'Punjab': 0.65,        # Drier climate
            'Karnataka': 0.85,     # Moderate rainfall
            'Uttar Pradesh': 0.90, # Similar to Maharashtra
            'Gujarat': 0.55,       # Drier, desert regions
            'Madhya Pradesh': 0.80 # Central India, moderate
        }
        
        # WPI (price) adjustments based on regional factors
        self.wpi_adjustments = {
            'Punjab': {
                'base': 1.08,      # Generally higher prices
                'Wheat': 1.12,     # Premium wheat region
                'Cotton': 1.05,
                'Bajra': 1.03,
                'Sugarcane': 1.06
            },
            'Karnataka': {
                'base': 0.96,      # Slightly lower
                'Jowar': 0.94,
                'Cotton': 1.02,
                'Sugarcane': 0.98,
                'Wheat': 0.95
            },
            'Uttar Pradesh': {
                'base': 1.03,      # Higher due to large market
                'Wheat': 1.05,
                'Sugarcane': 1.08, # Major sugarcane state
                'Bajra': 1.02
            },
            'Gujarat': {
                'base': 1.01,
                'Cotton': 1.06,    # Major cotton state
                'Wheat': 1.02,
                'Bajra': 0.98
            },
            'Madhya Pradesh': {
                'base': 0.92,      # Generally lower prices
                'Jowar': 0.90,
                'Wheat': 0.94,
                'Cotton': 0.96
            }
        }
        
        # Seasonal variation adjustments (different growing seasons)
        self.seasonal_shifts = {
            'Punjab': {'kharif_shift': -1, 'rabi_shift': 0},      # Harvest 1 month earlier
            'Karnataka': {'kharif_shift': 1, 'rabi_shift': 0},    # Harvest 1 month later
            'Uttar Pradesh': {'kharif_shift': 0, 'rabi_shift': 0}, # Similar timing
            'Gujarat': {'kharif_shift': 0, 'rabi_shift': 1},      # Rabi delayed
            'Madhya Pradesh': {'kharif_shift': 0, 'rabi_shift': -1} # Rabi earlier
        }
    
    def generate_state_dataset(self, base_csv_path, state_name, crop_name, output_path):
        """
        Generate state-specific dataset from base Maharashtra data
        
        Args:
            base_csv_path: Path to Maharashtra CSV file
            state_name: Target state name
            crop_name: Crop name
            output_path: Output file path
        """
        # Read base data
        df = pd.read_csv(base_csv_path)
        
        # Apply state-specific transformations
        df_state = df.copy()
        
        # 1. Adjust Rainfall
        if state_name in self.rainfall_adjustments:
            rainfall_multiplier = self.rainfall_adjustments[state_name]
            df_state['Rainfall'] = df_state['Rainfall'] * rainfall_multiplier
            
            # Add some realistic noise (±10%)
            noise = np.random.uniform(0.90, 1.10, len(df_state))
            df_state['Rainfall'] = df_state['Rainfall'] * noise
            
            # Ensure minimum rainfall
            df_state['Rainfall'] = df_state['Rainfall'].clip(lower=10)
        
        # 2. Adjust WPI (Prices)
        if state_name in self.wpi_adjustments:
            state_adj = self.wpi_adjustments[state_name]
            
            # Base adjustment
            base_multiplier = state_adj['base']
            
            # Crop-specific adjustment
            crop_multiplier = state_adj.get(crop_name, 1.0)
            
            # Combined adjustment
            total_multiplier = base_multiplier * crop_multiplier
            
            df_state['WPI'] = df_state['WPI'] * total_multiplier
            
            # Add realistic market fluctuation (±5%)
            noise = np.random.uniform(0.95, 1.05, len(df_state))
            df_state['WPI'] = df_state['WPI'] * noise
        
        # 3. Apply seasonal shifts (subtle changes in timing)
        if state_name in self.seasonal_shifts:
            shift = self.seasonal_shifts[state_name]
            
            # Apply subtle price variations based on harvest timing
            # This creates realistic regional price differences
            for idx, row in df_state.iterrows():
                month = row['Month']
                
                # Kharif crops (June-Oct): Jowar, Cotton, Bajra
                if crop_name in ['Jowar', 'Cotton', 'Bajra']:
                    if 6 <= month <= 10:
                        # Harvest timing affects prices
                        shift_factor = 1.0 + (shift['kharif_shift'] * 0.02)
                        df_state.at[idx, 'WPI'] *= shift_factor
                
                # Rabi crops (Nov-Apr): Wheat
                elif crop_name in ['Wheat']:
                    if month >= 11 or month <= 4:
                        shift_factor = 1.0 + (shift['rabi_shift'] * 0.02)
                        df_state.at[idx, 'WPI'] *= shift_factor
                
                # Year-round: Sugarcane (less affected)
                # No shift needed
        
        # 4. Add state-specific yearly trend variation
        # Different states have different growth rates
        yearly_trends = {
            'Punjab': 1.02,        # Faster growth
            'Karnataka': 0.99,     # Slower growth
            'Uttar Pradesh': 1.01, # Moderate growth
            'Gujarat': 1.015,      # Moderate-high growth
            'Madhya Pradesh': 0.98 # Slower growth
        }
        
        if state_name in yearly_trends:
            trend = yearly_trends[state_name]
            base_year = df_state['Year'].min()
            
            for idx, row in df_state.iterrows():
                years_passed = row['Year'] - base_year
                trend_factor = trend ** years_passed
                df_state.at[idx, 'WPI'] *= trend_factor
        
        # 5. Round to reasonable precision
        df_state['Rainfall'] = df_state['Rainfall'].round(1)
        df_state['WPI'] = df_state['WPI'].round(2)
        
        # Save to output path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_state.to_csv(output_path, index=False)
        
        return df_state
    
    def generate_all_states(self, base_data_dir='data/states/Maharashtra', 
                           output_base_dir='data/states'):
        """Generate datasets for all states"""
        
        state_crops = {
            'Punjab': ['Wheat', 'Bajra', 'Cotton', 'Sugarcane'],
            'Karnataka': ['Jowar', 'Cotton', 'Sugarcane', 'Wheat'],
            'Uttar Pradesh': ['Wheat', 'Sugarcane', 'Bajra'],
            'Gujarat': ['Cotton', 'Wheat', 'Bajra'],
            'Madhya Pradesh': ['Jowar', 'Wheat', 'Cotton']
        }
        
        results = []
        
        for state, crops in state_crops.items():
            state_folder = state.replace(' ', '')
            
            for crop in crops:
                base_file = os.path.join(base_data_dir, f"{crop}.csv")
                output_file = os.path.join(output_base_dir, state_folder, f"{crop}.csv")
                
                if os.path.exists(base_file):
                    print(f"Generating {crop} data for {state}...")
                    df = self.generate_state_dataset(base_file, state, crop, output_file)
                    
                    results.append({
                        'state': state,
                        'crop': crop,
                        'file': output_file,
                        'rows': len(df),
                        'avg_wpi': df['WPI'].mean(),
                        'avg_rainfall': df['Rainfall'].mean()
                    })
                else:
                    print(f"⚠️  Base file not found: {base_file}")
        
        return results

# Main execution
if __name__ == '__main__':
    print("=" * 60)
    print("🌾 Generating State-Specific Crop Price Data")
    print("=" * 60)
    print()
    
    generator = StateDataGenerator()
    results = generator.generate_all_states()
    
    print()
    print("=" * 60)
    print("✅ Generation Complete!")
    print("=" * 60)
    print()
    
    # Summary
    print("📊 Summary:")
    print()
    
    for result in results:
        print(f"✓ {result['state']} - {result['crop']}")
        print(f"  Rows: {result['rows']} | Avg WPI: {result['avg_wpi']:.2f} | "
              f"Avg Rainfall: {result['avg_rainfall']:.1f}mm")
    
    print()
    print(f"Total datasets generated: {len(results)}")
    print()

