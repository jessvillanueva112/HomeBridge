import nltk
import json
import random
import logging
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK data if not already available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt data...")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords data...")
    nltk.download('stopwords')

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading NLTK vader_lexicon data...")
    nltk.download('vader_lexicon')

# Force download to ensure we have all necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Keywords related to homesickness
HOMESICKNESS_KEYWORDS = [
    'miss', 'home', 'family', 'lonely', 'alone', 'far', 'different', 'culture',
    'language', 'food', 'familiar', 'friends', 'distance', 'sad', 'isolated',
    'nostalgia', 'lost', 'stranger', 'unfamiliar', 'adapt', 'adjust', 'barrier',
    'homesick', 'memory', 'memories', 'parents', 'siblings', 'comfort'
]

# Load resilience strategies
def load_resilience_strategies():
    try:
        with open('static/data/resilience_strategies.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default strategies if file not found
        return {
            "high": [
                {
                    "title": "Connect with UBC International Student Community",
                    "description": "Attend events organized by the UBC International Student Association to meet others experiencing similar challenges.",
                    "steps": ["Find upcoming events on the UBC website", "Attend at least one event this week", "Introduce yourself to at least three people"]
                },
                {
                    "title": "Virtual Family Connection",
                    "description": "Schedule regular video calls with family and friends from home.",
                    "steps": ["Set a weekly call time that works across time zones", "Share your experiences and listen to theirs", "Create a shared digital photo album"]
                },
                {
                    "title": "Cultural Comfort Food",
                    "description": "Find restaurants or learn to cook familiar dishes from your home country.",
                    "steps": ["Research local restaurants serving your cuisine", "Learn one recipe from home each week", "Host a small cultural dinner with new friends"]
                }
            ],
            "medium": [
                {
                    "title": "Gratitude Journaling",
                    "description": "Write down three things you appreciate about your new environment daily.",
                    "steps": ["Get a dedicated notebook", "Set a daily reminder", "Reflect on positive aspects of your day before sleep"]
                },
                {
                    "title": "Explore Vancouver",
                    "description": "Discover beautiful locations around Vancouver to create new positive memories.",
                    "steps": ["Visit Stanley Park", "Explore Granville Island", "Take photos of places that make you happy"]
                },
                {
                    "title": "UBC Campus Resources",
                    "description": "Utilize UBC's counseling and wellness services designed for international students.",
                    "steps": ["Book an initial consultation with UBC Counseling", "Attend a wellness workshop", "Join a peer support group"]
                }
            ],
            "low": [
                {
                    "title": "Create a Comfort Corner",
                    "description": "Design a space in your room with familiar items from home.",
                    "steps": ["Add photos, souvenirs or decorations from home", "Include sensory elements like familiar scents", "Make it your go-to relaxation spot"]
                },
                {
                    "title": "Mindfulness Practice",
                    "description": "Learn basic mindfulness techniques to stay grounded and present.",
                    "steps": ["Try a 5-minute guided meditation daily", "Practice deep breathing when feeling overwhelmed", "Use the UBC Wellness Centre resources"]
                },
                {
                    "title": "Join a Club or Activity",
                    "description": "Find a club or activity that connects to your interests or culture.",
                    "steps": ["Browse UBC's club directory", "Attend an introductory meeting", "Participate regularly in one group activity"]
                }
            ]
        }

def analyze_text(text):
    """
    Analyze text to determine sentiment and homesickness level.
    
    Returns:
        tuple: (sentiment_score, homesickness_level)
    """
    try:
        # Initialize sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Get sentiment score
        sentiment = sia.polarity_scores(text)
        sentiment_score = sentiment['compound']
        
        # Tokenize and clean text
        try:
            tokens = word_tokenize(text.lower())
        except Exception as e:
            logging.error(f"Error with word_tokenize: {str(e)}")
            # Fallback if word_tokenize fails
            tokens = text.lower().split()
        
        try:
            stop_words = set(stopwords.words('english'))
        except Exception as e:
            logging.error(f"Error loading stopwords: {str(e)}")
            # Basic English stopwords as fallback
            stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'of', 'in', 'on', 'at', 'to', 'is', 'are', 'was', 'were'}
        
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        # Calculate homesickness level based on keyword presence
        homesickness_count = sum(1 for word in filtered_tokens if word in HOMESICKNESS_KEYWORDS)
        text_length_factor = max(1, len(filtered_tokens) / 10)
        normalized_count = homesickness_count / text_length_factor
        
        # Convert to 1-10 scale
        homesickness_level = min(10, max(1, round(normalized_count * 3 + (1 - sentiment_score) * 5)))
        
        logging.debug(f"Text analysis - Sentiment: {sentiment_score}, Homesickness level: {homesickness_level}")
        return sentiment_score, homesickness_level
        
    except Exception as e:
        logging.error(f"Error analyzing text: {str(e)}")
        # Return default values in case of error
        return 0.0, 5

def get_resilience_strategies(text, homesickness_level):
    """
    Get personalized resilience strategies based on text content and homesickness level.
    
    Args:
        text (str): User's input text
        homesickness_level (int): Calculated homesickness level (1-10)
        
    Returns:
        list: List of strategy dictionaries
    """
    try:
        strategies = load_resilience_strategies()
        
        # Validate homesickness_level is within expected range
        homesickness_level = min(10, max(1, int(homesickness_level)))
        
        # Determine which category of strategies to use
        if homesickness_level >= 7:
            category = "high"
        elif homesickness_level >= 4:
            category = "medium"
        else:
            category = "low"
        
        # Select strategies from the appropriate category
        selected_strategies = strategies[category]
        
        # For a real application, we would use more sophisticated matching
        # This is a simplified approach for the MVP
        
        # Return a subset of strategies (2-3)
        num_strategies = min(3, len(selected_strategies))
        return random.sample(selected_strategies, num_strategies)
        
    except Exception as e:
        logging.error(f"Error getting resilience strategies: {str(e)}")
        # Fallback strategies in case of error
        return [
            {
                "title": "Connect with Others",
                "description": "Spend time with friends or reach out to family back home.",
                "steps": ["Call a family member", "Meet a friend for coffee", "Join a student club"]
            },
            {
                "title": "Self-Care Practice",
                "description": "Take time for activities that help you relax and recharge.",
                "steps": ["Get adequate sleep", "Eat nutritious meals", "Take time for hobbies"]
            },
            {
                "title": "Mindfulness Meditation",
                "description": "Practice being present and grounded to reduce stress.",
                "steps": ["Start with 5 minutes daily", "Focus on your breathing", "Use a guided meditation app"]
            }
        ]
