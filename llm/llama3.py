import requests
import json
from utils.logger import log_message, log_error

class LlamaClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.1-8b-instruct:free"
        log_message("LlamaClient initialized")
    
    def chat_completion(self, messages, max_tokens=500):
        """Make API call to LLaMA"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data)
            result = response.json()
            
            if response.status_code == 200:
                return result['choices'][0]['message']['content']
            else:
                log_error(f"API Error: {result}")
                return "I'm having technical difficulties."
        except Exception as e:
            log_error(f"LLaMA API Error: {str(e)}")
            return "Sorry, I'm experiencing issues."
    
    def detect_intent(self, user_message):
        """Detect user intent"""
        prompt = f"""
Classify this message into ONE intent:
- make_reservation: wants to book a table
- modify_reservation: wants to change booking
- cancel_reservation: wants to cancel booking
- restaurant_recommendation: wants restaurant suggestions
- general_info: asking about restaurants

Message: "{user_message}"
Respond with only the intent name.
"""
        messages = [{"role": "user", "content": prompt}]
        intent = self.chat_completion(messages, max_tokens=20)
        return intent.strip().lower()
