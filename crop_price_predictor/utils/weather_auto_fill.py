"""
Calculate State-Month Weather Averages
Generates average rainfall and temperature for each state-month combination
"""
import pandas as pd
import numpy as np
import os
import json

class WeatherAveragesCalculator:
    """Calculate average weather conditions by state and month"""
    
    def __init__(self):
        self.state_folders = {
            'Maharashtra': 'Maharashtra',
            'Punjab': 'Punjab', 
            'Karnataka': 'Karnataka',
            'Uttar Pradesh': 'UttarPradesh',
            'Gujarat': 'Gujarat',
            'Madhya Pradesh': 'MadhyaPradesh'
        }
    
    def calculate_state_month_averages(self, base_dir='data/states'):
        """Calculate average rainfall and temperature for each state-month combination"""
        
        averages = {}
        
        for state_name, folder_name in self.state_folders.items():
            state_path = os.path.join(base_dir, folder_name)
            
            if not os.path.exists(state_path):
                continue
            
            # Get all CSV files for this state
            csv_files = [f for f in os.listdir(state_path) if f.endswith('.csv')]
            
            if not csv_files:
                continue
            
            # Combine all crop data for this state
            all_data = []
            
            for csv_file in csv_files:
                csv_path = os.path.join(state_path, csv_file)
                df = pd.read_csv(csv_path)
                all_data.append(df)
            
            # Combine all data
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Calculate monthly averages
            monthly_avg = combined_df.groupby('Month').agg({
                'Rainfall': 'mean',
                'Temperature': 'mean'
            }).round(1)
            
            # Convert to dictionary
            state_averages = {}
            for month in range(1, 13):
                if month in monthly_avg.index:
                    state_averages[month] = {
                        'rainfall': float(monthly_avg.loc[month, 'Rainfall']),
                        'temperature': float(monthly_avg.loc[month, 'Temperature'])
                    }
                else:
                    # Fallback values if no data
                    state_averages[month] = {
                        'rainfall': 50.0,
                        'temperature': 25.0
                    }
            
            averages[state_name] = state_averages
        
        return averages
    
    def save_averages_to_json(self, averages, output_path='static/js/weather_averages.json'):
        """Save averages to JSON file for frontend use"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(averages, f, indent=2)
        
        print(f"✅ Weather averages saved to: {output_path}")
    
    def generate_javascript_function(self, averages):
        """Generate JavaScript function for frontend"""
        
        js_code = """
// Auto-fill weather data based on state and month
function autoFillWeatherData() {
    const stateSelect = document.getElementById('state');
    const monthSelect = document.getElementById('month');
    const rainfallInput = document.getElementById('rainfall');
    const temperatureInput = document.getElementById('temperature');
    
    if (!stateSelect || !monthSelect || !rainfallInput || !temperatureInput) {
        return;
    }
    
    const selectedState = stateSelect.value;
    const selectedMonth = parseInt(monthSelect.value);
    
    if (!selectedState || !selectedMonth) {
        return;
    }
    
    // Weather averages by state and month
    const weatherAverages = """ + json.dumps(averages, indent=4) + """;
    
    if (weatherAverages[selectedState] && weatherAverages[selectedState][selectedMonth]) {
        const avg = weatherAverages[selectedState][selectedMonth];
        
        // Only auto-fill if fields are empty
        if (!rainfallInput.value || rainfallInput.value === '') {
            rainfallInput.value = avg.rainfall;
        }
        
        if (!temperatureInput.value || temperatureInput.value === '') {
            temperatureInput.value = avg.temperature;
        }
        
        // Show info message
        showWeatherInfo(selectedState, selectedMonth, avg);
    }
}

function showWeatherInfo(state, month, avg) {
    // Create or update info message
    let infoDiv = document.getElementById('weather-info');
    if (!infoDiv) {
        infoDiv = document.createElement('div');
        infoDiv.id = 'weather-info';
        infoDiv.className = 'alert alert-info mt-2';
        document.getElementById('temperature').parentNode.appendChild(infoDiv);
    }
    
    const monthNames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    infoDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>
        <strong>Auto-filled weather data for ${state} in ${monthNames[month]}:</strong><br>
        Average Rainfall: ${avg.rainfall}mm | Average Temperature: ${avg.temperature}°C<br>
        <small class="text-muted">You can modify these values if you have more accurate data.</small>
    `;
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    const stateSelect = document.getElementById('state');
    const monthSelect = document.getElementById('month');
    
    if (stateSelect) {
        stateSelect.addEventListener('change', autoFillWeatherData);
    }
    
    if (monthSelect) {
        monthSelect.addEventListener('change', autoFillWeatherData);
    }
    
    // Auto-fill on page load if state and month are already selected
    setTimeout(autoFillWeatherData, 100);
});
"""
        
        return js_code

# Main execution
if __name__ == '__main__':
    print("=" * 70)
    print("🌤️  Calculating State-Month Weather Averages")
    print("=" * 70)
    print()
    
    calculator = WeatherAveragesCalculator()
    averages = calculator.calculate_state_month_averages()
    
    # Save to JSON
    calculator.save_averages_to_json(averages)
    
    # Generate JavaScript
    js_code = calculator.generate_javascript_function(averages)
    
    # Save JavaScript file
    js_path = 'static/js/weather_auto_fill.js'
    os.makedirs(os.path.dirname(js_path), exist_ok=True)
    
    with open(js_path, 'w') as f:
        f.write(js_code)
    
    print(f"✅ JavaScript auto-fill code saved to: {js_path}")
    
    # Display summary
    print()
    print("📊 Weather Averages Summary:")
    print()
    
    for state, months in averages.items():
        print(f"🌍 {state}:")
        for month in [3, 6, 9, 12]:  # Show sample months
            if month in months:
                avg = months[month]
                print(f"   Month {month:2d}: {avg['rainfall']:5.1f}mm rain, {avg['temperature']:4.1f}°C")
        print()
    
    print("=" * 70)
    print("✅ Auto-fill system ready!")
    print("=" * 70)
    print()
    print("🎯 Features:")
    print("   - Auto-fills rainfall & temperature when state+month selected")
    print("   - Uses historical averages from datasets")
    print("   - Farmers can still override with their own values")
    print("   - Shows helpful info messages")
    print()

