"""
Utility functions and data models for the AI Travel Planner.
This module contains all the data structures and helper functions needed for the application.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import json


class Place(BaseModel):
    """Represents a tourist attraction or notable place."""
    name: str = Field(..., description="Name of the place")
    description: str = Field(..., description="Short description")
    rating: float = Field(..., ge=0, le=5, description="Rating (0-5)")
    visit_duration: Optional[str] = Field(None, description="Suggested visit duration")
    entry_fee: Optional[str] = Field(None, description="Entry fee information")
    best_time: Optional[str] = Field(None, description="Best time to visit")


class Activity(BaseModel):
    """Represents an activity during travel."""
    name: str = Field(..., description="Activity name")
    description: str = Field(..., description="Activity description")
    duration: Optional[str] = Field(None, description="Activity duration")
    cost: Optional[str] = Field(None, description="Estimated cost")


class Restaurant(BaseModel):
    """Represents a restaurant or food place."""
    name: str = Field(..., description="Restaurant name")
    cuisine: str = Field(..., description="Type of cuisine")
    price_range: str = Field(..., description="Price range (budget/medium/expensive)")
    specialties: List[str] = Field(default_factory=list, description="Must-try dishes")
    rating: float = Field(..., ge=0, le=5, description="Rating (0-5)")


class DayPlan(BaseModel):
    """Represents a complete day's itinerary."""
    day: int = Field(..., description="Day number")
    date: Optional[str] = Field(None, description="Date of travel")
    theme: Optional[str] = Field(None, description="Theme for the day")
    morning_activities: List[Activity] = Field(default_factory=list)
    afternoon_activities: List[Activity] = Field(default_factory=list)
    evening_activities: List[Activity] = Field(default_factory=list)
    restaurants: List[Restaurant] = Field(default_factory=list)
    places_to_visit: List[Place] = Field(default_factory=list)
    estimated_budget: Optional[str] = Field(None, description="Estimated budget for the day")
    travel_notes: Optional[str] = Field(None, description="Travel tips for the day")


class Hotel(BaseModel):
    """Represents hotel accommodation."""
    name: str = Field(..., description="Hotel name")
    type: str = Field(..., description="Hotel type (budget/mid-range/luxury)")
    price_range: str = Field(..., description="Price per night")
    rating: float = Field(..., ge=0, le=5, description="Rating (0-5)")
    amenities: List[str] = Field(default_factory=list, description="Available amenities")
    location: str = Field(..., description="Location description")
    booking_link: Optional[str] = Field(None, description="Booking link")


class TravelPlan(BaseModel):
    """Complete travel plan structure."""
    destination: str = Field(..., description="Travel destination")
    duration_days: int = Field(..., description="Total trip duration")
    budget: str = Field(..., description="Total budget")
    travel_style: str = Field(..., description="Travel style (budget/comfort/luxury)")
    start_date: Optional[str] = Field(None, description="Trip start date")
    
    # Core components
    daily_plans: List[DayPlan] = Field(default_factory=list)
    hotel_recommendations: List[Hotel] = Field(default_factory=list)
    
    # Additional features
    packing_checklist: List[str] = Field(default_factory=list)
    travel_tips: List[str] = Field(default_factory=list)
    map_links: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    total_estimated_cost: Optional[str] = Field(None, description="Total estimated cost")


class TravelRequest(BaseModel):
    """User travel request structure."""
    destination: str = Field(..., description="Where do you want to go?")
    duration_days: int = Field(..., description="How many days?")
    budget: str = Field(..., description="What's your budget?")
    travel_style: str = Field(..., description="Travel style preference")
    start_date: Optional[str] = Field(None, description="When do you want to travel?")
    special_requests: Optional[str] = Field(None, description="Any special requests?")
    
    def __init__(self, **data):
        """Initialize with automatic type conversion for duration_days."""
        # Convert duration_days to int if it's a string
        if 'duration_days' in data:
            try:
                data['duration_days'] = int(data['duration_days'])
            except (ValueError, TypeError):
                data['duration_days'] = 3  # Default fallback
        super().__init__(**data)


def format_travel_plan_json(plan: TravelPlan) -> str:
    """Convert travel plan to formatted JSON string."""
    return json.dumps(plan.dict(), indent=2, ensure_ascii=False)


def parse_travel_plan_from_json(json_str: str) -> TravelPlan:
    """Parse travel plan from JSON string."""
    data = json.loads(json_str)
    return TravelPlan(**data)


def calculate_trip_summary(plan: TravelPlan) -> Dict[str, Any]:
    """Calculate summary statistics for the travel plan."""
    total_places = sum(len(day.places_to_visit) for day in plan.daily_plans)
    total_activities = sum(
        len(day.morning_activities) + len(day.afternoon_activities) + len(day.evening_activities)
        for day in plan.daily_plans
    )
    total_restaurants = sum(len(day.restaurants) for day in plan.daily_plans)
    
    return {
        "total_places": total_places,
        "total_activities": total_activities,
        "total_restaurants": total_restaurants,
        "days_planned": len(plan.daily_plans),
        "hotels_recommended": len(plan.hotel_recommendations),
        "packing_items": len(plan.packing_checklist),
        "travel_tips": len(plan.travel_tips)
    }


def validate_travel_request(request: TravelRequest) -> List[str]:
    """Validate travel request and return list of errors."""
    errors = []
    
    if not request.destination or len(request.destination.strip()) < 2:
        errors.append("Please provide a valid destination")
    
    # Convert duration_days to int if it's a string
    try:
        duration = int(request.duration_days)
        if duration < 1 or duration > 30:
            errors.append("Duration must be between 1 and 30 days")
    except (ValueError, TypeError):
        errors.append("Duration must be a valid number")
    
    if not request.budget or request.budget.lower() not in ["budget", "medium", "high"]:
        errors.append("Budget must be: budget, medium, or high")
    
    if not request.travel_style or request.travel_style.lower() not in ["budget", "comfort", "luxury"]:
        errors.append("Travel style must be: budget, comfort, or luxury")
    
    return errors


def get_sample_destinations() -> List[str]:
    """Get list of popular destinations for suggestions."""
    return [
        "Paris, France",
        "Tokyo, Japan",
        "New York, USA",
        "Bali, Indonesia",
        "Dubai, UAE",
        "London, UK",
        "Rome, Italy",
        "Barcelona, Spain",
        "Amsterdam, Netherlands",
        "Singapore",
        "Sydney, Australia",
        "Cairo, Egypt"
    ]


def get_budget_options() -> Dict[str, str]:
    """Get budget options with descriptions."""
    return {
        "budget": "Budget-friendly (hostels, street food, free activities)",
        "medium": "Mid-range (3-star hotels, mix of restaurants, some paid attractions)",
        "high": "Luxury (5-star hotels, fine dining, premium experiences)"
    }


def get_travel_style_options() -> Dict[str, str]:
    """Get travel style options with descriptions."""
    return {
        "budget": "Backpacker style, focus on saving money",
        "comfort": "Balance between cost and comfort",
        "luxury": "Premium experiences, no budget constraints"
    }
