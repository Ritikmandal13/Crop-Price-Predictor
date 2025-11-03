"""
State Configuration Module
Manages state-specific data and mappings for crop price prediction
"""

class StateConfig:
    """Configuration for Indian states and their agricultural data"""
    
    # Major agricultural states in India
    STATES = {
        'Maharashtra': {
            'code': 'MH',
            'major_crops': ['Jowar', 'Cotton', 'Sugarcane', 'Wheat', 'Bajra'],
            'region': 'Western',
            'data_available': True
        },
        'Punjab': {
            'code': 'PB',
            'major_crops': ['Wheat', 'Bajra', 'Cotton', 'Sugarcane'],
            'region': 'Northern',
            'data_available': True
        },
        'Karnataka': {
            'code': 'KA',
            'major_crops': ['Jowar', 'Cotton', 'Sugarcane', 'Wheat'],
            'region': 'Southern',
            'data_available': True
        },
        'Uttar Pradesh': {
            'code': 'UP',
            'major_crops': ['Wheat', 'Sugarcane', 'Bajra'],
            'region': 'Northern',
            'data_available': True
        },
        'Gujarat': {
            'code': 'GJ',
            'major_crops': ['Cotton', 'Wheat', 'Bajra'],
            'region': 'Western',
            'data_available': True
        },
        'Madhya Pradesh': {
            'code': 'MP',
            'major_crops': ['Jowar', 'Wheat', 'Cotton'],
            'region': 'Central',
            'data_available': True
        }
    }
    
    # All supported crops
    ALL_CROPS = ['Jowar', 'Wheat', 'Cotton', 'Sugarcane', 'Bajra']
    
    @classmethod
    def get_all_states(cls):
        """Get list of all available states"""
        return sorted(cls.STATES.keys())
    
    @classmethod
    def get_state_info(cls, state_name):
        """Get information about a specific state"""
        return cls.STATES.get(state_name, None)
    
    @classmethod
    def get_crops_for_state(cls, state_name):
        """Get list of major crops for a specific state"""
        state_info = cls.STATES.get(state_name)
        if state_info:
            return state_info['major_crops']
        return cls.ALL_CROPS
    
    @classmethod
    def is_data_available(cls, state_name):
        """Check if data is available for the state"""
        state_info = cls.STATES.get(state_name)
        return state_info['data_available'] if state_info else False
    
    @classmethod
    def get_data_path(cls, state_name, crop_name):
        """Get file path for state-specific crop data"""
        # Normalize state name (remove spaces for folder names)
        folder_name = state_name.replace(' ', '')
        return f"data/states/{folder_name}/{crop_name}.csv"
    
    @classmethod
    def get_fallback_path(cls, crop_name):
        """Get fallback data path (Maharashtra as default)"""
        return f"data/states/Maharashtra/{crop_name}.csv"
    
    @classmethod
    def get_states_by_region(cls, region):
        """Get states filtered by region"""
        return [name for name, info in cls.STATES.items() if info['region'] == region]

# Global instance
state_config = StateConfig()

