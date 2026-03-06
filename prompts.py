"""
Prompt templates for the AI Travel Planner.
This module contains all the prompt templates used for different stages of travel planning.
"""

from langchain_core.prompts import PromptTemplate


# System prompt for extracting travel details from user input
TRAVEL_DETAILS_EXTRACTOR_PROMPT = PromptTemplate.from_template("""
You are a travel planning assistant. Extract structured travel details from the user's request.

User Request: {user_input}

Extract the following information:
- destination: Where the user wants to travel
- duration_days: Number of days for the trip
- budget: Budget level (budget/medium/high)
- travel_style: Travel style preference (budget/comfort/luxury)
- start_date: When they want to travel (if mentioned)
- special_requests: Any special requirements or preferences

Return the result as a JSON object with these exact keys.
If any information is missing, use "not_specified" as the value.

Example output:
{{
    "destination": "Paris, France",
    "duration_days": 5,
    "budget": "medium",
    "travel_style": "comfort",
    "start_date": "not_specified",
    "special_requests": "Interested in museums and local cuisine"
}}
""")


# Main travel planning prompt
TRAVEL_PLANNING_PROMPT = PromptTemplate.from_template("""
You are an expert travel planner with deep knowledge of destinations worldwide. 
Create a comprehensive, personalized travel plan based on the following details:

Travel Details:
- Destination: {destination}
- Duration: {duration_days} days
- Budget Level: {budget}
- Travel Style: {travel_style}
- Start Date: {start_date}
- Special Requests: {special_requests}

Generate a complete travel plan in JSON format with the following structure:

{{
    "destination": "destination name",
    "duration_days": number_of_days,
    "budget": "budget_level",
    "travel_style": "travel_style",
    "start_date": "start_date",
    
    "daily_plans": [
        {{
            "day": 1,
            "date": "YYYY-MM-DD",
            "theme": "Day theme (e.g., 'City Exploration')",
            "morning_activities": [
                {{
                    "name": "Activity name",
                    "description": "Detailed description",
                    "duration": "2-3 hours",
                    "cost": "Free/$20/$50"
                }}
            ],
            "afternoon_activities": [
                {{
                    "name": "Activity name", 
                    "description": "Detailed description",
                    "duration": "2-3 hours",
                    "cost": "Free/$30/$60"
                }}
            ],
            "evening_activities": [
                {{
                    "name": "Activity name",
                    "description": "Detailed description", 
                    "duration": "2-3 hours",
                    "cost": "Free/$25/$55"
                }}
            ],
            "restaurants": [
                {{
                    "name": "Restaurant name",
                    "cuisine": "Type of cuisine",
                    "price_range": "budget/medium/expensive",
                    "specialties": ["dish1", "dish2"],
                    "rating": 4.5
                }}
            ],
            "places_to_visit": [
                {{
                    "name": "Place name",
                    "description": "Why it's worth visiting",
                    "rating": 4.7,
                    "visit_duration": "2-3 hours",
                    "entry_fee": "Free/$15/$30",
                    "best_time": "Morning/Afternoon/Evening"
                }}
            ],
            "estimated_budget": "$X for the day",
            "travel_notes": "Important tips for the day"
        }}
    ],
    
    "hotel_recommendations": [
        {{
            "name": "Hotel name",
            "type": "budget/mid-range/luxury",
            "price_range": "$X per night",
            "rating": 4.3,
            "amenities": ["WiFi", "Breakfast", "Pool"],
            "location": "City center/Near attractions",
            "booking_link": "Optional booking link"
        }}
    ],
    
    "packing_checklist": [
        "Essential item 1",
        "Essential item 2",
        "Destination-specific item"
    ],
    
    "travel_tips": [
        "Important tip 1",
        "Cultural tip 2", 
        "Safety tip 3"
    ],
    
    "map_links": [
        "Google Maps link for city overview",
        "Google Maps link for attractions area"
    ],
    
    "total_estimated_cost": "$X total"
}}

IMPORTANT GUIDELINES:
1. Be realistic about timing and distances
2. Suggest activities that match the budget level
3. Include a mix of popular attractions and hidden gems
4. Provide practical, actionable advice
5. Consider travel time between locations
6. Include cultural experiences and local cuisine
7. Make the plan exciting but achievable
8. Ensure all JSON syntax is correct
9. Use realistic ratings (3.5-5.0) for places and restaurants
10. Include specific, actionable details

Return ONLY the JSON object, no additional text.
""")


