import json
import uuid
from datetime import datetime
from utils.logger import log_message, log_error

class ReservationTool:
    def __init__(self, data_file="data/restaurant_data.json"):
        self.data_file = data_file
        self.reservations = []  # In-memory storage for demo
        
    def load_restaurants(self):
        """Load restaurant data"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data.get('restaurants', [])
        except Exception as e:
            log_error(f"Failed to load restaurants: {str(e)}")
            return []
    
    def check_availability(self, restaurant_id, date, time, party_size):
        """Check if restaurant has availability"""
        restaurants = self.load_restaurants()
        
        for restaurant in restaurants:
            if restaurant['id'] == restaurant_id:
                # Simple availability check (in real app, check actual bookings)
                capacity = restaurant.get('capacity', 0)
                if party_size <= capacity:
                    return True
        return False
    
    def make_reservation(self, restaurant_id, date, time, party_size, customer_name, phone):
        """Create a new reservation"""
        if self.check_availability(restaurant_id, date, time, party_size):
            reservation = {
                'id': str(uuid.uuid4()),
                'restaurant_id': restaurant_id,
                'date': date,
                'time': time,
                'party_size': party_size,
                'customer_name': customer_name,
                'phone': phone,
                'status': 'confirmed',
                'created_at': datetime.now().isoformat()
            }
            
            self.reservations.append(reservation)
            log_message(f"Reservation created: {reservation['id']}")
            return reservation
        else:
            return None
    
    def get_restaurant_info(self, restaurant_id):
        """Get restaurant information"""
        restaurants = self.load_restaurants()
        for restaurant in restaurants:
            if restaurant['id'] == restaurant_id:
                return restaurant
        return None
