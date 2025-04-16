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

# Set NLTK data path to temporary directory
nltk.data.path.append(os.getenv('NLTK_DATA', '/tmp/nltk_data'))

# Download necessary NLTK data
def download_nltk_data():
    try:
        # Check if data already exists
        if not os.path.exists(os.path.join(nltk.data.path[0], 'tokenizers/punkt')):
            logging.info("Downloading required NLTK data...")
            nltk.download('punkt', download_dir=nltk.data.path[0])
            nltk.download('stopwords', download_dir=nltk.data.path[0])
            nltk.download('vader_lexicon', download_dir=nltk.data.path[0])
            logging.info("NLTK data downloaded successfully")
    except Exception as e:
        logging.error(f"Error downloading NLTK data: {str(e)}")
        # Fallback to basic tokenization if NLTK data is not available
        logging.warning("Using fallback tokenization method")

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
            "social": [
                {
                    "name": "Connect with Home",
                    "description": "Schedule regular video calls with family and friends back home",
                    "steps": ["Set up weekly call times", "Share photos and updates", "Write letters or emails"]
                },
                {
                    "name": "Join Student Groups",
                    "description": "Connect with other international students through campus organizations",
                    "steps": ["Attend club fairs", "Join cultural associations", "Participate in events"]
                }
            ],
            "cultural": [
                {
                    "name": "Explore Local Culture",
                    "description": "Try local restaurants and attend cultural events",
                    "steps": ["Visit local markets", "Try new foods", "Attend community events"]
                }
            ],
            "routine": [
                {
                    "name": "Build New Routines",
                    "description": "Create a daily schedule that includes both familiar and new activities",
                    "steps": ["Set regular meal times", "Plan daily activities", "Include exercise"]
                }
            ]
        }
    except Exception as e:
        logging.error(f"Error loading resilience strategies: {e}")
        return {"social": [], "cultural": [], "routine": []}

def analyze_text(text):
    """
    Analyze text to determine sentiment and homesickness level.
    Using traditional NLP techniques.
    
    Returns:
        dict: Analysis results containing sentiment_score and homesickness_level
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
        return {
            'sentiment': sentiment_score,
            'keywords': list(set(word for word in filtered_tokens if word in HOMESICKNESS_KEYWORDS)),
            'suggestions': get_resilience_strategies(text, homesickness_level)
        }
        
    except Exception as e:
        logging.error(f"Error analyzing text: {str(e)}")
        # Return default values in case of error
        return {
            'sentiment': 0.0,
            'keywords': [],
            'suggestions': get_resilience_strategies('', 5)
        }

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
        
        # Get strategies from each category
        all_strategies = []
        for category in ['social', 'cultural', 'routine']:
            if category in strategies:
                all_strategies.extend(strategies[category])
        
        # Return a subset of strategies (2-3)
        num_strategies = min(3, len(all_strategies))
        return random.sample(all_strategies, num_strategies) if all_strategies else []
        
    except Exception as e:
        logging.error(f"Error getting resilience strategies: {str(e)}")
        # Fallback strategies in case of error
        return [
            {
                "name": "Connect with Others",
                "description": "Spend time with friends or reach out to family back home.",
                "steps": ["Call a family member", "Meet a friend for coffee", "Join a student club"]
            },
            {
                "name": "Self-Care Practice",
                "description": "Take time for activities that help you relax and recharge.",
                "steps": ["Get adequate sleep", "Eat nutritious meals", "Take time for hobbies"]
            }
        ]
