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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_nltk_data():
    """Download required NLTK data to /tmp directory."""
    try:
        # Set NLTK data path to /tmp
        nltk.data.path.append('/tmp/nltk_data')
        
        # Create directory if it doesn't exist
        os.makedirs('/tmp/nltk_data', exist_ok=True)
        
        # Download only required resources
        required_data = {
            'tokenizers/punkt': 'punkt',
            'corpora/stopwords': 'stopwords',
            'sentiment/vader_lexicon': 'vader_lexicon'
        }
        
        for path, resource in required_data.items():
            try:
                nltk.data.find(path)
                logger.info(f"NLTK resource {resource} already downloaded")
            except LookupError:
                logger.info(f"Downloading NLTK resource: {resource}")
                nltk.download(resource, download_dir='/tmp/nltk_data')
                logger.info(f"Successfully downloaded {resource}")
                
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {str(e)}")
        raise

# Download NLTK data on import
download_nltk_data()

# Initialize NLTK components
try:
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words('english'))
except Exception as e:
    logger.error(f"Error initializing NLTK components: {str(e)}")
    raise

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
            logger.warning("Resilience strategies file not found, using defaults")
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
        logger.error(f"Error loading resilience strategies: {str(e)}")
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
        # Get sentiment score
        sentiment = sia.polarity_scores(text)
        sentiment_score = sentiment['compound']
        
        # Tokenize and clean text
        try:
            tokens = word_tokenize(text.lower())
        except Exception as e:
            logger.error(f"Error with word_tokenize: {str(e)}")
            # Fallback if word_tokenize fails
            tokens = text.lower().split()
        
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
        
        logger.debug(f"Text analysis - Sentiment: {sentiment_score}, Homesickness level: {homesickness_level}")
        return {
            'sentiment': sentiment_score,
            'keywords': keywords,
            'suggestions': suggestions,
            'homesickness_level': homesickness_level
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        # Return default values in case of error
        return {
            'sentiment': 0.0,
            'keywords': [],
            'suggestions': [],
            'homesickness_level': 5
        }
