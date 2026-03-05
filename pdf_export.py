"""
PDF Export functionality for the AI Travel Planner.
This module handles converting travel plans to downloadable PDF format.
"""

import os
import io
from typing import Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, blue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from utils import TravelPlan


class PDFExporter:
    """
    Handles exporting travel plans to PDF format.
    
    This class creates beautiful, professional PDF documents from travel plans
    that users can download and share.
    """
    
    def __init__(self):
        """Initialize the PDF exporter with styles and formatting."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the PDF."""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E3A87'),
            alignment=TA_CENTER,
            borderWidth=0,
            borderColor=black
        )
        
        # Heading style
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#2E3A87'),
            borderWidth=1,
            borderColor=HexColor('#E0E0E0'),
            borderPadding=5
        )
        
        # Subheading style
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=HexColor('#4A5568')
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14
        )
        
        # Highlight style
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            textColor=HexColor('#2E3A87'),
            borderWidth=1,
            borderColor=HexColor('#E0E0E0'),
            borderPadding=5,
            backgroundColor=HexColor('#F7FAFC')
        )
    
    def export_travel_plan(self, travel_plan: TravelPlan, filename: Optional[str] = None) -> bytes:
        """
        Export a travel plan to PDF format.
        
        Args:
            travel_plan: The travel plan to export
            filename: Optional filename for the PDF
            
        Returns:
            PDF file as bytes
        """
        # Create a buffer to store the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build the PDF content
        story = []
        
        # Add title page
        story.extend(self._create_title_page(travel_plan))
        story.append(PageBreak())
        
        # Add table of contents
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # Add trip overview
        story.extend(self._create_trip_overview(travel_plan))
        
        # Add daily itinerary
        story.extend(self._create_daily_itinerary(travel_plan))
        
        # Add hotel recommendations
        story.extend(self._create_hotel_recommendations(travel_plan))
        
        # Add packing checklist
        story.extend(self._create_packing_checklist(travel_plan))
        
        # Add travel tips
        story.extend(self._create_travel_tips(travel_plan))
        
        # Add map links
        story.extend(self._create_map_links(travel_plan))
        
        # Build the PDF
        doc.build(story)
        
        # Get the PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_title_page(self, travel_plan: TravelPlan) -> list:
        """Create the title page content."""
        content = []
        
        # Main title
        content.append(Spacer(1, 2*inch))
        content.append(Paragraph("✈️ Travel Itinerary", self.title_style))
        content.append(Spacer(1, 0.5*inch))
        
        # Destination and duration
        content.append(Paragraph(
            f"<b>{travel_plan.destination}</b><br/>"
            f"{travel_plan.duration_days} Days • {travel_plan.budget.title()} Budget • {travel_plan.travel_style.title()} Style",
            self.heading_style
        ))
        content.append(Spacer(1, 0.5*inch))
        
        # Trip dates
        if travel_plan.start_date:
            content.append(Paragraph(
                f"Starting: {travel_plan.start_date}",
                self.body_style
            ))
        
        # Generated date
        content.append(Spacer(1, 1*inch))
        content.append(Paragraph(
            f"Generated on: {travel_plan.created_at.strftime('%B %d, %Y')}",
            self.body_style
        ))
        
        return content
    
    def _create_table_of_contents(self) -> list:
        """Create table of contents."""
        content = []
        
        content.append(Paragraph("📋 Table of Contents", self.heading_style))
        content.append(Spacer(1, 0.3*inch))
        
        toc_items = [
            ("Trip Overview", 3),
            ("Daily Itinerary", 4),
            ("Hotel Recommendations", 5),
            ("Packing Checklist", 6),
            ("Travel Tips", 7),
            ("Map Links", 8)
        ]
        
        for item, page in toc_items:
            content.append(Paragraph(f"• {item} ............. {page}", self.body_style))
        
        return content
    
    def _create_trip_overview(self, travel_plan: TravelPlan) -> list:
        """Create trip overview section."""
        content = []
        
        content.append(Paragraph("🌍 Trip Overview", self.heading_style))
        
        # Overview table
        overview_data = [
            ['Destination', travel_plan.destination],
            ['Duration', f"{travel_plan.duration_days} days"],
            ['Budget', travel_plan.budget.title()],
            ['Travel Style', travel_plan.travel_style.title()],
            ['Start Date', travel_plan.start_date or "Flexible"],
            ['Estimated Cost', travel_plan.total_estimated_cost or "To be determined"]
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E3A87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F7FAFC')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0'))
        ]))
        
        content.append(overview_table)
        content.append(Spacer(1, 0.5*inch))
        
        return content
    
    def _create_daily_itinerary(self, travel_plan: TravelPlan) -> list:
        """Create daily itinerary section."""
        content = []
        
        content.append(Paragraph("📅 Daily Itinerary", self.heading_style))
        
        for day_plan in travel_plan.daily_plans:
            content.append(Paragraph(f"Day {day_plan.day}: {day_plan.theme or 'Travel Day'}", self.subheading_style))
            
            if day_plan.date:
                content.append(Paragraph(f"Date: {day_plan.date}", self.body_style))
            
            # Morning activities
            if day_plan.morning_activities:
                content.append(Paragraph("🌅 Morning", self.body_style))
                for activity in day_plan.morning_activities:
                    content.append(Paragraph(
                        f"• <b>{activity.name}</b> - {activity.description} ({activity.duration})",
                        self.body_style
                    ))
            
            # Afternoon activities
            if day_plan.afternoon_activities:
                content.append(Paragraph("☀️ Afternoon", self.body_style))
                for activity in day_plan.afternoon_activities:
                    content.append(Paragraph(
                        f"• <b>{activity.name}</b> - {activity.description} ({activity.duration})",
                        self.body_style
                    ))
            
            # Evening activities
            if day_plan.evening_activities:
                content.append(Paragraph("🌆 Evening", self.body_style))
                for activity in day_plan.evening_activities:
                    content.append(Paragraph(
                        f"• <b>{activity.name}</b> - {activity.description} ({activity.duration})",
                        self.body_style
                    ))
            
            # Restaurants
            if day_plan.restaurants:
                content.append(Paragraph("🍽️ Recommended Restaurants", self.body_style))
                for restaurant in day_plan.restaurants:
                    content.append(Paragraph(
                        f"• <b>{restaurant.name}</b> ({restaurant.cuisine}, {restaurant.price_range}) - Rating: {restaurant.rating}/5",
                        self.body_style
                    ))
                    if restaurant.specialties:
                        specialties = ", ".join(restaurant.specialties)
                        content.append(Paragraph(f"  Specialties: {specialties}", self.body_style))
            
            # Places to visit
            if day_plan.places_to_visit:
                content.append(Paragraph("🏛️ Places to Visit", self.body_style))
                for place in day_plan.places_to_visit:
                    content.append(Paragraph(
                        f"• <b>{place.name}</b> - {place.description} (Rating: {place.rating}/5)",
                        self.body_style
                    ))
                    if place.visit_duration:
                        content.append(Paragraph(f"  Visit duration: {place.visit_duration}", self.body_style))
                    if place.entry_fee:
                        content.append(Paragraph(f"  Entry fee: {place.entry_fee}", self.body_style))
            
            # Day budget and notes
            if day_plan.estimated_budget:
                content.append(Paragraph(f"💰 Estimated budget for the day: {day_plan.estimated_budget}", self.highlight_style))
            
            if day_plan.travel_notes:
                content.append(Paragraph(f"💡 Travel tips: {day_plan.travel_notes}", self.highlight_style))
            
            content.append(Spacer(1, 0.3*inch))
        
        return content
    
    def _create_hotel_recommendations(self, travel_plan: TravelPlan) -> list:
        """Create hotel recommendations section."""
        content = []
        
        content.append(Paragraph("🏨 Hotel Recommendations", self.heading_style))
        
        if not travel_plan.hotel_recommendations:
            content.append(Paragraph("No hotel recommendations available.", self.body_style))
            return content
        
        for hotel in travel_plan.hotel_recommendations:
            content.append(Paragraph(f"<b>{hotel.name}</b>", self.subheading_style))
            content.append(Paragraph(f"Type: {hotel.type} • Price: {hotel.price_range} • Rating: {hotel.rating}/5", self.body_style))
            content.append(Paragraph(f"Location: {hotel.location}", self.body_style))
            
            if hotel.amenities:
                amenities = ", ".join(hotel.amenities)
                content.append(Paragraph(f"Amenities: {amenities}", self.body_style))
            
            content.append(Spacer(1, 0.2*inch))
        
        return content
    
    def _create_packing_checklist(self, travel_plan: TravelPlan) -> list:
        """Create packing checklist section."""
        content = []
        
        content.append(Paragraph("🎒 Packing Checklist", self.heading_style))
        
        if not travel_plan.packing_checklist:
            content.append(Paragraph("No packing checklist available.", self.body_style))
            return content
        
        for item in travel_plan.packing_checklist:
            content.append(Paragraph(f"☐ {item}", self.body_style))
        
        return content
    
    def _create_travel_tips(self, travel_plan: TravelPlan) -> list:
        """Create travel tips section."""
        content = []
        
        content.append(Paragraph("💡 Travel Tips", self.heading_style))
        
        if not travel_plan.travel_tips:
            content.append(Paragraph("No travel tips available.", self.body_style))
            return content
        
        for tip in travel_plan.travel_tips:
            content.append(Paragraph(f"• {tip}", self.body_style))
        
        return content
    
    def _create_map_links(self, travel_plan: TravelPlan) -> list:
        """Create map links section."""
        content = []
        
        content.append(Paragraph("🗺️ Map Links", self.heading_style))
        
        if not travel_plan.map_links:
            content.append(Paragraph("No map links available.", self.body_style))
            return content
        
        for i, link in enumerate(travel_plan.map_links, 1):
            content.append(Paragraph(f"{i}. {link}", self.body_style))
        
        return content


