from llm.llama3 import LlamaClient
from tools.reservation import ReservationTool
from tools.recommend import RecommendationTool
from utils.logger import log_message, log_error

class FoodieSpotAgent:
    def __init__(self, api_key):
        self.llama_client = LlamaClient(api_key)
        self.reservation_tool = ReservationTool()
        self.recommendation_tool = RecommendationTool()
        log_message("FoodieSpot Agent initialized")
    
    def process_message(self, user_message):
        """Main function to process user messages"""
        log_message(f"Processing: {user_message}")
        
        # Step 1: Detect intent
        intent = self.llama_client.detect_intent(user_message)
        log_message(f"Intent detected: {intent}")
        
        # Step 2: Call appropriate tool based on intent
        if "recommendation" in intent:
            return self.handle_recommendation(user_message)
        elif "make_reservation" in intent:
            return self.handle_reservation(user_message)
        elif "cancel_reservation" in intent:
            return self.handle_cancellation(user_message)
        elif "modify_reservation" in intent:
            return self.handle_modification(user_message)
        else:
            return self.handle_general_info(user_message)
    
    def handle_recommendation(self, user_message):
        """Handle restaurant recommendations"""
        # Extract cuisine from message using LLaMA
        cuisine_prompt = f"""
        Extract the cuisine type from this message. If no specific cuisine mentioned, return 'any'.
        Message: "{user_message}"
        Respond with only the cuisine name.
        """
        cuisine = self.llama_client.chat_completion([{"role": "user", "content": cuisine_prompt}], max_tokens=20)
        
        if "any" in cuisine.lower():
            restaurants = self.recommendation_tool.get_all_restaurants()[:5]
        else:
            restaurants = self.recommendation_tool.recommend_by_cuisine(cuisine.strip())
        
        if restaurants:
            formatted_list = self.recommendation_tool.format_restaurant_list(restaurants)
            return f"Here are some great restaurant recommendations:\n\n{formatted_list}"
        else:
            return "I couldn't find any restaurants matching your preferences. Would you like to see all our locations?"
    
    def handle_reservation(self, user_message):
        """Handle NEW reservation requests"""
        restaurants = self.recommendation_tool.get_all_restaurants()
        restaurant_names = [r['name'] for r in restaurants[:5]]
        
        response = "I'd be happy to help you make a **NEW reservation**! Here are some of our popular locations:\n\n"
        for i, name in enumerate(restaurant_names, 1):
            response += f"{i}. {name}\n"
        
        response += "\n📅 **For your new reservation, please tell me:**\n- Which restaurant?\n- What date and time?\n- How many people?\n- Any special requests?"
        return response
    
    def handle_cancellation(self, user_message):
        """Handle reservation cancellations"""
        return """I can help you cancel your reservation. To cancel, I'll need:

📋 **Cancellation Information:**
- Your name or confirmation number
- Restaurant name  
- Date of reservation

**Current Reservations:**
If you don't have your confirmation details, please provide:
- Name used for booking
- Phone number
- Approximate date

Please provide these details and I'll help you cancel your reservation right away.

💡 **Note:** Cancellations made 24 hours in advance help us better serve other guests!"""

    def handle_modification(self, user_message):
        """Handle reservation modifications"""
        return """I'd be happy to help you modify your reservation! 

📝 **To modify your booking, I need:**
- Your current reservation details (name/confirmation number)
- Restaurant name and current date/time
- What you'd like to change:
  - New date
  - New time  
  - Party size
  - Special requests

**Modification Options:**
✅ Change date/time
✅ Adjust party size  
✅ Add special dietary requirements
✅ Request specific seating

Please provide your current reservation details and what you'd like to change."""
    
    def handle_general_info(self, user_message):
        """Handle general information requests"""
        # Get restaurant context
        restaurants = self.recommendation_tool.get_all_restaurants()
        context = f"FoodieSpot has {len(restaurants)} locations across the city."
        
        # Generate response with LLaMA
        system_prompt = f"""
        You are FoodieBot for FoodieSpot restaurant chain.
        Context: {context}
        Be helpful, friendly, and informative about our restaurants.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        return self.llama_client.chat_completion(messages)
