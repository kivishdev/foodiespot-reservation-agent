import json
from utils.logger import log_message, log_error

class RecommendationTool:
    def __init__(self, data_file="data/restaurant_data.json"):
        self.data_file = data_file
    
    def load_restaurants(self):
        """Load restaurant data"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data.get('restaurants', [])
        except Exception as e:
            log_error(f"Failed to load restaurants: {str(e)}")
            return []
    
    def recommend_by_cuisine(self, cuisine_type, max_results=5):
        """Recommend restaurants by cuisine"""
        restaurants = self.load_restaurants()
        matches = []
        
        for restaurant in restaurants:
            cuisine = restaurant.get('cuisine', '')
            
            # Handle both list and string cuisine types
            if isinstance(cuisine, list):
                # Check if cuisine_type matches any item in the list
                if any(cuisine_type.lower() in c.lower() for c in cuisine):
                    matches.append(restaurant)
            elif isinstance(cuisine, str):
                # Check if cuisine_type is in the string
                if cuisine_type.lower() in cuisine.lower():
                    matches.append(restaurant)
        
        # Sort by rating
        matches.sort(key=lambda x: x.get('rating', 0), reverse=True)
        return matches[:max_results]
    
    def recommend_by_location(self, location, max_results=5):
        """Recommend restaurants by location"""
        restaurants = self.load_restaurants()
        matches = []
        
        for restaurant in restaurants:
            location_field = restaurant.get('location', '')
            if location.lower() in location_field.lower():
                matches.append(restaurant)
        
        matches.sort(key=lambda x: x.get('rating', 0), reverse=True)
        return matches[:max_results]
    
    def get_all_restaurants(self):
        """Get all restaurants"""
        return self.load_restaurants()
    
    def format_restaurant_list(self, restaurants):
        """Format restaurant list for display"""
        if not restaurants:
            return "No restaurants found."
        
        result = "Here are the restaurants:\n\n"
        for restaurant in restaurants:
            # Handle cuisine display for both list and string
            cuisine = restaurant.get('cuisine', 'Unknown')
            if isinstance(cuisine, list):
                cuisine_str = ', '.join(cuisine)
            else:
                cuisine_str = cuisine
                
            result += f"🍽️ **{restaurant['name']}**\n"
            result += f"   📍 {restaurant.get('location', 'Location not specified')}\n"
            result += f"   🍴 {cuisine_str}\n"
            result += f"   ⭐ {restaurant.get('rating', 'No rating')}/5\n"
            
            # Handle capacity safely
            capacity = restaurant.get('capacity', 'Not specified')
            result += f"   👥 Capacity: {capacity}\n\n"
        
        return result
