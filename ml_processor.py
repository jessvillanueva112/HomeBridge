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
                        'description': 'Maintain meaningful connections with family and friends back home',
                        'steps': [
                            'Schedule regular video calls with loved ones',
                            'Share your daily experiences and photos',
                            'Create a shared digital space (e.g., family chat)',
                            'Plan virtual activities together'
                        ]
                    },
                    {
                        'name': 'Build Local Support',
                        'description': 'Develop a support network in your new environment',
                        'steps': [
                            'Join international student groups',
                            'Attend cultural events and meetups',
                            'Connect with peers from similar backgrounds',
                            'Participate in mentorship programs'
                        ]
                    }
                ],
                'cultural': [
                    {
                        'name': 'Cultural Integration',
                        'description': 'Gradually adapt to the new cultural environment',
                        'steps': [
                            'Explore local cultural events and festivals',
                            'Try local foods and restaurants',
                            'Learn about Canadian customs and traditions',
                            'Share your own culture with others'
                        ]
                    },
                    {
                        'name': 'Language Practice',
                        'description': 'Improve language skills in a supportive environment',
                        'steps': [
                            'Join language exchange programs',
                            'Attend conversation circles',
                            'Practice with native speakers',
                            'Use language learning apps'
                        ]
                    }
                ],
                'routine': [
                    {
                        'name': 'Structured Daily Life',
                        'description': 'Create a balanced daily routine',
                        'steps': [
                            'Set regular study and sleep schedules',
                            'Include time for self-care and relaxation',
                            'Plan meals and grocery shopping',
                            'Schedule regular exercise'
                        ]
                    },
                    {
                        'name': 'Academic Organization',
                        'description': 'Manage academic responsibilities effectively',
                        'steps': [
                            'Use a planner or digital calendar',
                            'Break tasks into smaller steps',
                            'Set realistic goals and deadlines',
                            'Utilize academic support services'
                        ]
                    }
                ],
                'emotional': [
                    {
                        'name': 'Emotional Awareness',
                        'description': 'Develop healthy emotional processing habits',
                        'steps': [
                            'Keep a personal journal',
                            'Practice mindfulness and meditation',
                            'Identify and express your feelings',
                            'Seek professional support when needed'
                        ]
                    },
                    {
                        'name': 'Self-Care Practices',
                        'description': 'Maintain physical and mental well-being',
                        'steps': [
                            'Establish a regular sleep routine',
                            'Engage in physical activity',
                            'Practice relaxation techniques',
                            'Maintain a balanced diet'
                        ]
                    }
                ]
            }
    except Exception as e:
        logger.error(f"Error loading resilience strategies: {str(e)}")
        return {
            'social': [],
            'cultural': [],
            'routine': [],
            'emotional': []
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
