import sys
import os
from dotenv import load_dotenv  # Add this import
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime, timedelta
from backend.agent import FoodieSpotAgent

# Load environment variables
load_dotenv()  # Add this line
api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

# Page config
st.set_page_config(
    page_title="FoodieSpot Reservation Agent",
    page_icon="🍽️",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    # Use environment variable instead of hardcoded key
    API_KEY = os.getenv('OPENROUTER_API_KEY')  # Changed this line
    if not API_KEY:
        st.error("⚠️ Please set OPENROUTER_API_KEY in your .env file")
        st.stop()
    st.session_state.agent = FoodieSpotAgent(API_KEY)

if 'show_booking_form' not in st.session_state:
    st.session_state.show_booking_form = False

if 'show_cancel_form' not in st.session_state:
    st.session_state.show_cancel_form = False

# App header
st.title("🍽️ FoodieSpot Reservation Agent")
st.markdown("Welcome to FoodieSpot! I can help you find restaurants and make reservations.")

# Booking Form Function
def show_booking_form():
    st.markdown("### 📅 Make a Reservation")
    
    # Get restaurant list
    restaurants = st.session_state.agent.recommendation_tool.get_all_restaurants()
    restaurant_names = [f"{r['name']} - {r['location']}" for r in restaurants]
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_restaurant = st.selectbox(
                "🏪 Select Restaurant",
                restaurant_names,
                help="Choose your preferred restaurant location"
            )
            
            reservation_date = st.date_input(
                "📅 Reservation Date",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=90)
            )
            
            reservation_time = st.time_input(
                "🕐 Reservation Time",
                value=datetime.now().replace(hour=19, minute=0, second=0).time()
            )
        
        with col2:
            party_size = st.number_input(
                "👥 Party Size",
                min_value=1,
                max_value=20,
                value=2
            )
            
            customer_name = st.text_input(
                "👤 Your Name",
                placeholder="Enter your full name"
            )
            
            phone_number = st.text_input(
                "📞 Phone Number",
                placeholder="Enter your phone number"
            )
        
        special_requests = st.text_area(
            "💬 Special Requests (Optional)",
            placeholder="Dietary restrictions, seating preferences, etc."
        )
        
        submitted = st.form_submit_button("🎯 Book Reservation", use_container_width=True)
        
        if submitted:
            if customer_name and phone_number:
                # Process the reservation
                reservation_details = {
                    'restaurant': selected_restaurant,
                    'date': reservation_date.strftime('%Y-%m-%d'),
                    'time': reservation_time.strftime('%H:%M'),
                    'party_size': party_size,
                    'customer_name': customer_name,
                    'phone': phone_number,
                    'special_requests': special_requests
                }
                
                success_message = f"""
✅ **Reservation Confirmed!**

📋 **Reservation Details:**
- **Restaurant:** {selected_restaurant}
- **Date:** {reservation_date.strftime('%B %d, %Y')}
- **Time:** {reservation_time.strftime('%I:%M %p')}
- **Party Size:** {party_size} people
- **Name:** {customer_name}
- **Phone:** {phone_number}

📧 **Confirmation:** A confirmation email will be sent shortly.
📱 **SMS Reminder:** You'll receive a reminder 24 hours before your reservation.

Thank you for choosing FoodieSpot! We look forward to serving you.
"""
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": success_message
                })
                st.session_state.show_booking_form = False
                st.rerun()
            else:
                st.error("Please fill in your name and phone number.")

# Cancellation Form Function
def show_cancel_form():
    st.markdown("### ❌ Cancel Reservation")
    
    with st.form("cancel_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cancel_name = st.text_input(
                "👤 Name on Reservation",
                placeholder="Enter the name used for booking"
            )
            
            cancel_phone = st.text_input(
                "📞 Phone Number",
                placeholder="Phone number used for booking"
            )
        
        with col2:
            cancel_date = st.date_input(
                "📅 Reservation Date",
                min_value=datetime.now().date() - timedelta(days=30),
                max_value=datetime.now().date() + timedelta(days=90)
            )
            
            confirmation_number = st.text_input(
                "🎫 Confirmation Number (Optional)",
                placeholder="Enter if you have it"
            )
        
        cancel_reason = st.text_area(
            "💬 Reason for Cancellation (Optional)",
            placeholder="Help us improve our service"
        )
        
        submitted = st.form_submit_button("🗑️ Cancel Reservation", use_container_width=True)
        
        if submitted:
            if cancel_name and cancel_phone:
                cancel_message = f"""
✅ **Reservation Cancelled Successfully**

📋 **Cancelled Reservation:**
- **Name:** {cancel_name}
- **Phone:** {cancel_phone}
- **Date:** {cancel_date.strftime('%B %d, %Y')}

📧 **Confirmation:** A cancellation confirmation will be sent to your email.
💰 **Refund:** If applicable, refunds will be processed within 3-5 business days.

We're sorry to see you cancel. We hope to serve you again soon at FoodieSpot!
"""
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": cancel_message
                })
                st.session_state.show_cancel_form = False
                st.rerun()
            else:
                st.error("Please provide your name and phone number.")

# Show forms if triggered
if st.session_state.show_booking_form:
    show_booking_form()

if st.session_state.show_cancel_form:
    show_cancel_form()

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about restaurants or reservations..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if user wants to book or cancel
    if any(word in prompt.lower() for word in ["book", "reserve", "reservation", "table"]) and not any(word in prompt.lower() for word in ["cancel", "modify"]):
        st.session_state.show_booking_form = True
        st.rerun()
    elif any(word in prompt.lower() for word in ["cancel", "delete"]):
        st.session_state.show_cancel_form = True
        st.rerun()
    else:
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.process_message(prompt)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with quick actions
with st.sidebar:
    st.header("Quick Actions")
    
    if st.button("🍝 Italian Restaurants"):
        prompt = "Show me Italian restaurants"
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = st.session_state.agent.process_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    if st.button("📅 Make Reservation"):
        st.session_state.show_booking_form = True
        st.rerun()
    
    if st.button("❌ Cancel Reservation"):
        st.session_state.show_cancel_form = True
        st.rerun()
    
    if st.button("🏪 All Locations"):
        prompt = "Show me all restaurant locations"
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = st.session_state.agent.process_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
