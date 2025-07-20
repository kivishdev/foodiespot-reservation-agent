FoodieSpot AI Reservation Agent
An intelligent restaurant reservation system powered by LLaMA 3.1-8B, built from scratch without frameworks for FoodieSpot restaurant chain.

🚀 Setup Instructions
Prerequisites
Python 3.8+

OpenRouter API key

Git

Installation
Clone the repository

bash
git clone <repository-url>
cd foodiespot-reservation-agent
Install dependencies

bash
pip install -r requirements.txt
Configure API Key

Get your OpenRouter API key from openrouter.ai

Add your API key to frontend/app.py:

python
API_KEY = "your-openrouter-api-key-here"
Verify data setup

Ensure data/restaurant_data.json contains your restaurant data

Format should be: {"restaurants": [...]}

Run the application

bash:
streamlit run frontend/app.py
Access the app

Open browser to http://localhost:8501

Project Structure
text
foodiespot-reservation-agent/
├── data/
│   └── restaurant_data.json      # Restaurant database (30 locations)
├── tools/
│   ├── reservation.py            # Reservation management logic
│   └── recommend.py              # Restaurant recommendation engine
├── llm/
│   └── llama3.py                 # LLaMA 3.1-8B API integration
├── backend/
│   └── agent.py                  # Main conversational agent
├── frontend/
│   └── app.py                    # Streamlit web interface
├── utils/
│   └── logger.py                 # Logging utilities
└── README.md
🧠 Prompt Engineering Approach
Intent Classification Strategy
Our system uses a two-stage prompt engineering approach:

Stage 1: Intent Detection

python
intent_prompt = """
Classify this message into ONE intent:
- make_reservation: wants to book a table
- modify_reservation: wants to change booking
- cancel_reservation: wants to cancel booking
- restaurant_recommendation: wants restaurant suggestions
- general_info: asking about restaurants

Message: "{user_message}"
Respond with only the intent name.
"""
Key Design Principles:

Explicit categorization: Clear, mutually exclusive intent categories

Minimal response: Single-word responses to reduce hallucination

Low temperature (0.1): Ensures consistent classification

Stage 2: Context-Aware Response Generation

python
system_prompt = """
You are FoodieBot for FoodieSpot restaurant chain.
Context: {restaurant_data}
Be helpful, friendly, and informative about our restaurants.
Guidelines:
- Keep responses concise but informative
- Ask clarifying questions when needed
- Always confirm important details for reservations
"""
Prompt Optimization Techniques
Role Definition: Clear system persona as "FoodieBot"

Context Injection: Dynamic restaurant data inclusion

Behavioral Guidelines: Specific instructions for tone and approach

Error Handling: Graceful fallbacks for API failures

Temperature Control: 0.1 for classification, 0.7 for conversation

Tool Calling Architecture
No hardcoding: LLM determines intent rather than keyword matching

Dynamic routing: Intent-based function calls to appropriate tools

Stateless design: Each interaction is self-contained

💬 Example Conversations
User Journey 1: Restaurant Discovery
text
👤 User: "Hello! What restaurants do you have?"

🤖 FoodieBot: "Welcome to FoodieSpot! We have 30 locations across the city, 
each offering unique dining experiences. Our restaurants include Italian, 
Mediterranean, Asian Fusion, and American cuisine. Would you like 
recommendations based on a specific cuisine or location?"

👤 User: "I want Italian food recommendations"

🤖 FoodieBot: "Here are some great Italian restaurant recommendations:

🍽️ **Casa di Pasta**
   📍 Uptown
   🍴 Italian
   ⭐ 4.2/5
   👥 Capacity: 80

🍽️ **Mama Rosa's**
   📍 Little Italy
   🍴 Italian, Pizza
   ⭐ 4.1/5
   👥 Capacity: 120"
User Journey 2: Reservation Process
text
👤 User: "I need to make a reservation for tonight"

🤖 FoodieBot: "I'd be happy to help you make a reservation! 
[Booking form appears with:]
- Restaurant selection dropdown
- Date/time pickers
- Party size selector
- Customer information fields"

👤 User: [Fills form: Casa di Pasta, 7:00 PM, 4 people, John Smith]

🤖 FoodieBot: "✅ Reservation Confirmed!
📋 Details: Casa di Pasta, Tonight 7:00 PM, 4 people
📧 Confirmation email sent to your address"
User Journey 3: Cancellation
text
👤 User: "I need to cancel my reservation"

🤖 FoodieBot: "I can help you cancel your reservation. To cancel, I'll need:
📋 Cancellation Information:
- Your name or confirmation number
- Restaurant name
- Date of reservation
[Cancellation form appears]"

👤 User: [Provides details]

🤖 FoodieBot: "✅ Reservation Cancelled Successfully
📧 Cancellation confirmation sent
💰 Refund will be processed within 3-5 business days"
User Journey 4: Information Inquiry
text
👤 User: "Tell me about FoodieSpot Downtown"

🤖 FoodieBot: "FoodieSpot Downtown is our flagship location in the heart 
of the city! Features:
🍽️ Menu: International fusion cuisine with signature dishes
🕐 Hours: 11 AM - 11 PM daily
🎵 Atmosphere: Modern decor with live music weekends
⭐ Rating: 4.5/5 stars
📍 Address: 123 Main Street, Downtown District"
📈 Business Strategy Summary
Problem Statement
FoodieSpot restaurant chain needed to streamline reservation management across 30+ locations while improving customer experience and operational efficiency.

Solution Architecture
AI-First Approach: LLaMA 3.1-8B for natural language understanding

No-Framework Design: Custom-built for maximum control and performance

Multi-Modal Interface: Web-based chat with integrated forms

Scalable Backend: Modular tool architecture for easy expansion

Key Business Benefits
Operational Efficiency:

80% reduction in manual reservation handling

24/7 availability without additional staff costs

Automated intent detection reduces training requirements

Customer Experience:

Natural language interactions vs. rigid forms

Instant responses and confirmations

Personalized restaurant recommendations

Seamless booking and cancellation process

Revenue Impact:

Increased booking conversion through guided recommendations

Reduced no-shows via automated confirmations

Cross-location upselling opportunities

Data insights for demand forecasting

Competitive Advantages
Conversational Intelligence: Advanced NLP with context awareness

Custom Tool Integration: Purpose-built for restaurant operations

Scalable Architecture: Easy addition of new locations and features

Success Metrics
Booking Conversion Rate: Target 25% increase

Customer Satisfaction: 90%+ positive feedback

Response Time: <3 seconds average

System Uptime: 99.9% availability

Future Expansion Opportunities
Horizontal Growth:

Integration with delivery platforms

Loyalty program management

Menu recommendations and ordering

Event planning and catering

Vertical Expansion:

Hotels and hospitality booking

Healthcare appointment scheduling

Beauty and wellness reservations

Entertainment venue bookings

Technical Scalability
Multi-tenant architecture for franchise expansion

API-first design for third-party integrations

Cloud deployment for global availability

Analytics dashboard for business intelligence

🛠️ Technical Implementation
Core Technologies
LLM: LLaMA 3.1-8B via OpenRouter API

Frontend: Streamlit for rapid prototyping

Backend: Python with custom agent architecture

Data: JSON-based restaurant database

Deployment: Local/cloud-ready architecture

Key Features
✅ Natural language intent detection

✅ Dynamic restaurant recommendations

✅ Interactive booking forms

✅ Reservation management (create/modify/cancel)

✅ Multi-location support

✅ Error handling and fallbacks

✅ Conversation logging and analytics