# Hotel recommendations prompt
HOTEL_RECOMMENDATIONS_PROMPT = PromptTemplate.from_template("""
You are a hotel expert. Recommend 3-5 hotels for this travel destination:

Destination: {destination}
Budget Level: {budget}
Travel Style: {travel_style}
Duration: {duration_days} days

Provide hotel recommendations in JSON format:

{{
    "hotel_recommendations": [
        {{
            "name": "Hotel name",
            "type": "budget/mid-range/luxury", 
            "price_range": "$X per night",
            "rating": 4.5,
            "amenities": ["WiFi", "Breakfast", "Gym"],
            "location": "Specific location description",
            "booking_link": "Optional booking site link",
            "pros": ["Reason 1", "Reason 2"],
            "cons": ["Potential issue 1"]
        }}
    ]
}}

Include options that match the budget and travel style.
""")


# Packing checklist prompt
PACKING_CHECKLIST_PROMPT = PromptTemplate.from_template("""
You are a travel expert. Create a comprehensive packing checklist for:

Destination: {destination}
Duration: {duration_days} days
Travel Style: {travel_style}
Season/Time: {start_date}

Generate a packing checklist in JSON format:

{{
    "packing_checklist": [
        "Essential documents (passport, tickets, etc.)",
        "Clothing items specific to destination and season",
        "Electronics and chargers",
        "Toiletries and personal items",
        "Health and safety items",
        "Destination-specific items"
    ]
}}

Consider:
- Weather and climate
- Cultural dress codes
- Activities planned
- Duration of trip
""")


# Travel tips prompt
TRAVEL_TIPS_PROMPT = PromptTemplate.from_template("""
You are an experienced travel guide. Provide essential travel tips for:

Destination: {destination}
Duration: {duration_days} days
Budget Level: {budget}

Generate travel tips in JSON format:

{{
    "travel_tips": [
        "Transportation tips (how to get around)",
        "Money and payment advice", 
        "Cultural etiquette tips",
        "Safety and security advice",
        "Food and dining recommendations",
        "Best time to visit attractions",
        "Local customs to know",
        "Emergency information"
    ]
}}

Focus on practical, actionable advice that will enhance the travel experience.
""")


# Map links prompt
MAP_LINKS_PROMPT = PromptTemplate.from_template("""
Generate useful Google Maps links for a traveler visiting {destination}:

Destination: {destination}
Duration: {duration_days} days

Create REAL, WORKING Google Maps URLs for this specific destination. Use actual Google Maps URL patterns:

1. City overview: https://www.google.com/maps/place/{destination} (replace spaces with +)
2. Tourist attractions: https://www.google.com/maps/search/tourist+attractions+{destination}
3. Hotels: https://www.google.com/maps/search/hotels+{destination}
4. Restaurants: https://www.google.com/maps/search/restaurants+{destination}
5. Airport: https://www.google.com/maps/search/airport+{destination}

Return in JSON format:
{{
    "map_links": [
        "https://www.google.com/maps/place/[actual-destination-search]",
        "https://www.google.com/maps/search/tourist+attractions+[destination]", 
        "https://www.google.com/maps/search/hotels+[destination]",
        "https://www.google.com/maps/search/restaurants+[destination]",
        "https://www.google.com/maps/search/airport+[destination]"
    ]
}}

IMPORTANT: Create ACTUAL working URLs with the real destination name, not placeholder IDs!
""")


# Itinerary formatting prompt for display
ITINERARY_FORMATTING_PROMPT = PromptTemplate.from_template("""
You are a travel writer. Transform this structured travel plan into an engaging, readable format:

{travel_plan_json}

Create a beautiful, inspiring travel itinerary that:
1. Has a warm, exciting introduction
2. Organizes each day clearly with morning, afternoon, and evening
3. Includes practical tips and recommendations
4. Has a helpful conclusion
5. Uses emojis to make it visually appealing
6. Flows naturally and is easy to read

Make it sound like it's written by an experienced, enthusiastic travel agent.
""")


# Error handling prompt for when AI fails
ERROR_RECOVERY_PROMPT = PromptTemplate.from_template("""
The travel planning system encountered an issue. Create a helpful response for:

User Request: {user_input}
Error: {error_message}

Generate a friendly, helpful message that:
1. Acknowledges the issue
2. Suggests alternative ways to get help
3. Provides general travel advice for the destination if possible
4. Encourages the user to try again

Be supportive and constructive.
""")
