"""
Helper utility functions
"""
from datetime import datetime

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_year():
    """Get current year"""
    return datetime.now().year

def get_current_month():
    """Get current month"""
    return datetime.now().month

def format_currency(amount):
    """Format amount in Indian Rupees"""
    return f"₹{amount:,.2f}"

def get_month_name(month_num):
    """Convert month number to name"""
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return months[month_num] if 1 <= month_num <= 12 else 'Unknown'

# Districts in Maharashtra
MAHARASHTRA_DISTRICTS = [
    'Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara',
    'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli',
    'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban',
    'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar',
    'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg',
    'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal', 'Sambhajinagar'
]

# Common crops
CROP_COMMODITIES = ['Jowar', 'Wheat', 'Cotton', 'Sugarcane', 'Bajra', 'Rice', 'Maize']

