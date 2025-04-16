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

def load_resilience_strategies():
    """Load resilience strategies from JSON file or return defaults."""
    try:
        file_path = os.path.join('static', 'data', 'resilience_strategies.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            logging.warning("Resilience strategies file not found, using defaults")
            return {
                'social': [
                    {
                        'name': 'Connect with Home',
                        'description': 'Regular video calls with family and friends',
                        'steps': [
                            'Schedule weekly video calls with family',
                            'Join family group chats',
                            'Share daily updates with close friends'
                        ]
                    },
                    {
                        'name': 'Join Student Groups',
                        'description': 'Connecting with other international students',
                        'steps': [
                            'Attend UBC International Student Association events',
                            'Join cultural student groups',
                            'Participate in language exchange programs'
                        ]
                    }
                ],
                'cultural': [
                    {
                        'name': 'Explore Local Culture',
                        'description': 'Engaging with local restaurants and events',
                        'steps': [
                            'Visit local cultural festivals',
                            'Try new restaurants weekly',
                            'Join cultural workshops'
                        ]
                    }
                ],
                'routine': [
                    {
                        'name': 'Build New Routines',
                        'description': 'Creating a daily schedule with familiar and new activities',
                        'steps': [
                            'Establish a morning routine',
                            'Schedule regular study times',
                            'Include exercise in daily schedule'
                        ]
                    }
                ]
            }
    except Exception as e:
        logging.error(f"Error loading resilience strategies: {str(e)}")
        return {
            'social': [],
            'cultural': [],
            'routine': []
        }

def analyze_text(text):
    """
    Analyze text to determine sentiment and homesickness level.
    Returns:
        dict: Analysis results containing sentiment, keywords, and suggestions
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
        
        # Get matching keywords
        keywords = list(set(word for word in filtered_tokens if word in HOMESICKNESS_KEYWORDS))
        
        # Get suggestions based on homesickness level
        strategies = load_resilience_strategies()
        suggestions = []
        
        # Select strategies from each category
        for category in ['social', 'cultural', 'routine']:
            if category in strategies and strategies[category]:
                suggestions.append(random.choice(strategies[category]))
        
        logging.debug(f"Text analysis - Sentiment: {sentiment_score}, Homesickness level: {homesickness_level}")
        return {
            'sentiment': sentiment_score,
            'keywords': keywords,
            'suggestions': suggestions,
            'homesickness_level': homesickness_level
        }
        
    except Exception as e:
        logging.error(f"Error analyzing text: {str(e)}")
        # Return default values in case of error
        return {
            'sentiment': 0.0,
            'keywords': [],
            'suggestions': [],
            'homesickness_level': 5
        }
