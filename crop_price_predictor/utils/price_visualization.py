"""
Price Visualization and Historical Analysis
Generates charts and trends for crop prices
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.utils
import json
from datetime import datetime, timedelta

class PriceVisualization:
    def __init__(self):
        """Initialize price visualization system"""
        # MSP multipliers for converting WPI to actual prices (₹/quintal)
        self.crop_multipliers = {
            'Jowar': {'min': 1550, 'max': 2970},
            'Wheat': {'min': 1350, 'max': 2125},
            'Cotton': {'min': 3600, 'max': 6080},
            'Sugarcane': {'min': 2250, 'max': 2775},
            'Bajra': {'min': 1175, 'max': 2350}
        }
    
    def _wpi_to_price(self, wpi, commodity):
        """Convert WPI to approximate price in rupees per quintal"""
        if commodity in self.crop_multipliers:
            multipliers = self.crop_multipliers[commodity]
            min_price = (wpi * multipliers['min']) / 100
            max_price = (wpi * multipliers['max']) / 100
            avg_price = (min_price + max_price) / 2
            return avg_price
        return wpi  # Fallback to WPI if commodity not found
    
    def load_historical_data(self, commodity, csv_path=None):
        """
        Load historical price data from CSV
        
        Args:
            commodity: Crop name
            csv_path: Path to CSV file (optional)
        
        Returns:
            DataFrame with historical data
        """
        if csv_path is None:
            csv_path = f"data/{commodity}.csv"
        
        try:
            df = pd.read_csv(csv_path)
            # Create a proper date column
            df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def create_historical_trend_chart(self, commodity):
        """
        Create interactive line chart showing historical price trends
        
        Args:
            commodity: Crop name
        
        Returns:
            Plotly figure as JSON
        """
        df = self.load_historical_data(commodity)
        
        if df is None or df.empty:
            return None
        
        # Create figure
        fig = go.Figure()
        
        # Convert dates to strings for JSON serialization
        dates_str = df['Date'].dt.strftime('%Y-%m-%d').tolist()
        wpi_values = df['WPI'].tolist()
        
        # Convert WPI to actual prices in rupees
        price_values = [self._wpi_to_price(wpi, commodity) for wpi in wpi_values]
        
        # Add price trend line (converted from WPI)
        fig.add_trace(go.Scatter(
            x=dates_str,
            y=price_values,
            mode='lines+markers',
            name='Price per Quintal',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=6),
            customdata=wpi_values,
            hovertemplate='<b>Date</b>: %{x}<br>' +
                         '<b>Price</b>: ₹%{y:.2f}/quintal<br>' +
                         '<b>WPI</b>: %{customdata:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add rainfall as secondary axis if available
        if 'Rainfall' in df.columns:
            rainfall_values = df['Rainfall'].tolist()
            fig.add_trace(go.Bar(
                x=dates_str,
                y=rainfall_values,
                name='Rainfall (mm)',
                yaxis='y2',
                marker_color='rgba(52, 152, 219, 0.3)',
                hovertemplate='<b>Date</b>: %{x}<br>' +
                             '<b>Rainfall</b>: %{y:.1f} mm<br>' +
                             '<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f'Historical Price Trend - {commodity}',
            xaxis_title='Date',
            yaxis_title='Price (₹ per quintal)',
            yaxis2=dict(
                title='Rainfall (mm)',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Use plotly's JSON encoder with engine='json' to avoid binary encoding
        import plotly
        return plotly.io.to_json(fig, engine='json')
    
    def create_seasonal_pattern_chart(self, commodity):
        """
        Create chart showing seasonal price patterns
        
        Args:
            commodity: Crop name
        
        Returns:
            Plotly figure as JSON
        """
        df = self.load_historical_data(commodity)
        
        if df is None or df.empty:
            return None
        
        # Calculate average WPI by month across all years
        monthly_avg = df.groupby('Month')['WPI'].agg(['mean', 'std']).reset_index()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = go.Figure()
        
        # Convert to lists for JSON serialization
        months_list = monthly_avg['Month'].tolist()
        mean_wpi_list = monthly_avg['mean'].tolist()
        std_list = monthly_avg['std'].tolist()
        
        # Convert WPI to prices
        mean_price_list = [self._wpi_to_price(wpi, commodity) for wpi in mean_wpi_list]
        std_price_list = [self._wpi_to_price(std, commodity) for std in std_list]
        
        # Add average line
        fig.add_trace(go.Scatter(
            x=months_list,
            y=mean_price_list,
            mode='lines+markers',
            name='Average Price',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=10),
            customdata=mean_wpi_list,
            error_y=dict(
                type='data',
                array=std_price_list,
                visible=True
            ),
            hovertemplate='<b>Month</b>: %{x}<br>' +
                         '<b>Avg Price</b>: ₹%{y:.2f}/quintal<br>' +
                         '<b>WPI</b>: %{customdata:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Seasonal Price Pattern - {commodity}',
            xaxis=dict(
                title='Month',
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=month_names
            ),
            yaxis_title='Average Price (₹ per quintal)',
            hovermode='x',
            template='plotly_white',
            height=400
        )
        
        # Use plotly's JSON encoder with engine='json' to avoid binary encoding
        import plotly
        return plotly.io.to_json(fig, engine='json')
    
    def create_year_comparison_chart(self, commodity):
        """
        Create chart comparing prices across different years
        
        Args:
            commodity: Crop name
        
        Returns:
            Plotly figure as JSON
        """
        df = self.load_historical_data(commodity)
        
        if df is None or df.empty:
            return None
        
        # Get last 5 years
        recent_years = sorted(df['Year'].unique())[-5:]
        df_recent = df[df['Year'].isin(recent_years)]
        
        fig = go.Figure()
        
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        
        for i, year in enumerate(recent_years):
            year_data = df_recent[df_recent['Year'] == year]
            # Convert to lists for JSON serialization
            months_list = year_data['Month'].tolist()
            wpi_list = year_data['WPI'].tolist()
            
            # Convert WPI to prices
            price_list = [self._wpi_to_price(wpi, commodity) for wpi in wpi_list]
            
            fig.add_trace(go.Scatter(
                x=months_list,
                y=price_list,
                mode='lines+markers',
                name=str(year),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6),
                customdata=wpi_list,
                hovertemplate='<b>Month</b>: %{x}<br>' +
                             '<b>Price</b>: ₹%{y:.2f}/quintal<br>' +
                             '<b>WPI</b>: %{customdata:.2f}<br>' +
                             '<extra></extra>'
            ))
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig.update_layout(
            title=f'Year-wise Price Comparison - {commodity}',
            xaxis=dict(
                title='Month',
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=month_names
            ),
            yaxis_title='Price (₹ per quintal)',
            hovermode='x',
            template='plotly_white',
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Use plotly's JSON encoder with engine='json' to avoid binary encoding
        import plotly
        return plotly.io.to_json(fig, engine='json')
    
    def predict_future_prices(self, commodity, months_ahead=6):
        """
        Predict future prices using simple trend analysis
        
        Args:
            commodity: Crop name
            months_ahead: Number of months to predict
        
        Returns:
            Dictionary with predictions
        """
        df = self.load_historical_data(commodity)
        
        if df is None or df.empty:
            return None
        
        # Get last 12 months of data
        df_sorted = df.sort_values('Date')
        recent_data = df_sorted.tail(12)
        
        # Calculate trend
        avg_price = recent_data['WPI'].mean()
        trend = (recent_data['WPI'].iloc[-1] - recent_data['WPI'].iloc[0]) / len(recent_data)
        
        # Generate predictions
        last_date = df_sorted['Date'].max()
        predictions = []
        
        for i in range(1, months_ahead + 1):
            future_date = last_date + pd.DateOffset(months=i)
            predicted_price = avg_price + (trend * i)
            
            predictions.append({
                'month': future_date.strftime('%B %Y'),
                'predicted_wpi': round(predicted_price, 2),
                'confidence': 'Medium' if i <= 3 else 'Low'
            })
        
        return predictions
    
    def create_future_forecast_chart(self, commodity, months_ahead=6):
        """
        Create chart showing historical data + future forecast
        
        Args:
            commodity: Crop name
            months_ahead: Number of months to forecast
        
        Returns:
            Plotly figure as JSON
        """
        df = self.load_historical_data(commodity)
        
        if df is None or df.empty:
            return None
        
        # Get recent data (last 2 years)
        df_sorted = df.sort_values('Date')
        recent_data = df_sorted.tail(24)
        
        # Generate future predictions
        predictions = self.predict_future_prices(commodity, months_ahead)
        
        if predictions is None:
            return None
        
        # Create future dates DataFrame
        future_dates = []
        future_prices = []
        last_date = df_sorted['Date'].max()
        
        for i, pred in enumerate(predictions, 1):
            future_dates.append((last_date + pd.DateOffset(months=i)).strftime('%Y-%m-%d'))
            future_prices.append(pred['predicted_wpi'])
        
        fig = go.Figure()
        
        # Convert historical data to lists
        hist_dates = recent_data['Date'].dt.strftime('%Y-%m-%d').tolist()
        hist_wpi = recent_data['WPI'].tolist()
        hist_prices = [self._wpi_to_price(wpi, commodity) for wpi in hist_wpi]
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=hist_dates,
            y=hist_prices,
            mode='lines+markers',
            name='Historical Prices',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=6),
            customdata=hist_wpi,
            hovertemplate='<b>Date</b>: %{x}<br>' +
                         '<b>Price</b>: ₹%{y:.2f}/quintal<br>' +
                         '<b>WPI</b>: %{customdata:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_prices,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#e74c3c', width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond')
        ))
        
        fig.update_layout(
            title=f'Price Forecast - {commodity} (Next {months_ahead} Months)',
            xaxis_title='Date',
            yaxis_title='Price (₹ per quintal)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Use plotly's JSON encoder with engine='json' to avoid binary encoding
        import plotly
        return plotly.io.to_json(fig, engine='json')

# Global instance
price_visualizer = PriceVisualization()