def create_pdf_exporter() -> PDFExporter:
    """
    Factory function to create a PDFExporter instance.
    
    Returns:
        Initialized PDFExporter instance
    """
    return PDFExporter()


def export_travel_plan_to_pdf(travel_plan: TravelPlan, filename: Optional[str] = None) -> bytes:
    """
    Convenience function to export a travel plan to PDF.
    
    Args:
        travel_plan: The travel plan to export
        filename: Optional filename for the PDF
        
    Returns:
        PDF file as bytes
    """
    exporter = create_pdf_exporter()
    return exporter.export_travel_plan(travel_plan, filename)


# Demo function for testing
def demo_pdf_export():
    """Demo function to test PDF export."""
    try:
        from utils import TravelPlan, DayPlan, Activity, Restaurant, Place, Hotel
        
        # Create a sample travel plan
        travel_plan = TravelPlan(
            destination="Paris, France",
            duration_days=3,
            budget="medium",
            travel_style="comfort",
            start_date="2024-06-15",
            daily_plans=[
                DayPlan(
                    day=1,
                    theme="Arrival and Exploration",
                    morning_activities=[
                        Activity(name="Airport Transfer", description="Transfer from airport to hotel", duration="1 hour", cost="€30")
                    ],
                    restaurants=[
                        Restaurant(name="Café de Flore", cuisine="French", price_range="medium", specialties=["Croissants", "Coffee"], rating=4.2)
                    ],
                    places_to_visit=[
                        Place(name="Eiffel Tower", description="Iconic Paris landmark", rating=4.8, visit_duration="2 hours", entry_fee="€25")
                    ]
                )
            ],
            hotel_recommendations=[
                Hotel(name="Hotel des Grands Boulevards", type="mid-range", price_range="€150/night", rating=4.3, amenities=["WiFi", "Breakfast"], location="City Center")
            ],
            packing_checklist=["Passport", "Comfortable shoes", "Camera"],
            travel_tips=["Learn basic French phrases", "Keep emergency contacts handy"],
            map_links=["https://maps.google.com/paris"]
        )
        
        # Export to PDF
        pdf_bytes = export_travel_plan_to_pdf(travel_plan)
        
        # Save to file for testing
        with open("travel_plan_demo.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        print("PDF exported successfully!")
        
    except Exception as e:
        print(f"PDF export demo failed: {e}")


if __name__ == "__main__":
    demo_pdf_export()
