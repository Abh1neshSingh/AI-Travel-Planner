"""
AI Travel Agent - Core LangChain logic for travel planning.
This module handles all AI interactions and travel plan generation.
"""

import os
import json
import logging
import re
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# LangChain imports
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# Local imports
from utils import TravelPlan, TravelRequest, validate_travel_request
from prompts import (
    TRAVEL_DETAILS_EXTRACTOR_PROMPT,
    TRAVEL_PLANNING_PROMPT,
    HOTEL_RECOMMENDATIONS_PROMPT,
    PACKING_CHECKLIST_PROMPT,
    TRAVEL_TIPS_PROMPT,
    MAP_LINKS_PROMPT,
    ERROR_RECOVERY_PROMPT
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TravelAgent:
    """
    Main AI Travel Agent class that handles all travel planning operations.
    
    This class uses LangChain and LLM APIs to generate comprehensive travel plans
    based on user preferences and requirements.
    """
    
    def __init__(self, model_name: str = "open-mixtral-8x22b"):
        """
        Initialize the Travel Agent.
        
        Args:
            model_name: Name of the LLM model to use
        """
        self.model_name = model_name
        self.llm = None
        self.json_parser = JsonOutputParser()
        
        # Initialize the LLM
        self._initialize_llm()
        
        # Set up the processing chains
        self._setup_chains()
    
    def _initialize_llm(self):
        """Initialize the language model."""
        try:
            # Check for API key in multiple sources (local env and Streamlit secrets)
            api_key = os.getenv("MISTRAL_API_KEY")
            
            # If not found in environment, try Streamlit secrets (for deployment)
            if not api_key:
                try:
                    import streamlit as st
                    api_key = st.secrets.get("MISTRAL_API_KEY")
                    logger.info("Using API key from Streamlit secrets")
                except Exception as secret_error:
                    logger.warning(f"Could not access Streamlit secrets: {secret_error}")
            
            if not api_key or api_key == "your_mistral_api_key_here":
                logger.warning("MISTRAL_API_KEY not found or not configured in environment variables")
                # Create a mock agent for demo purposes
                self.llm = None
                return
            
            # Initialize Mistral AI model
            self.llm = ChatMistralAI(model=self.model_name, temperature=0.7, mistral_api_key=api_key)
            logger.info(f"Initialized {self.model_name} model")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    def _setup_chains(self):
        """Set up the LangChain processing chains."""
        if not self.llm:
            logger.warning("LLM not initialized - chains will not be available")
            self.details_chain = None
            self.planning_chain = None
            self.hotel_chain = None
            self.packing_chain = None
            self.tips_chain = None
            self.maps_chain = None
            self.error_chain = None
            return
        
        # Travel details extraction chain
        self.details_chain = TRAVEL_DETAILS_EXTRACTOR_PROMPT | self.llm | self.json_parser
        
        # Main travel planning chain
        self.planning_chain = TRAVEL_PLANNING_PROMPT | self.llm | self.json_parser
        
        # Additional feature chains
        self.hotel_chain = HOTEL_RECOMMENDATIONS_PROMPT | self.llm | self.json_parser
        self.packing_chain = PACKING_CHECKLIST_PROMPT | self.llm | self.json_parser
        self.tips_chain = TRAVEL_TIPS_PROMPT | self.llm | self.json_parser
        self.maps_chain = MAP_LINKS_PROMPT | self.llm | self.json_parser
        self.error_chain = ERROR_RECOVERY_PROMPT | self.llm
    
    def extract_travel_details(self, user_input: str) -> Dict[str, Any]:
        """
        Extract structured travel details from user input.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Dictionary containing extracted travel details
        """
        try:
            logger.info(f"Extracting details from: {user_input}")
            
            if not self.details_chain:
                # Fallback extraction using simple patterns
                return self._fallback_extract_details(user_input)
            
            result = self.details_chain.invoke({"user_input": user_input})
            logger.info("Successfully extracted travel details")
            
            return result
            
        except Exception as e:
            logger.error(f"Error extracting travel details: {e}")
            return self._fallback_extract_details(user_input)
    
    def generate_travel_plan(self, travel_request: TravelRequest) -> TravelPlan:
        """
        Generate a complete travel plan based on user request.
        
        Args:
            travel_request: Structured travel request
            
        Returns:
            Complete TravelPlan object
        """
        try:
            logger.info(f"Generating travel plan for {travel_request.destination}")
            
            # Validate the request first
            errors = validate_travel_request(travel_request)
            if errors:
                raise ValueError(f"Invalid request: {', '.join(errors)}")
            
            # Generate the main travel plan
            plan_dict = self.planning_chain.invoke(travel_request.dict())
            
            # Convert to TravelPlan object
            travel_plan = TravelPlan(**plan_dict)
            
            logger.info("Successfully generated travel plan")
            return travel_plan
            
        except Exception as e:
            logger.error(f"Error generating travel plan: {e}")
            return self._get_fallback_travel_plan(travel_request)
    
    def enhance_travel_plan(self, travel_plan: TravelPlan) -> TravelPlan:
        """
        Enhance an existing travel plan with additional features.
        
        Args:
            travel_plan: Existing travel plan to enhance
            
        Returns:
            Enhanced travel plan
        """
        try:
            logger.info("Enhancing travel plan with additional features")
            
            # Generate hotel recommendations
            if not travel_plan.hotel_recommendations:
                hotels = self.hotel_chain.invoke({
                    "destination": travel_plan.destination,
                    "budget": travel_plan.budget,
                    "travel_style": travel_plan.travel_style,
                    "duration_days": travel_plan.duration_days
                })
                travel_plan.hotel_recommendations = hotels.get("hotel_recommendations", [])
            
            # Generate packing checklist
            if not travel_plan.packing_checklist:
                packing = self.packing_chain.invoke({
                    "destination": travel_plan.destination,
                    "duration_days": travel_plan.duration_days,
                    "travel_style": travel_plan.travel_style,
                    "start_date": travel_plan.start_date or "not_specified"
                })
                travel_plan.packing_checklist = packing.get("packing_checklist", [])
            
            # Generate travel tips
            if not travel_plan.travel_tips:
                tips = self.tips_chain.invoke({
                    "destination": travel_plan.destination,
                    "duration_days": travel_plan.duration_days,
                    "budget": travel_plan.budget
                })
                travel_plan.travel_tips = tips.get("travel_tips", [])
            
            # Generate map links
            if not travel_plan.map_links:
                maps = self.maps_chain.invoke({
                    "destination": travel_plan.destination,
                    "duration_days": travel_plan.duration_days
                })
                travel_plan.map_links = maps.get("map_links", [])
            
            logger.info("Successfully enhanced travel plan")
            return travel_plan
            
        except Exception as e:
            logger.error(f"Error enhancing travel plan: {e}")
            # Return original plan if enhancement fails
            return travel_plan
    
    def get_error_response(self, user_input: str, error_message: str) -> str:
        """
        Generate a helpful error response for the user.
        
        Args:
            user_input: Original user input
            error_message: Error that occurred
            
        Returns:
            Helpful error response string
        """
        try:
            response = self.error_chain.invoke({
                "user_input": user_input,
                "error_message": error_message
            })
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating error response: {e}")
            return "I'm having trouble processing your request right now. Please try again in a moment."
    
    def _fallback_extract_details(self, user_input: str) -> Dict[str, Any]:
        """Fallback extraction using simple pattern matching."""
        import re
        
        # Initialize defaults
        details = {
            "destination": "not_specified",
            "duration_days": 3,
            "budget": "medium",
            "travel_style": "comfort",
            "start_date": "not_specified",
            "special_requests": "not_specified"
        }
        
        user_lower = user_input.lower()
        
        # Extract destination - more flexible pattern matching
        # Look for patterns like "go to [destination]", "visit [destination]", "[destination] trip", etc.
        destination_patterns = [
            r"(?:go to|visit|travel to|want to go to|planning to visit|going to)\s+([a-zA-Z\s]+)",
            r"(?:trip to|vacation in|holiday in|tour of)\s+([a-zA-Z\s]+)",
            r"([a-zA-Z\s]+)(?:\s+trip|\s+vacation|\s+tour|\s+holiday)",
            r"(?:want to|planning|going)\s+([a-zA-Z\s]+)",
        ]
        
        for pattern in destination_patterns:
            match = re.search(pattern, user_lower)
            if match:
                dest = match.group(1).strip()
                # Clean up the destination - remove common stop words
                stop_words = ["a", "an", "the", "for", "with", "and", "in", "on", "at"]
                dest_words = [word for word in dest.split() if word not in stop_words and len(word) > 1]
                if dest_words:
                    details["destination"] = " ".join(dest_words).title()
                    break
        
        # If still not found, try to extract any capitalized words that might be destinations
        if details["destination"] == "not_specified":
            # Look for words that might be destinations (capitalized or common travel words)
            words = user_input.split()
            for i, word in enumerate(words):
                # Check if this word could be a destination
                if (word.istitle() or word.isupper()) and len(word) > 2:
                    # Skip common non-destination words
                    skip_words = ["i", "want", "to", "go", "for", "day", "days", "with", "and", "budget", "luxury", "cheap"]
                    if word.lower() not in skip_words:
                        # Take this word and possibly the next word as destination
                        potential_dest = word
                        if i + 1 < len(words) and len(words[i + 1]) > 2:
                            next_word = words[i + 1].lower()
                            if next_word not in skip_words:
                                potential_dest += " " + words[i + 1]
                        details["destination"] = potential_dest.title()
                        break
        
        # Extract duration
        duration_patterns = [
            r"(\d+)\s+days?",
            r"(\d+)\s+day",
            r"for\s+(\d+)\s+days?",
            r"(\d+)\s*-?\s*day"
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, user_lower)
            if match:
                try:
                    details["duration_days"] = int(match.group(1))
                    break
                except ValueError:
                    continue
        
        # Extract budget
        budget_keywords = {
            "budget": ["budget", "cheap", "affordable", "low cost", "economy"],
            "medium": ["medium", "moderate", "reasonable", "mid"],
            "high": ["luxury", "expensive", "high", "premium", "deluxe"]
        }
        
        for budget_level, keywords in budget_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                details["budget"] = budget_level
                break
        
        # Extract travel style
        style_keywords = {
            "budget": ["backpacker", "budget", "cheap", "basic"],
            "comfort": ["comfort", "moderate", "balanced", "standard"],
            "luxury": ["luxury", "premium", "deluxe", "high-end", "5-star"]
        }
        
        for style_level, keywords in style_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                details["travel_style"] = style_level
                break
        
        return details
    
    def _get_default_travel_details(self) -> Dict[str, Any]:
        """Get default travel details when extraction fails."""
        return {
            "destination": "not_specified",
            "duration_days": 3,
            "budget": "medium",
            "travel_style": "comfort",
            "start_date": "not_specified",
            "special_requests": "not_specified"
        }
    
    def _generate_real_map_links(self, destination: str) -> List[str]:
        """Generate real, working Google Maps links for a destination."""
        
        # Clean destination name for URL (replace spaces with +)
        clean_destination = re.sub(r'\s+', '+', destination.strip())
        
        return [
            f"https://www.google.com/maps/place/{clean_destination}",
            f"https://www.google.com/maps/search/tourist+attractions+{clean_destination}",
            f"https://www.google.com/maps/search/hotels+{clean_destination}",
            f"https://www.google.com/maps/search/restaurants+{clean_destination}",
            f"https://www.google.com/maps/search/airport+{clean_destination}"
        ]
    
    def _get_fallback_travel_plan(self, travel_request: TravelRequest) -> TravelPlan:
        """Get a basic fallback travel plan when AI generation fails."""
        logger.warning("Using fallback travel plan")
        
        # Generate real map links
        real_map_links = self._generate_real_map_links(travel_request.destination)
        
        return TravelPlan(
            destination=travel_request.destination,
            duration_days=travel_request.duration_days,
            budget=travel_request.budget,
            travel_style=travel_request.travel_style,
            start_date=travel_request.start_date,
            daily_plans=[
                {
                    "day": 1,
                    "theme": "Exploration Day",
                    "morning_activities": [{"name": "City Walk", "description": "Explore the city center", "duration": "2 hours", "cost": "Free"}],
                    "afternoon_activities": [{"name": "Local Museum", "description": "Visit a local museum", "duration": "2 hours", "cost": "$10-20"}],
                    "evening_activities": [{"name": "Dinner", "description": "Try local cuisine", "duration": "2 hours", "cost": "$20-40"}],
                    "restaurants": [{"name": "Local Restaurant", "cuisine": "Local", "price_range": "medium", "specialties": ["Local dishes"], "rating": 4.0}],
                    "places_to_visit": [{"name": "Main Square", "description": "Central meeting point", "rating": 4.0, "visit_duration": "1 hour"}],
                    "estimated_budget": "$50-100",
                    "travel_notes": "Take comfortable walking shoes"
                }
            ],
            hotel_recommendations=[
                {"name": "City Hotel", "type": "mid-range", "price_range": "$80-120", "rating": 4.0, "amenities": ["WiFi", "Breakfast"], "location": "City center"}
            ],
            packing_checklist=["Passport", "Comfortable clothes", "Camera", "Medications"],
            travel_tips=["Learn basic local phrases", "Keep emergency contacts handy"],
            map_links=real_map_links,  # Use real map links instead of placeholder
            total_estimated_cost="$200-500"
        )


def create_travel_agent() -> TravelAgent:
    """
    Factory function to create a TravelAgent instance.
    
    Returns:
        Initialized TravelAgent instance
    """
    try:
        return TravelAgent()
    except Exception as e:
        logger.error(f"Failed to create travel agent: {e}")
        raise


# Demo function for testing
def demo_travel_agent():
    """Test the travel agent functionality."""
    try:
        print("🤖 Initializing Travel Agent...")
        agent = create_travel_agent()
        
        # Test request
        user_input = "I want to plan a 5-day trip to Paris with a medium budget"
        print(f"📝 Testing: {user_input}")
        
        # Extract details
        details = agent.extract_travel_details(user_input)
        print("✅ Details extracted:", details)
        
        # Create travel request
        request = TravelRequest(**details)
        
        # Generate travel plan
        print("🗺️ Generating travel plan...")
        plan = agent.generate_travel_plan(request)
        print("🎉 Plan generated successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    demo_travel_agent()
