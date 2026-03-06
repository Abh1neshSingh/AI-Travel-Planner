"""
AI Travel Planner - Main Streamlit Application
A beautiful, ChatGPT-style travel planning assistant powered by AI.
"""

import streamlit as st
import streamlit.components.v1 as components
import time
import json
from datetime import datetime
from typing import Dict, Any, List

# Local imports
from travel_agent import create_travel_agent, TravelAgent
from utils import (
    TravelPlan, TravelRequest, validate_travel_request,
    get_sample_destinations, get_budget_options, get_travel_style_options,
    calculate_trip_summary
)
from pdf_export import export_travel_plan_to_pdf

# Configure Streamlit page
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS for beautiful styling
def load_custom_css():
    """Load custom CSS for the application."""
    st.markdown("""
    <style>
        /* Main styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem 1rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 1.5rem;
            width: 100%;
            box-sizing: border-box;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
            margin: 0 0 0.5rem 0;
            word-wrap: break-word;
        }
        
        .main-header p {
            font-size: 0.9rem;
            margin: 0.25rem 0;
            word-wrap: break-word;
        }
        
        .chat-message {
            padding: 0.75rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            max-width: 95%;
            word-wrap: break-word;
            box-sizing: border-box;
        }
        
        .user-message {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            margin-right: auto;
        }
        
        .day-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 100%;
            box-sizing: border-box;
        }
        
        .hotel-card {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .tip-card {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .sidebar-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .loading-spinner {
            text-align: center;
            padding: 2rem;
        }
        
        .success-message {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .error-message {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                padding: 1rem 0.75rem;
                margin-bottom: 1rem;
            }
            
            .main-header h1 {
                font-size: 1.5rem;
            }
            
            .main-header p {
                font-size: 0.8rem;
            }
            
            .chat-message {
                max-width: 98%;
                padding: 0.5rem;
            }
            
            .day-card {
                padding: 0.75rem;
            }
            
            .hotel-card, .tip-card {
                padding: 0.75rem;
            }
        }
        
        @media (max-width: 480px) {
            .main-header h1 {
                font-size: 1.3rem;
            }
            
            .main-header p {
                font-size: 0.75rem;
            }
            
            .chat-message {
                max-width: 100%;
                padding: 0.5rem;
            }
        }
        
        /* Hide streamlit elements */
        .stDeployButton {
            display: none;
        }
        
        /* Custom button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        
        /* Select box styling */
        .stSelectbox > div > div > select {
            border-radius: 5px;
            border: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'travel_agent' not in st.session_state:
        st.session_state.travel_agent = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'assistant',
                'content': '👋 Hello! I\'m your AI Travel Assistant! 🌍✈️\n\nI can help you create amazing travel plans in seconds! Just tell me:\n• Where you want to go\n• How many days\n• Your budget preference\n\nFor example: "I want to plan a 5-day trip to Paris with a medium budget"\n\nOr use the sidebar to set your preferences and click "Generate Travel Plan"!',
                'timestamp': datetime.now()
            }
        ]
    if 'current_travel_plan' not in st.session_state:
        st.session_state.current_travel_plan = None
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'destination': '',
            'duration_days': 3,
            'budget': 'medium',
            'travel_style': 'comfort',
            'start_date': '',
            'special_requests': ''
        }


def create_travel_agent_if_needed():
    """Create travel agent if not already created."""
    if st.session_state.travel_agent is None:
        with st.spinner("🤖 Initializing AI Travel Agent..."):
            try:
                st.session_state.travel_agent = create_travel_agent()
                st.success("✅ AI Travel Agent ready!")
            except Exception as e:
                st.error(f"❌ Failed to initialize AI Agent: {e}")
                st.session_state.travel_agent = None


def render_header():
    """Render the main header of the application."""
    st.markdown("""
    <div class="main-header">
        <h1>✈️ AI Travel Planner</h1>
        <p>Your intelligent travel companion for creating perfect itineraries</p>
        <p>🌍 Personalized • 🤖 AI-Powered • 📋 Comprehensive Plans</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with user preferences."""
    st.sidebar.markdown("## 🎯 Travel Preferences")
    
    # Destination input with suggestions
    destinations = get_sample_destinations()
    destination = st.sidebar.selectbox(
        "📍 Destination",
        options=["Custom"] + destinations,
        help="Choose your travel destination"
    )
    
    if destination == "Custom":
        destination = st.sidebar.text_input(
            "Enter destination:",
            value=st.session_state.user_preferences['destination'],
            placeholder="e.g., Paris, France"
        )
    
    # Duration
    duration = st.sidebar.slider(
        "📅 Duration (days)",
        min_value=1,
        max_value=30,
        value=st.session_state.user_preferences['duration_days'],
        help="How many days do you want to travel?"
    )
    
    # Budget
    budget_options = get_budget_options()
    budget = st.sidebar.selectbox(
        "💰 Budget",
        options=list(budget_options.keys()),
        index=1,
        format_func=lambda x: f"{x.title()} - {budget_options[x]}",
        help="Select your budget level"
    )
    
    # Travel style
    style_options = get_travel_style_options()
    travel_style = st.sidebar.selectbox(
        "🎨 Travel Style",
        options=list(style_options.keys()),
        index=1,
        format_func=lambda x: f"{x.title()} - {style_options[x]}",
        help="Choose your travel style"
    )
    
    # Start date
    start_date = st.sidebar.date_input(
        "🗓️ Start Date",
        help="When do you want to start your trip?"
    )
    
    # Special requests
    special_requests = st.sidebar.text_area(
        "📝 Special Requests",
        value=st.session_state.user_preferences['special_requests'],
        placeholder="Any special interests, dietary requirements, accessibility needs, etc.",
        help="Tell us about any special preferences"
    )
    
    # Update session state
    st.session_state.user_preferences.update({
        'destination': destination,
        'duration_days': duration,
        'budget': budget,
        'travel_style': travel_style,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'special_requests': special_requests
    })
    
    # Generate plan button
    if st.sidebar.button("🚀 Generate Travel Plan", type="primary"):
        if destination and duration > 0:
            generate_travel_plan()
        else:
            st.sidebar.error("Please fill in destination and duration")


def render_chat_interface():
    """Render the chat interface."""
    st.markdown("## 💬 Chat with AI Travel Assistant")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 AI Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your travel plans...")
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Process with AI agent
        if st.session_state.travel_agent:
            with st.spinner("🤔 Thinking..."):
                try:
                    # Check for greetings and casual conversation first
                    user_lower = user_input.lower().strip()
                    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy"]
                    casual_responses = [
                        "how are you", "what's up", "what can you do", "help", "thanks", "thank you", 
                        "bye", "goodbye", "book ticket", "booking", "tickets"
                    ]
                    
                    # Handle greetings
                    if any(greeting in user_lower for greeting in greetings):
                        response = "👋 Hello! I'm your AI Travel Assistant! I'm here to help you plan amazing trips. "
                        response += "Just tell me where you want to go, for how many days, and your budget. "
                        response += "For example: 'I want to plan a 5-day trip to Paris with a medium budget' 🌍✈️"
                    
                    # Handle casual questions
                    elif any(casual in user_lower for casual in casual_responses):
                        if "how are you" in user_lower:
                            response = "I'm doing great, thanks for asking! 😊 I'm excited to help you plan your next adventure! "
                            response += "Where would you like to travel to?"
                        elif "what can you do" in user_lower or "help" in user_lower:
                            response = "I can help you create complete travel plans! 🌍 I'll generate:\n"
                            response += "• Day-by-day itineraries\n• Hotel recommendations\n• Restaurant suggestions\n• Packing checklists\n• Travel tips\n"
                            response += "Just tell me your destination, duration, and budget!"
                        elif "book" in user_lower or "ticket" in user_lower:
                            response = "I can help you plan your perfect trip, but I don't actually book tickets or hotels. "
                            response += "I'll create a detailed itinerary with recommendations, and then you can book through your preferred travel sites! "
                            response += "Where would you like to go?"
                        elif "thanks" in user_lower or "thank you" in user_lower:
                            response = "You're welcome! 😊 Let me know if you need help planning any trips!"
                        elif "bye" in user_lower or "goodbye" in user_lower:
                            response = "Goodbye! Have a wonderful day and happy travels! ✈️"
                        else:
                            response = "I'm here to help with travel planning! Tell me about your dream destination! 🌍"
                    
                    # Handle travel requests
                    else:
                        # Extract travel details from user input
                        details = st.session_state.travel_agent.extract_travel_details(user_input)
                        
                        # Debug: Print extracted details (remove in production)
                        print(f"Extracted details: {details}")
                        
                        # Check if user provided enough information to generate a plan
                        destination = details.get('destination', '').strip()
                        duration = details.get('duration_days', 0)
                        budget = details.get('budget', '').strip()
                        travel_style = details.get('travel_style', '').strip()
                        
                        # Create response based on context and extracted information
                        if st.session_state.current_travel_plan:
                            # If we have a current plan, provide specific advice
                            response = f"I see you're asking about {details.get('destination', 'your trip')}. "
                            response += "Based on your current travel plan, I can help you with specific details. "
                            response += "Would you like me to modify your plan or provide more information about specific aspects?"
                        elif destination and destination != "not_specified":
                            # If user provided destination, acknowledge and try to generate plan
                            if duration > 0:
                                try:
                                    # Update session state with extracted details
                                    st.session_state.user_preferences.update({
                                        'destination': destination,
                                        'duration_days': duration,
                                        'budget': budget if budget and budget != "not_specified" else st.session_state.user_preferences.get('budget', 'medium'),
                                        'travel_style': travel_style if travel_style and travel_style != "not_specified" else st.session_state.user_preferences.get('travel_style', 'comfort'),
                                        'special_requests': details.get('special_requests', '')
                                    })
                                    
                                    # Generate travel plan automatically
                                    travel_request = TravelRequest(**st.session_state.user_preferences)
                                    travel_plan = st.session_state.travel_agent.generate_travel_plan(travel_request)
                                    travel_plan = st.session_state.travel_agent.enhance_travel_plan(travel_plan)
                                    st.session_state.current_travel_plan = travel_plan
                                    
                                    response = f"🎉 Perfect! I've created a fantastic {travel_plan.duration_days}-day travel plan for {travel_plan.destination}! "
                                    response += "Check out your personalized itinerary below. You can ask me to modify anything or provide more details!"
                                    
                                except Exception as plan_error:
                                    # If plan generation fails, acknowledge what we understood and ask for more
                                    response = f"Great! I understand you want to go to {destination} for {duration} days. "
                                    if not budget or budget == "not_specified":
                                        response += "What's your budget preference (budget/medium/high)? "
                                    response += "Let me know and I'll create your perfect itinerary!"
                            else:
                                # Got destination but no duration
                                response = f"Great choice! {destination} is an amazing destination. "
                                response += "How many days would you like to stay? Also, what's your budget preference?"
                        else:
                            # If no destination detected, provide helpful guidance
                            response = "I'd love to help you plan your perfect trip! 🌍 "
                            response += "Just tell me: Where would you like to go, for how many days, and what's your budget? "
                            response += "For example: 'I want to plan a 5-day trip to Paris with a medium budget'"
                    
                    # Add assistant response to chat
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response,
                        'timestamp': datetime.now()
                    })
                    
                    # Rerun to update the chat
                    st.rerun()
                    
                except Exception as e:
                    # Handle errors gracefully
                    error_response = f"❌ Sorry, I encountered an error: {str(e)}. "
                    
                    if "API" in str(e).upper() or "key" in str(e).lower():
                        error_response += "Please check your API key in the .env file. "
                        error_response += "You can still use the sidebar to generate travel plans!"
                    else:
                        error_response += "Please try again or use the sidebar to set your preferences."
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': error_response,
                        'timestamp': datetime.now()
                    })
                    
                    st.rerun()
        else:
            # AI Agent not initialized - provide helpful response
            fallback_response = "🤖 I'm having trouble connecting to my AI brain right now. "
            fallback_response += "This might be due to a missing API key. "
            fallback_response += "Please use the sidebar to set your travel preferences and click 'Generate Travel Plan' - it works perfectly! "
            fallback_response += "Or check your .env file for the MISTRAL_API_KEY."
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': fallback_response,
                'timestamp': datetime.now()
            })
            
            st.rerun()


def generate_travel_plan():
    """Generate a travel plan based on user preferences."""
    try:
        # Create travel request
        travel_request = TravelRequest(**st.session_state.user_preferences)
        
        # Validate request
        errors = validate_travel_request(travel_request)
        if errors:
            st.error(f"Please fix these issues: {', '.join(errors)}")
            return
        
        # Generate plan with loading indicator
        with st.spinner("🌍 Creating your personalized travel plan..."):
            # Generate the travel plan
            travel_plan = st.session_state.travel_agent.generate_travel_plan(travel_request)
            
            # Enhance the plan with additional features
            travel_plan = st.session_state.travel_agent.enhance_travel_plan(travel_plan)
            
            # Store in session state
            st.session_state.current_travel_plan = travel_plan
            
            # Add success message to chat
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"🎉 I've created a fantastic {travel_plan.duration_days}-day travel plan for {travel_plan.destination}! Check out the detailed itinerary below.",
                'timestamp': datetime.now()
            })
            
            st.success("✅ Travel plan generated successfully!")
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error generating travel plan: {e}")
        # Add error message to chat
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"Sorry, I encountered an error while generating your travel plan: {e}. Please try again.",
            'timestamp': datetime.now()
        })


def render_travel_plan():
    """Render the generated travel plan."""
    if not st.session_state.current_travel_plan:
        return
    
    plan = st.session_state.current_travel_plan
    
    # Plan header
    st.markdown(f"## 🌍 Your Travel Plan: {plan.destination}")
    
    # Plan summary
    summary = calculate_trip_summary(plan)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Days", summary['days_planned'])
    with col2:
        st.metric("🏛️ Places", summary['total_places'])
    with col3:
        st.metric("🍽️ Restaurants", summary['total_restaurants'])
    with col4:
        st.metric("🏨 Hotels", summary['hotels_recommended'])
    
    # Export buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export to PDF", type="primary"):
            export_to_pdf()
    with col2:
        if st.button("🔄 Generate New Plan"):
            st.session_state.current_travel_plan = None
            st.rerun()
    
    # Daily itinerary
    st.markdown("### 📅 Daily Itinerary")
    
    for day_plan in plan.daily_plans:
        with st.expander(f"Day {day_plan.day}: {day_plan.theme or 'Travel Day'}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                if day_plan.morning_activities:
                    st.markdown("🌅 **Morning**")
                    for activity in day_plan.morning_activities:
                        st.markdown(f"• **{activity.name}** - {activity.description}")
                        if activity.duration:
                            st.markdown(f"  *Duration: {activity.duration}*")
                        if activity.cost:
                            st.markdown(f"  *Cost: {activity.cost}*")
                
                if day_plan.afternoon_activities:
                    st.markdown("☀️ **Afternoon**")
                    for activity in day_plan.afternoon_activities:
                        st.markdown(f"• **{activity.name}** - {activity.description}")
                        if activity.duration:
                            st.markdown(f"  *Duration: {activity.duration}*")
                        if activity.cost:
                            st.markdown(f"  *Cost: {activity.cost}*")
            
            with col2:
                if day_plan.evening_activities:
                    st.markdown("🌆 **Evening**")
                    for activity in day_plan.evening_activities:
                        st.markdown(f"• **{activity.name}** - {activity.description}")
                        if activity.duration:
                            st.markdown(f"  *Duration: {activity.duration}*")
                        if activity.cost:
                            st.markdown(f"  *Cost: {activity.cost}*")
                
                if day_plan.restaurants:
                    st.markdown("🍽️ **Recommended Restaurants**")
                    for restaurant in day_plan.restaurants:
                        st.markdown(f"• **{restaurant.name}** ({restaurant.cuisine})")
                        st.markdown(f"  *Rating: {restaurant.rating}/5 • {restaurant.price_range}*")
                        if restaurant.specialties:
                            specialties = ", ".join(restaurant.specialties)
                            st.markdown(f"  *Specialties: {specialties}*")
            
            # Places to visit
            if day_plan.places_to_visit:
                st.markdown("🏛️ **Places to Visit**")
                for place in day_plan.places_to_visit:
                    st.markdown(f"• **{place.name}** - {place.description}")
                    st.markdown(f"  *Rating: {place.rating}/5*")
                    if place.visit_duration:
                        st.markdown(f"  *Visit duration: {place.visit_duration}*")
                    if place.entry_fee:
                        st.markdown(f"  *Entry fee: {place.entry_fee}*")
            
            # Day budget and tips
            if day_plan.estimated_budget:
                st.markdown(f"💰 **Estimated Budget:** {day_plan.estimated_budget}")
            
            if day_plan.travel_notes:
                st.markdown(f"💡 **Travel Tips:** {day_plan.travel_notes}")
    
    # Hotel recommendations
    if plan.hotel_recommendations:
        st.markdown("### 🏨 Hotel Recommendations")
        
        for hotel in plan.hotel_recommendations:
            with st.expander(f"{hotel.name} ({hotel.type})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Type:** {hotel.type}")
                    st.markdown(f"**Price:** {hotel.price_range}")
                    st.markdown(f"**Rating:** {hotel.rating}/5")
                    st.markdown(f"**Location:** {hotel.location}")
                
                with col2:
                    if hotel.amenities:
                        st.markdown("**Amenities:**")
                        for amenity in hotel.amenities:
                            st.markdown(f"• {amenity}")
    
    # Additional information
    col1, col2 = st.columns(2)
    
    with col1:
        if plan.packing_checklist:
            st.markdown("### 🎒 Packing Checklist")
            for item in plan.packing_checklist:
                st.markdown(f"☐ {item}")
    
    with col2:
        if plan.travel_tips:
            st.markdown("### 💡 Travel Tips")
            for tip in plan.travel_tips:
                st.markdown(f"• {tip}")
    
    # Map links
    if plan.map_links:
        st.markdown("### 🗺️ Map Links")
        for i, link in enumerate(plan.map_links, 1):
            st.markdown(f"{i}. {link}")


def export_to_pdf():
    """Export the current travel plan to PDF."""
    try:
        if not st.session_state.current_travel_plan:
            st.error("No travel plan to export")
            return
        
        with st.spinner("📄 Generating PDF..."):
            pdf_bytes = export_travel_plan_to_pdf(st.session_state.current_travel_plan)
            
            # Create download button
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"travel_plan_{st.session_state.current_travel_plan.destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            
        st.success("✅ PDF generated successfully!")
        
    except Exception as e:
        st.error(f"❌ Error generating PDF: {e}")


def main():
    """Main application function."""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Create travel agent
    create_travel_agent_if_needed()
    
    # Render components
    render_header()
    
    # Main layout
    if st.session_state.current_travel_plan:
        render_travel_plan()
    else:
        # Show chat interface when no plan is generated
        render_chat_interface()
    
    # Always show sidebar
    render_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>Intelligent travel planning powered by AI</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
