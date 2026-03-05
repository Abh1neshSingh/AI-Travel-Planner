# AI Travel Planner 🗺️✈️

![Travel Planner Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=AI+Travel+Planner+Demo)

An intelligent travel planning assistant that creates personalized, comprehensive travel itineraries using advanced AI. Simply describe your travel preferences, and watch as AI generates detailed day-by-day plans with hotels, restaurants, activities, and travel tips.

## 🌟 Key Features

### 🤖 AI-Powered Planning
- **Smart Itinerary Generation**: Personalized travel plans based on your preferences
- **Budget-Aware Planning**: Tailored recommendations for budget, medium, or luxury travel
- **Multi-Day Planning**: Detailed day-by-day breakdowns with morning, afternoon, and evening activities
- **Hotel Recommendations**: Curated accommodation suggestions matching your style and budget
- **Restaurant Guide**: Local cuisine recommendations with ratings and specialties
- **Travel Tips**: Destination-specific advice, cultural tips, and safety information

### 💬 Chat Interface
- **ChatGPT-Style Conversations**: Natural, intuitive chat interface
- **Context-Aware Responses**: AI remembers your preferences and conversation history
- **Real-Time Generation**: Watch your travel plan being created in real-time
- **Interactive Sidebar**: Easy-to-use controls for travel preferences

### 📋 Comprehensive Features
- **Packing Checklist**: Smart suggestions based on destination and duration
- **Map Links**: Google Maps integration for navigation
- **PDF Export**: Download your complete travel plan as a beautiful PDF
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Clean, professional interface with gradient designs

## 🛠️ Tech Stack

### Core Technologies
- **Streamlit**: Modern web framework for Python
- **LangChain**: Advanced AI framework for LLM orchestration
- **Mistral AI**: Powerful language model for travel planning
- **Pydantic**: Data validation and structured models

### Additional Libraries
- **ReportLab**: Professional PDF generation
- **Python-dotenv**: Environment variable management
- **Streamlit Components**: Enhanced UI components

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Mistral AI API key (get free key at [console.mistral.ai](https://console.mistral.ai/))

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/asyncarush/travel-planner-assistant
   cd travel-planner-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Mistral API key
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:8501`

## 🎯 Usage Guide

### Creating Your Travel Plan

1. **Set Your Preferences** (Sidebar):
   - Choose your destination or enter a custom one
   - Select trip duration (1-30 days)
   - Set budget level (budget/medium/high)
   - Choose travel style (budget/comfort/luxury)
   - Pick start date
   - Add any special requests

2. **Generate Plan:**
   - Click "Generate Travel Plan"
   - Watch AI create your personalized itinerary
   - Review the comprehensive day-by-day breakdown

3. **Explore Features:**
   - Expand daily itineraries for detailed activities
   - Browse hotel recommendations
   - Check packing checklist
   - Review travel tips
   - Access map links

4. **Export & Share:**
   - Download your plan as PDF
   - Share with travel companions
   - Print for your trip

### Chat with AI Assistant

- Ask questions about your destination
- Request modifications to your plan
- Get travel advice and recommendations
- Discuss specific interests or requirements

## 📁 Project Structure

```
travel-planner-assistant/
│
├── app.py                 # Main Streamlit application
├── travel_agent.py       # Core AI logic and LangChain integration
├── utils.py              # Data models and utility functions
├── prompts.py            # AI prompt templates
├── pdf_export.py         # PDF generation functionality
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required: Mistral AI API Key
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional: OpenAI API Key (alternative to Mistral)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Google Maps API Key (enhanced map features)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### API Keys Setup

1. **Mistral AI** (Recommended):
   - Visit [console.mistral.ai](https://console.mistral.ai/)
   - Create a free account
   - Generate an API key
   - Add to your `.env` file

2. **OpenAI** (Alternative):
   - Visit [platform.openai.com](https://platform.openai.com/)
   - Create an API key
   - Add to your `.env` file

## 🎨 Features Deep Dive

### AI Travel Planning

The AI uses advanced prompting to generate:
- **Structured Itineraries**: Day-by-day plans with time-based activities
- **Budget Optimization**: Recommendations matching your financial preferences
- **Local Insights**: Authentic experiences and hidden gems
- **Practical Information**: Transportation, timing, and logistics

### Data Models

Clean, structured data models ensure:
- **Type Safety**: Pydantic models for data validation
- **Consistency**: Standardized format for all travel data
- **Extensibility**: Easy to add new features and attributes
- **Reliability**: Robust error handling and fallbacks

### PDF Export

Professional PDF generation includes:
- **Beautiful Layout**: Clean typography and design
- **Complete Information**: All travel details in one document
- **Navigation**: Table of contents and section headers
- **Print-Ready**: Optimized for both screen and print

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Add comments explaining complex logic
- Keep functions small and focused
- Use type hints for better code clarity
- Test your changes thoroughly

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure your `.env` file is properly configured
   - Check that your API key is valid and active
   - Verify you have sufficient API credits

2. **Import Errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check your Python version (3.9+ required)
   - Ensure virtual environment is activated

3. **Streamlit Issues**:
   - Clear browser cache and restart
   - Check for port conflicts (default: 8501)
   - Update Streamlit: `pip install --upgrade streamlit`

4. **PDF Generation Issues**:
   - Ensure ReportLab is properly installed
   - Check available disk space
   - Verify travel plan data is complete

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and code comments
- **Community**: Join discussions in GitHub Discussions

## 📊 Example Usage

### Sample Travel Plan Request

**Input:**
- Destination: "Paris, France"
- Duration: 5 days
- Budget: Medium
- Style: Comfort
- Special: "Interested in museums, local cuisine, and day trips"

**AI Generates:**
- **Day 1**: Arrival, Eiffel Tower, Seine River cruise
- **Day 2**: Louvre Museum, Latin Quarter exploration
- **Day 3**: Versailles day trip, French dinner experience
- **Day 4**: Montmartre, Sacré-Cœur, art galleries
- **Day 5**: Shopping, departure preparations

**Includes:**
- 3 hotel recommendations (mid-range)
- 12 restaurant suggestions
- Packing checklist for France
- Paris travel tips and etiquette
- Google Maps links for navigation

## 🌟 Why This Project?

### For AI Engineers
- **LangChain Integration**: Advanced AI orchestration patterns
- **Prompt Engineering**: Sophisticated prompting techniques
- **Data Modeling**: Clean, structured AI outputs
- **Error Handling**: Robust fallback mechanisms

### For Data Scientists
- **Structured Outputs**: JSON-based AI responses
- **Data Validation**: Pydantic models for reliability
- **API Integration**: Multiple LLM provider support
- **Production Ready**: Scalable architecture

### For Recruiters
- **Modern Stack**: Latest Python AI technologies
- **Clean Code**: Well-structured, commented codebase
- **Complete Project**: End-to-end functionality
- **Professional UI**: Polished user experience

## 📜 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Mistral AI** for providing powerful language models
- **LangChain** for excellent AI orchestration framework
- **Streamlit** for beautiful web interface framework
- **ReportLab** for PDF generation capabilities

---

**🚀 Ready to start your AI-powered travel adventure?** 

Clone this repository, set up your API key, and start planning your perfect trip today!
