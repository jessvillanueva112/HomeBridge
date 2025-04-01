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

# Download necessary NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        logging.info("Downloading required NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        logging.info("NLTK data downloaded successfully")

# Download NLTK data on import
download_nltk_data()

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
        # Try to load from static/data first
        file_path = os.path.join('static', 'data', 'resilience_strategies.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        
        # Fallback to default strategies if file doesn't exist
        logging.warning("Resilience strategies file not found, using defaults")
        return {
            "strategies": [
                {
                    "name": "Connect with Home",
                    "description": "Schedule regular video calls with family and friends back home",
                    "category": "social"
                },
                {
                    "name": "Explore Local Culture",
                    "description": "Try local restaurants and attend cultural events",
                    "category": "cultural"
                },
                {
                    "name": "Build New Routines",
                    "description": "Create a daily schedule that includes both familiar and new activities",
                    "category": "routine"
                }
            ]
        }
    except Exception as e:
        logging.error(f"Error loading resilience strategies: {e}")
        return {"strategies": []}

def analyze_text(text):
    """
    Analyze text to determine sentiment and homesickness level.
    Using Gemini API if available, with fallback to traditional NLP techniques.
    
    Returns:
        tuple: (sentiment_score, homesickness_level)
    """
    try:
        # First, try to use Gemini for enhanced analysis
        from utils.gemini_integration import generate_analysis
        
        gemini_analysis = generate_analysis(text)
        
        if gemini_analysis and "sentiment_score" in gemini_analysis and "homesickness_level" in gemini_analysis:
            sentiment_score = gemini_analysis["sentiment_score"]
            homesickness_level = gemini_analysis["homesickness_level"]
            logging.info(f"Using Gemini analysis: Sentiment={sentiment_score}, Homesickness={homesickness_level}")
            return sentiment_score, homesickness_level
        
        # Fallback to traditional analysis if Gemini isn't available or response didn't contain expected fields
        logging.info("Falling back to traditional text analysis")
        
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
    Using Gemini API if available, with fallback to traditional method.
    
    Args:
        text (str): User's input text
        homesickness_level (int): Calculated homesickness level (1-10)
        
    Returns:
        list: List of strategy dictionaries
    """
    try:
        # First, try to use Gemini for personalized strategies
        from utils.gemini_integration import generate_resilience_strategies
        
        gemini_strategies = generate_resilience_strategies(text, homesickness_level)
        
        if gemini_strategies and len(gemini_strategies) > 0:
            logging.info(f"Using Gemini-generated strategies: {len(gemini_strategies)} strategies returned")
            return gemini_strategies
        
        # Fallback to traditional approach if Gemini isn't available
        logging.info("Falling back to traditional strategy selection")
        
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
